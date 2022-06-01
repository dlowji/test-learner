#!/usr/bin/env python
"""
Tests for the `learner-pathway-progress` models module.
"""

from django.test import TestCase

from test_utils.factories import LearnerPathwayMembershipFactory


class LearnerPathwayMembershipTests(TestCase):
    """
    LearnerPathwayMembership model tests
    """
    def setUp(self):
        super().setUp()
        self.membership = LearnerPathwayMembershipFactory()

    def test_string_representation(self):
        """
        Test the string representation of the LearnerPathwayMembership model.
        """
        pathway_uuid = self.membership.learner_pathway_uuid
        user = self.membership.user
        expected_str = f'User: {user}, Pathway UUID: {pathway_uuid}'
        expected_repr = f'<LearnerPathwayMembership user={user} pathway_uuid="{pathway_uuid}">'
        assert expected_str == str(self.membership)
        assert expected_repr == repr(self.membership)
