#!/usr/bin/env python
"""
Tests for the `learner-pathway-progress` models module.
"""

from uuid import UUID

import ddt
from django.contrib.auth import get_user_model
from django.test import TestCase
from opaque_keys.edx.keys import CourseKey

from learner_pathway_progress.models import LearnerPathwayProgress
from test_utils.constants import LearnerPathwayProgressOutputs
from test_utils.factories import (
    CourseEnrollmentFactory,
    LearnerEnterprisePathwayMembershipFactory,
    LearnerPathwayProgressFactory,
)

User = get_user_model()


@ddt.ddt
class LearnerPathwayProgressModelTests(TestCase):
    """
    Tests for the LearnerPathwayProgress model.
    """
    def setUp(self):
        """
        Set up test data
        """
        super().setUp()
        self.user = User.objects.create(username="rocky")
        self.user2 = User.objects.create(username="rocky2")
        self.learner_pathway_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b1")
        self.program1_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b2")
        self.program2_uuid = UUID("1f301a72-f344-4a31-9e9a-e0b04d8d86b3")
        LearnerPathwayProgressFactory.create(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid,
        )
        LearnerPathwayProgressFactory.create(
            user=self.user2,
            learner_pathway_uuid=self.learner_pathway_uuid,
        )
        self.course_keys = []
        for i in range(8):
            self.course_keys.insert(i, CourseKey.from_string(f"course-v1:test-enterprise+test1+202{i}"))

    def test_update_progress_when_single_enrollment_in_each_step(self):
        """
        Test the case when a learner has a single course enrollment for each step in the pathway.
        """
        for i in [0, 5]:
            CourseEnrollmentFactory.create(
                user=self.user2,
                course_id=self.course_keys[i],
                mode='verified'
            )
        learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user2,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        self.assertEqual(
            learner_pathway_progress.learner_pathway_progress,
            LearnerPathwayProgressOutputs.snapshot_from_discovery
        )
        learner_pathway_progress.update_pathway_progress()
        updated_learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user2,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        expected_learner_pathway_progress = LearnerPathwayProgressOutputs.updated_learner_progress2
        self.assertEqual(
            updated_learner_pathway_progress.learner_pathway_progress,
            expected_learner_pathway_progress
        )

    def test_update_progress_when_single_enrolled_run_in_each_course(self):
        """
        Test the case when a learner has a single enrollment for each course in the pathway.
        """
        for i in [1, 3, 4, 7]:
            CourseEnrollmentFactory.create(
                user=self.user,
                course_id=self.course_keys[i],
                mode='verified'
            )
        learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        self.assertEqual(
            learner_pathway_progress.learner_pathway_progress,
            LearnerPathwayProgressOutputs.snapshot_from_discovery
        )
        learner_pathway_progress.update_pathway_progress()
        updated_learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        expected_learner_pathway_progress = LearnerPathwayProgressOutputs.updated_learner_progress1
        self.assertEqual(
            updated_learner_pathway_progress.learner_pathway_progress,
            expected_learner_pathway_progress
        )

    def test_update_progress_when_all_courses_enrolled_in_all_steps(self):
        """
        Test the case when a learner is enrolled in all course runs for each course in the pathway.
        """
        for i in range(8):
            CourseEnrollmentFactory.create(
                user=self.user,
                course_id=self.course_keys[i],
                mode='verified'
            )
        learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        self.assertEqual(
            learner_pathway_progress.learner_pathway_progress,
            LearnerPathwayProgressOutputs.snapshot_from_discovery
        )
        learner_pathway_progress.update_pathway_progress()
        updated_learner_pathway_progress = LearnerPathwayProgress.objects.filter(
            user=self.user,
            learner_pathway_uuid=self.learner_pathway_uuid
        ).first()
        expected_learner_pathway_progress = LearnerPathwayProgressOutputs.updated_learner_progress1
        self.assertEqual(
            updated_learner_pathway_progress.learner_pathway_progress,
            expected_learner_pathway_progress
        )


class LearnerEnterprisePathwayMembershipTests(TestCase):
    """
    LearnerEnterprisePathwayMembership model tests
    """
    def setUp(self):
        super().setUp()
        self.membership = LearnerEnterprisePathwayMembershipFactory()

    def test_string_representation(self):
        """
        Test the string representation of the LearnerEnterprisePathwayMembership model.
        """
        pathway_uuid = self.membership.learner_pathway_uuid
        user = self.membership.user
        enterprise_customer_uuid = self.membership.enterprise_customer_uuid
        expected_str = f'User: {user}, Pathway UUID: {pathway_uuid}, Enterprise UUID: {enterprise_customer_uuid}'
        expected_repr = f'<LearnerEnterprisePathwayMembership user={user} pathway_uuid="{pathway_uuid}"' \
                        f' Enterprise UUID: {enterprise_customer_uuid}>'
        assert expected_str == str(self.membership)
        assert expected_repr == repr(self.membership)
