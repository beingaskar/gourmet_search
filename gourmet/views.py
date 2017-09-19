from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status

from django.conf import settings
from .forms import SearchFormSerializer

MAX_REVIEWS_COUNT_PER_HIT = getattr(settings, 'MAX_REVIEWS_COUNT_PER_HIT', 20)


class ReviewSearchAPI(generics.GenericAPIView):

    serializer_class = SearchFormSerializer

    def get_index(self):
        """
        Returns the reviews index.
        For now, reading from file on every server restart. Any change will be handled here.
        """

        return settings.REVIEWS_INDEX_TERM_LEVEL, \
               settings.REVIEWS_INDEX_REVIEW_LEVEL

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

        index_term_level, index_review_level = self.get_index()

        review_indices = []
        [review_indices.extend(index_term_level.get(q.lower(), [])) for q in query]

        reviews_score_data = []
        for ind in set(review_indices):
            ind = str(ind)
            query_score = 0
            for q in query:
                query_score += index_review_level[ind]["terms"].get(q, 0)
            reviews_score_data.append(
                {
                    'query_score': query_score,
                    'review_score': index_review_level[ind]["review_score"],
                    'id': ind
                }
            )

        reviews_score_data = sorted(
            reviews_score_data,
            key=lambda score_data: (score_data['query_score'], score_data['review_score']),
            reverse=True
        )

        reviews_data = self.get_reviews_data()

        reviews_data = [reviews_data[int(review['id'])] for review in reviews_score_data[:20]]

        return Response(reviews_data, http_status.HTTP_200_OK)
