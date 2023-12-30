"""
Root API URLs.
"""
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from .v1 import views
app_name = 'learner_pathway_progress'

urlpatterns = [
    # path('author/', include('learner_pathway_progress.api.v1.urls')),
    path('admin/', admin.site.urls),
    path('author/', views.AuthorAPIView.as_view()),
]
