""" API v1 views """

from django_filters.rest_framework import DjangoFilterBackend
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learner_pathway_progress.api.filters import PathwayProgressUUIDFilter
from learner_pathway_progress.api.serializers import LearnerPathwayProgressSerializer, AuthorSerializer
from learner_pathway_progress.models import LearnerEnterprisePathwayMembership, LearnerPathwayProgress, Author


class AuthorAPIView(APIView):

    permission_classes = (AllowAny,)

    #Handles GET request to get a list of all instances
    def get(self, request):
        authors = Author.objects.all()
        serializers = AuthorSerializer(authors, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    #Handles POST request to create a new instance
    def post(self, request):
        
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name')
        }
        
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)