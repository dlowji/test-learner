"""
Tests for utilities.
"""
from unittest import TestCase
from unittest.mock import patch

import pytest
from django.contrib.sites.models import Site
from opaque_keys.edx.keys import CourseKey

from learner_pathway_progress.models import LearnerPathwayMembership, LearnerPathwayProgress
from learner_pathway_progress.utilities import update_learner_pathway_progress
from test_utils.constants import (
    LEARNER_PATHWAY_UUID,
    LEARNER_PATHWAY_UUID2,
    TEST_USER_EMAIL,
    LearnerPathwayProgressOutputs,
)
from test_utils.factories import (
    CourseEnrollmentFactory,
    EnterpriseCourseEnrollmentFactory,
    EnterpriseCustomerUserFactory,
    UserFactory,
)


@pytest.mark.django_db
class TestUpdateLearnerPathwayProgress(TestCase):
    """
    Tests for utilities responsible for learner pathway progress upgrade.
    """

    def setUp(self):
        super().setUp()
        Site.objects.get_or_create(domain='example.com')
        self.user = UserFactory.create(email=TEST_USER_EMAIL)
        self.course_keys = []
        for i in range(8):
            self.course_keys.insert(i, CourseKey.from_string(f"course-v1:test-enterprise+test1+202{i}"))
        for i in [0, 5]:
            course_enrollment = CourseEnrollmentFactory.create(
                user=self.user,
                course_id=self.course_keys[i],
                mode='verified'
            )
            enterprise_customer_user = EnterpriseCustomerUserFactory(user_id=self.user.id)
            EnterpriseCourseEnrollmentFactory(
                enterprise_customer_user=enterprise_customer_user,
                course_id=course_enrollment.course_id
            )

    @patch("learner_pathway_progress.utilities.get_pathway_snapshot", )
    @patch("learner_pathway_progress.utilities.get_learner_pathways_associated_with_course", )
    def test_update_learner_pathway_progress(self, mocked_pathways_associated_with_course, mock_pathway_snapshot):
        """
        Test if learner course attached with the pathway and progress and membership record created.
        """
        mocked_pathways_associated_with_course.return_value = [LEARNER_PATHWAY_UUID, LEARNER_PATHWAY_UUID2]
        mock_pathway_snapshot.return_value = LearnerPathwayProgressOutputs.single_pathway_from_discovery
        update_learner_pathway_progress(self.user.id, self.course_keys[0])
        pathway_membership = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()

        pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()

        self.assertTrue(pathway_membership)
        self.assertTrue(pathway_progress)

    @patch("learner_pathway_progress.utilities.get_pathway_snapshot")
    @patch("learner_pathway_progress.utilities.get_learner_pathways_associated_with_course")
    def test_update_learner_pathway_progress_not_created(self, mocked_pathways_associated_with_course,
                                                         mock_pathway_snapshot):
        """
        Test if learner course attached with none of the pathways.
        """
        mocked_pathways_associated_with_course.return_value = []
        mock_pathway_snapshot.return_value = LearnerPathwayProgressOutputs.single_pathway_from_discovery
        update_learner_pathway_progress(self.user.id, self.course_keys[0])
        pathway_membership = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()

        pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()

        self.assertFalse(pathway_membership)
        self.assertFalse(pathway_progress)
