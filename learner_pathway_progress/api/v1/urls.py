"""
Api URLs for learner_pathway_progress.
"""
from rest_framework import routers

from .views import (
    AuthorAPIView,
)

router = routers.DefaultRouter()
# router.register('api', AuthorAPIView.as_view(), basename='author'),

urlpatterns = router.urls
