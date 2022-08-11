"""
Root API URLs.
"""
from django.conf.urls import include
from django.urls import path

app_name = 'learner_pathway_progress'

urlpatterns = [
    path('v1/', include('learner_pathway_progress.api.v1.urls')),
]
