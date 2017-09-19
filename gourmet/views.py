from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status

from django.conf import settings
from .forms import SearchFormSerializer
from .utils import get_popular_words

MAX_REVIEWS_COUNT_PER_HIT = getattr(settings, 'MAX_REVIEWS_COUNT_PER_HIT', 20)


class ReviewSearchAPI(generics.GenericAPIView):

    serializer_class = SearchFormSerializer

    def get_reviews_index(self):
        """
        Returns the reviews index.
        For now, reading from file on every server restart. Any change will be handled here.
        """

        return settings.REVIEWS_INDEX

    def get_reviews_data(self):
        """
        Returns review data.
        For now, reading from file on every server restart. Any change will be handled here.
        """
        return settings.REVIEWS_DATA

    def post(self, request):
        query = request.data.get('query', [])
        query = query.split(" ")
        if not query:
            return Response({"error": "Insufficient arguments"}, http_status.HTTP_400_BAD_REQUEST)

        review_indices = []
        [review_indices.extend(self.get_reviews_index().get(q.lower(), [])) for q in query]

        review_ids_by_score, score_dict = get_popular_words(review_indices, MAX_REVIEWS_COUNT_PER_HIT)

        # Handling tie and sorting (if query_score is same). Sorting by 'review/score' in that case.
        result = []
        last_score, last_index = None, None
        for i, review_id in enumerate(review_ids_by_score):
            review = self.get_reviews_data()[review_id]
            query_score = score_dict.get(review_id)

            if query_score == last_score:

                list_pre, list_post = result[:last_index], result[i+1:]
                li = result[last_index:i+1]
                li.append(review)
                sorted_list = sorted(li, key=lambda k: k['review/score'], reverse=True)
                result = list_pre + sorted_list + list_post
            else:
                result.append(review)
                last_index = i
            last_score = query_score

        return Response(result, http_status.HTTP_200_OK)
