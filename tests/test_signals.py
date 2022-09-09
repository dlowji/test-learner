"""
Tests for signals.
"""
from unittest import TestCase
from unittest.mock import patch

import ddt
import pytest
from edx_toggles.toggles.testutils import override_waffle_switch
from opaque_keys.edx.keys import CourseKey

from learner_pathway_progress.models import LearnerEnterprisePathwayMembership
from learner_pathway_progress.signals import (
    create_learner_enterprise_pathway_membership_for_user,
    listen_for_course_grade_upgrade_in_learner_pathway,
)
from learner_pathway_progress.waffle import ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH
from test_utils.constants import LEARNER_PATHWAY_UUID, TEST_USER_EMAIL
from test_utils.factories import (
    CourseEnrollmentFactory,
    EnterpriseCourseEnrollmentFactory,
    EnterpriseCustomerUserFactory,
    UserFactory,
)


@pytest.mark.django_db
@ddt.ddt
class TestSignalsWithWaffleSwitch(TestCase):
    """
    Tests waffle switch for signal functions.
    """

    def setUp(self):
        super().setUp()
        self.course_id = CourseKey.from_string("course-v1:test-enterprise+test1+2029")
        self.user = UserFactory.create(email=TEST_USER_EMAIL)
        course_enrollment = CourseEnrollmentFactory.create(
            user=self.user,
            course_id=self.course_id,
            mode='verified'
        )
        self.enterprise_customer_user = EnterpriseCustomerUserFactory(user_id=self.user.id)
        self.enterprise_course_enrollment = EnterpriseCourseEnrollmentFactory(
            enterprise_customer_user=self.enterprise_customer_user,
            course_id=str(course_enrollment.course_id)
        )

    @override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=False)
    @patch("learner_pathway_progress.signals.update_learner_pathway_progress")
    def test_update_learner_pathway_progress_waffle_switch_off(self, mock_update_learner_pathway_progress):
        """
        Test update_learner_pathway_progress signals when waffle switch is off.
        """
        listen_for_course_grade_upgrade_in_learner_pathway(None, self.user.id, self.course_id)
        mock_update_learner_pathway_progress.assert_not_called()

    @override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=True)
    @patch("learner_pathway_progress.signals.update_learner_pathway_progress")
    def test_update_learner_pathway_progress_waffle_switch_on(self, mock_update_learner_pathway_progress):
        """
        Test update_learner_pathway_progress signals when waffle switch is on.
        """
        listen_for_course_grade_upgrade_in_learner_pathway(None, self.user.id, self.course_id)
        mock_update_learner_pathway_progress.assert_called()

    @override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=True)
    @patch("learner_pathway_progress.signals.get_learner_pathways_associated_with_course")
    def test_create_learner_enterprise_pathway_membership_for_user_waffle_switch_on(
        self,
        mock_learner_pathways_associated_with_course,
    ):
        """
        Test create_learner_enterprise_pathway_membership_for_user signals when waffle switch is on.
        """
        mock_learner_pathways_associated_with_course.return_value = [LEARNER_PATHWAY_UUID]
        create_learner_enterprise_pathway_membership_for_user(None, self.enterprise_course_enrollment, True)
        pathway_membership = LearnerEnterprisePathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID,
            enterprise_customer_uuid=self.enterprise_course_enrollment.enterprise_customer_user.enterprise_customer.uuid
        ).exists()
        self.assertTrue(pathway_membership)
        mock_learner_pathways_associated_with_course.assert_called()

    @override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=True)
    @patch("learner_pathway_progress.signals.get_learner_pathways_associated_with_course")
    def test_create_learner_enterprise_pathway_membership_for_user_and_course_not_linked_with_any_pathway(
        self,
        mock_learner_pathways_associated_with_course,
    ):
        """
        Test create_learner_enterprise_pathway_membership_for_user signals when waffle switch is on
        and course is not linked with any pathway.
        """
        mock_learner_pathways_associated_with_course.return_value = []
        create_learner_enterprise_pathway_membership_for_user(None, self.enterprise_course_enrollment, True)
        pathway_membership = LearnerEnterprisePathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID,
            enterprise_customer_uuid=self.enterprise_course_enrollment.enterprise_customer_user.enterprise_customer.uuid
        ).exists()
        self.assertFalse(pathway_membership)
        mock_learner_pathways_associated_with_course.assert_called()

    @override_waffle_switch(ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH, active=False)
    @patch("learner_pathway_progress.signals.get_learner_pathways_associated_with_course")
    def test_create_learner_enterprise_pathway_membership_for_user_waffle_switch_off(
        self,
        mock_learner_pathways_associated_with_course,
    ):
        """
        Test create_learner_enterprise_pathway_membership_for_user signals when waffle switch is off.
        """
        mock_learner_pathways_associated_with_course.return_value = [LEARNER_PATHWAY_UUID]
        create_learner_enterprise_pathway_membership_for_user(None, self.enterprise_course_enrollment, True)
        pathway_membership = LearnerEnterprisePathwayMembership.objects.filter(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_UUID,
            enterprise_customer_uuid=self.enterprise_course_enrollment.enterprise_customer_user.enterprise_customer.uuid
        ).exists()
        self.assertFalse(pathway_membership)
        mock_learner_pathways_associated_with_course.assert_not_called()
