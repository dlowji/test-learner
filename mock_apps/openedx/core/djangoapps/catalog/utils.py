from django.contrib.auth.models import User

from test_utils.constants import TEST_USER_EMAIL


def get_catalog_api_base_url():
    return None


def check_catalog_integration_and_get_user(error_message_field):
    user = User.objects.get(email=TEST_USER_EMAIL)
    return user, None


def get_catalog_api_client(user):
    return None
