from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase

from gourmet.utils import load_json_data


class GourmetSearchTest(TestCase):

    def test_reviews_search_post(self):
        url = reverse('gourmet:reviews_search')
        # Positive scenario
        response = self.client.post(url, {"query": "admittedly coffee"})
        self.assertEqual(response.status_code, 200)
        # Negative scenario
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_utils_load_json(self):
        # Positive scenario
        file_path_valid = settings.FILES["REVIEWS"]["INDEX_REVIEW_LEVEL"]
        data = load_json_data(file_path_valid)
        self.assertEqual(type(data), dict)
        # Negative scenario
        file_path_invalid = "/test/test.txt"
        data = load_json_data(file_path_invalid)
        self.assertIsNone(data)

    def test_static_data(self):
        self.assertEqual(type(settings.REVIEWS_DATA), list)
        self.assertEqual(type(settings.REVIEWS_INDEX_TERM_LEVEL), dict)
        self.assertEqual(type(settings.REVIEWS_INDEX_REVIEW_LEVEL), dict)


