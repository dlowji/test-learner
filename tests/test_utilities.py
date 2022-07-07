"""
Tests for utilities.
"""
from unittest import TestCase
from unittest.mock import patch

import pytest
from django.contrib.sites.models import Site
from edx_toggles.toggles.testutils import override_waffle_switch
from opaque_keys.edx.keys import CourseKey

from learner_pathway_progress.models import LearnerPathwayMembership, LearnerPathwayProgress
from learner_pathway_progress.utilities import get_pathway_course_run_keys, update_learner_pathway_progress
from learner_pathway_progress.waffle import ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH
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
@override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=True)
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
                course_id=str(course_enrollment.course_id)
            )

    @patch("learner_pathway_progress.utilities.get_pathway_snapshot", )
    @patch("learner_pathway_progress.utilities.get_learner_pathways_associated_with_course", )
    def test_update_learner_pathway_progress(self, mocked_pathways_associated_with_course, mock_pathway_snapshot):
        """
        Test if learner course attached with the pathway, his progress and membership record created.
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
        mocked_pathways_associated_with_course.assert_called_with(self.user, str(self.course_keys[0]))

    @patch("learner_pathway_progress.utilities.get_pathway_snapshot")
    @patch("learner_pathway_progress.utilities.get_learner_pathways_associated_with_course")
    def test_update_learner_pathway_progress_not_created(self, mocked_pathways_associated_with_course,
                                                         mock_pathway_snapshot):
        """
        Test if learner course attached with none of the pathways, his progress and membership record not created
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
        mocked_pathways_associated_with_course.assert_called_with(self.user, str(self.course_keys[0]))

    @patch("learner_pathway_progress.utilities.get_pathway_snapshot")
    @patch("learner_pathway_progress.utilities.get_learner_pathways_associated_with_course")
    def test_update_learner_pathway_progress_with_wrong_course_key(self,
                                                                   mocked_pathways_associated_with_course,
                                                                   mock_pathway_snapshot):
        """
        Test if learner course_key is not in CourseLocator format, do not call
         get_learner_pathways_associated_with_course method and create membership or progress record.
        """
        mock_pathway_snapshot.return_value = LearnerPathwayProgressOutputs.single_pathway_from_discovery
        update_learner_pathway_progress(self.user.id, 'course-v1:abc/2022')
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
        self.assertFalse(mocked_pathways_associated_with_course.called)

    def test_get_pathway_course_run_keys(self):
        """
        Test if learner course_key is not in CourseLocator format, do not call
         get_learner_pathways_associated_with_course method and create membership or progress record.
        """
        pathway_course_runs = []
        pathway = LearnerPathwayProgressOutputs.single_pathway_from_discovery
        pathway_steps = pathway.get('steps') or []
        for step in pathway_steps:
            step_courses = step.get('courses') or []
            step_programs = step.get('programs') or []
            get_pathway_course_run_keys(step_courses, step_programs, pathway_course_runs)

        expected_pathway_course_runs = ['course-v1:test-enterprise+test1+2020',
                                        'course-v1:test-enterprise+test1+2021',
                                        'course-v1:test-enterprise+test1+2022',
                                        'course-v1:test-enterprise+test1+2023',
                                        'course-v1:edX+DemoX+Demo_Course',
                                        'course-v1:test-course-generator+8344+1',
                                        'course-v1:test-enterprise+test1+2024',
                                        'course-v1:test-enterprise+test1+2025',
                                        'course-v1:test-enterprise+test1+2026',
                                        'course-v1:test-enterprise+test1+2027',
                                        ]

        self.assertEqual(
            pathway_course_runs,
            expected_pathway_course_runs
        )
