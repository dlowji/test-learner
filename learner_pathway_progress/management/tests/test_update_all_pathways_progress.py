"""
Tests for populate pathway membership and progress management command.
"""
from unittest import TestCase
from unittest.mock import patch

import pytest
from django.contrib.sites.models import Site
from opaque_keys.edx.keys import CourseKey

from learner_pathway_progress.management.commands import update_all_pathways_progress
from learner_pathway_progress.models import LearnerPathwayMembership, LearnerPathwayProgress
from test_utils.constants import (
    LEARNER_PATHWAY_UUID,
    LEARNER_PATHWAY_UUID2,
    LEARNER_PATHWAY_UUID3,
    LEARNER_PATHWAY_UUID4,
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
class TestUpdateAllPathwaysProgress(TestCase):
    """
    Tests upgrade progress and create membership for learner pathways management command.
    """

    def setUp(self):
        super().setUp()
        Site.objects.get_or_create(domain='example.com')
        self.command = update_all_pathways_progress.Command()
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

    @patch("openedx.core.djangoapps.catalog.utils.check_catalog_integration_and_get_user")
    @patch("learner_pathway_progress.utilities.get_all_learner_pathways", )
    def test_membership_and_progress_if_enrollment_exists(self, mocked_all_learner_pathways, mock_user):
        mocked_all_learner_pathways.return_value = LearnerPathwayProgressOutputs.all_pathways_from_discovery
        mock_user.return_value = self.user, None
        self.command.handle()
        pathway_membership = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()
        pathway_membership2 = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID2
        ).exists()

        pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID
        ).exists()
        pathway_progress2 = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID2
        ).exists()

        self.assertTrue(pathway_membership)
        self.assertTrue(pathway_membership2)
        self.assertTrue(pathway_progress)
        self.assertTrue(pathway_progress2)

    @patch("openedx.core.djangoapps.catalog.utils.check_catalog_integration_and_get_user")
    @patch("learner_pathway_progress.utilities.get_all_learner_pathways", )
    def test_membership_and_progress_if_no_courses_linked_with_pathway(self, mocked_all_learner_pathways, mock_user):
        mocked_all_learner_pathways.return_value = LearnerPathwayProgressOutputs.all_pathways_from_discovery
        mock_user.return_value = self.user, None
        self.command.handle()
        pathway_membership = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID3
        ).exists()

        pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID3
        ).exists()
        self.assertFalse(pathway_membership)
        self.assertFalse(pathway_progress)

    @patch("openedx.core.djangoapps.catalog.utils.check_catalog_integration_and_get_user")
    @patch("learner_pathway_progress.utilities.get_all_learner_pathways", )
    def test_membership_and_progress_if_courses_linked_with_pathway_are_not_enrolled(
        self,
        mocked_all_learner_pathways,
        mock_user,
    ):
        mocked_all_learner_pathways.return_value = LearnerPathwayProgressOutputs.all_pathways_from_discovery
        mock_user.return_value = self.user, None
        self.command.handle()
        pathway_membership = LearnerPathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID4
        ).exists()

        pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID4
        ).exists()
        self.assertFalse(pathway_membership)
        self.assertFalse(pathway_progress)
