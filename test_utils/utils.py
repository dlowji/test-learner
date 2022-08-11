"""
Utils for `learner-pathway-progress` tests.
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

User = get_user_model()


def make_request(query_param=None, user=None):
    """
    creates a request objects, associates with user, add query params and returns.
    """
    if not user:
        user = User.objects.create(username="rockey")
    if query_param:
        request = APIRequestFactory().get('/', query_param)
    else:
        request = APIRequestFactory().get('/')
    request.user = user

    # Convert a Django HTTPResponse object into a rest_framework.request
    # using a generic API view. This is necessary because the drf-flex-fields
    # library relies on the `.query_params` property of the request. DRF requests
    # always have the `query_params` parameter unless the request is created using
    # `APIRequestFactory`, which yelds Django's standard `HttpRequest`.
    # Documentation: https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
    # DRF issue: https://github.com/encode/django-rest-framework/issues/6488
    return APIView().initialize_request(request)
