"""
Tests for updating pathway progress management command.
"""
import json
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

import pytest
from django.contrib.sites.models import Site
from lms.djangoapps.grades.models import PersistentCourseGrade
from opaque_keys.edx.keys import CourseKey
from pytz import UTC

from learner_pathway_progress.management.commands import update_existing_pathways_progress
from learner_pathway_progress.models import LearnerPathwayProgress
from test_utils.constants import (
    ENTERPRISE_CUSTOMER_UUID,
    LEARNER_PATHWAY_UUID,
    TEST_USER_EMAIL,
    LearnerPathwayProgressOutputs,
)
from test_utils.factories import (
    CourseEnrollmentFactory,
    EnterpriseCourseEnrollmentFactory,
    EnterpriseCustomerFactory,
    EnterpriseCustomerUserFactory,
    UserFactory,
)
from test_utils.utils import count_completed_courses


@pytest.mark.django_db
class TestUpdateAllExitingPathwaysProgress(TestCase):
    """
    Tests upgrade existing pathways progress for learners through management command.
    """

    def setUp(self):
        super().setUp()
        Site.objects.get_or_create(domain='example.com')
        self.command = update_existing_pathways_progress.Command()
        self.user = UserFactory.create(email=TEST_USER_EMAIL)
        self.course_keys = []
        self.enterprise_customer = EnterpriseCustomerFactory(uuid=ENTERPRISE_CUSTOMER_UUID)
        enterprise_customer_user = EnterpriseCustomerUserFactory(
            user_id=self.user.id,
            enterprise_customer=self.enterprise_customer
        )
        for i in range(8):
            self.course_keys.insert(i, CourseKey.from_string(f"course-v1:test-enterprise+test1+202{i}"))
        for i in [0, 5]:
            course_enrollment = CourseEnrollmentFactory.create(
                user=self.user,
                course_id=self.course_keys[i],
                mode='verified'
            )
            EnterpriseCourseEnrollmentFactory(
                enterprise_customer_user=enterprise_customer_user,
                course_id=course_enrollment.course_id
            )

    @patch("openedx.core.djangoapps.catalog.utils.check_catalog_integration_and_get_user")
    def test_enterprise_membership_and_progress_if_enrollment_exists(self, mock_user):
        mock_user.return_value = self.user, None

        pathway_progress = LearnerPathwayProgress.objects.create(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID,
            learner_pathway_progress=LearnerPathwayProgressOutputs.updated_learner_progress2
        )

        self.command.handle()

        pathway_snapshot = json.loads(pathway_progress.learner_pathway_progress)
        completion_count = count_completed_courses(pathway_snapshot, pathway_progress, self.user)

        self.assertEqual(completion_count, 0)

        course_grade_params = {
            "user_id": self.user.id,
            "course_id": 'course-v1:test-enterprise+test1+2020',
            "percent_grade": 77.7,
            "letter_grade": "pass",
            "passed_timestamp": datetime(2011, 1, 1, tzinfo=UTC)
        }

        PersistentCourseGrade.objects.create(**course_grade_params)

        pathway_progress = LearnerPathwayProgress.objects.get(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID,
        )

        self.command.handle()

        pathway_snapshot = json.loads(pathway_progress.learner_pathway_progress)
        completion_count = count_completed_courses(pathway_snapshot, pathway_progress, self.user)

        self.assertEqual(completion_count, 1)
