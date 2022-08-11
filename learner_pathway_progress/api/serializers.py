"""
Serializers for Learner Pathway Progress APIs.
"""

import json

from rest_framework import serializers

from learner_pathway_progress.models import LearnerPathwayProgress


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
