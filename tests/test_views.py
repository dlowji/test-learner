#!/usr/bin/env python
"""
Tests for `learner-pathway-progress` API Views.
"""

import json

import ddt
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from pytest import mark

from learner_pathway_progress.models import LearnerEnterprisePathwayMembership, LearnerPathwayProgress
from test_utils.constants import (
    ENTERPRISE_CUSTOMER_UUID,
    LEARNER_PATHWAY_A_UUID,
    LEARNER_PATHWAY_B_UUID,
    LEARNER_PATHWAY_C_UUID,
    LEARNER_PATHWAY_PROGRESS_DATA,
)

User = get_user_model()
USER_PASSWORD = 'QWERTY'


@mark.django_db
@ddt.ddt
class TestLearnerPathwayProgressViewSet(TestCase):
    """
    Tests for LearnerPathwayProgressViewSet.
    """
    def setUp(self):
        """
        Test set up
        """
        super().setUp()
        self.user = User.objects.create(username="rocky")
        self.second_user = User.objects.create(username="foggy")
        self.user.set_password(USER_PASSWORD)
        self.user.save()
        self.client = Client()

        # create learner pathway data
        self.learner_pathway_enterprise_membership = LearnerEnterprisePathwayMembership.objects.create(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_A_UUID,
            enterprise_customer_uuid=ENTERPRISE_CUSTOMER_UUID,
        )
        self.learner_pathway_progressA = LearnerPathwayProgress.objects.create(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_A_UUID,
            learner_pathway_progress=json.dumps(LEARNER_PATHWAY_PROGRESS_DATA[0]['learner_pathway_progress'])
        )
        self.learner_pathway_progressB = LearnerPathwayProgress.objects.create(
            user=self.user,
            learner_pathway_uuid=LEARNER_PATHWAY_B_UUID,
            learner_pathway_progress=json.dumps(LEARNER_PATHWAY_PROGRESS_DATA[1]['learner_pathway_progress'])
        )
        self.learner_pathway_progressC = LearnerPathwayProgress.objects.create(
            user=self.second_user,
            learner_pathway_uuid=LEARNER_PATHWAY_C_UUID,
            learner_pathway_progress=json.dumps(LEARNER_PATHWAY_PROGRESS_DATA[2]['learner_pathway_progress'])
        )
        self.client.login(username=self.user.username, password=USER_PASSWORD)

        self.view_url = '/v1/progress/'

    def _verify_learner_pathway_data(self, api_response, expected_data):
        """
        Verify that learner pathway progress api response matches the expected data.
        """
        response_data = api_response.json()
        assert len(response_data) == len(expected_data)

        for response_obj, expected_obj in zip(response_data, expected_data):
            # verify pathway progress data for current object
            response_obj = response_obj['learner_pathway_progress']
            expected_obj = expected_obj['learner_pathway_progress']
            assert response_obj['uuid'] == expected_obj['uuid']
            assert response_obj['title'] == expected_obj['title']
            assert response_obj['status'] == expected_obj['status']
            assert response_obj['overview'] == expected_obj['overview']
            # verify banner and card images
            assert response_obj['banner_image'] == expected_obj['banner_image']
            assert response_obj['card_image'] == expected_obj['card_image']

            assert len(response_obj['steps']) == len(expected_obj['steps'])

            # verify step data
            for i, step in enumerate(response_obj['steps']):
                assert step['min_requirement'] == expected_obj['steps'][i]['min_requirement']
                assert step['uuid'] == expected_obj['steps'][i]['uuid']
                assert step['status'] == expected_obj['steps'][i]['status']
                assert len(step['courses']) == len(expected_obj['steps'][i]['courses'])
                assert len(step['programs']) == len(expected_obj['steps'][i]['programs'])

    def test_learner_pathway_api(self):
        """
        Verify that learner pathway progress api returns the expected response.
        """
        api_response = self.client.get(self.view_url)
        self._verify_learner_pathway_data(api_response, LEARNER_PATHWAY_PROGRESS_DATA[0:2])

    def test_learner_pathway_api_filtering(self):
        """
        Verify that comma-delimited filtering on pathway uuids is enabled for learner pathway progress api .
        """
        url = f'{self.view_url}?uuid={LEARNER_PATHWAY_A_UUID}'
        api_response = self.client.get(url)
        data = api_response.json()
        assert len(data) == 1
        assert data[0]['learner_pathway_progress']['uuid'] == LEARNER_PATHWAY_A_UUID
        url = f'{self.view_url}?uuid={LEARNER_PATHWAY_A_UUID},{LEARNER_PATHWAY_B_UUID}'
        api_response = self.client.get(url)
        data = api_response.json()
        assert len(data) == 2
        assert data[0]['learner_pathway_progress']['uuid'] == LEARNER_PATHWAY_A_UUID
        assert data[1]['learner_pathway_progress']['uuid'] == LEARNER_PATHWAY_B_UUID

    def test_learner_pathway_progress_api_filtering_for_users(self):
        """
        verify that api only sends pathways data associated with currently logged in user.
        """
        url = f'{self.view_url}?uuid={LEARNER_PATHWAY_C_UUID}'
        api_response = self.client.get(url)
        data = api_response.json()
        assert len(data) == 0

    def test_learner_pathway_api_enterprise_filtering(self):
        """
        Verify that filtering on enterprise uuid is enabled for learner pathway progress api .
        """
        url = f'{self.view_url}?enterprise_uuid={ENTERPRISE_CUSTOMER_UUID}'
        api_response = self.client.get(url)
        data = api_response.json()
        assert len(data) == 1
        assert data[0]['learner_pathway_progress']['uuid'] == LEARNER_PATHWAY_A_UUID
        url = f'{self.view_url}?uuid={LEARNER_PATHWAY_A_UUID}&enterprise_uuid={ENTERPRISE_CUSTOMER_UUID}'
        api_response = self.client.get(url)
        data = api_response.json()
        assert len(data) == 1
        assert data[0]['learner_pathway_progress']['uuid'] == LEARNER_PATHWAY_A_UUID
