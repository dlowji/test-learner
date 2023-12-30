"""
Serializers for Learner Pathway Progress APIs.
"""

import json

from rest_framework import serializers

from learner_pathway_progress.models import LearnerPathwayProgress, Author


class LearnerPathwayProgressSerializer(serializers.ModelSerializer):
    """
    Serializer for LearnerPathwayProgress model.
    """
    learner_pathway_progress = serializers.SerializerMethodField()

    class Meta:
        model = LearnerPathwayProgress
        fields = ['learner_pathway_progress']

    def get_learner_pathway_progress(self, obj):
        return json.loads(obj.learner_pathway_progress) if obj.learner_pathway_progress else {}
    
    
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    """

    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

    # def get_author(self, obj):
    #     return json.loads(obj)
