#!/usr/bin/env python
"""
Tests for `learner-pathway-progress` serializers.
"""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from learner_pathway_progress.api.serializers import LearnerPathwayProgressSerializer
from learner_pathway_progress.models import LearnerPathwayProgress
from test_utils.constants import LEARNER_PATHWAY_A_UUID, LEARNER_PATHWAY_PROGRESS_DATA
from test_utils.utils import make_request

User = get_user_model()


class TestLearnerPathwayProgressSerializer(TestCase):
    """
    Tests for LearnerPathwayProgressSerializer.
    """
    serializer_class = LearnerPathwayProgressSerializer

    def setUp(self):
        """
        Test set up
        """
        super().setUp()
        self.user = User.objects.create(username="rocky")

    def create_pathway_progress(self):
        """
        returns pathway after creating and associating with the user.
        """
        learner_pathway_progress = LearnerPathwayProgress.objects.create(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_A_UUID,
            learner_pathway_progress=json.dumps(LEARNER_PATHWAY_PROGRESS_DATA[0]['learner_pathway_progress'])
        )
        return learner_pathway_progress

    def test_data(self):
        """
        verifies whether serializer returns correct data.
        """
        request = make_request(user=self.user)
        pathway_progress = self.create_pathway_progress()
        serializer = self.serializer_class(pathway_progress, context={'request': request})
        self.assertDictEqual(serializer.data, LEARNER_PATHWAY_PROGRESS_DATA[0])
