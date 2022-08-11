"""
Api URLs for learner_pathway_progress.
"""
from rest_framework import routers

from learner_pathway_progress.api.v1 import views

router = routers.SimpleRouter()
router.register(r'progress', views.LearnerPathwayProgressViewSet, basename='learner-pathway-progress')

urlpatterns = router.urls
