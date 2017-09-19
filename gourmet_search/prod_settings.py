from .settings import *

from gourmet.utils import load_json_data


INSTALLED_APPS += ("gunicorn",)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Static Data
# Load static data from json to settings variable.

REVIEWS_INDEX_TERM_LEVEL = load_json_data(FILES["REVIEWS"]["INDEX_TERM_LEVEL"])
REVIEWS_INDEX_REVIEW_LEVEL = load_json_data(FILES["REVIEWS"]["INDEX_REVIEW_LEVEL"])
REVIEWS_DATA = load_json_data(FILES["REVIEWS"]["DATA"])
