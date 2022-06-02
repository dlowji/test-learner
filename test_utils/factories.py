"""
factories for learner_pathway_progress.
"""

import json
from datetime import datetime
from uuid import uuid4

import factory
from common.djangoapps.student.models import CourseEnrollment
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from pytz import UTC

from learner_pathway_progress.models import LearnerPathwayMembership, LearnerPathwayProgress

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """
    Factory class for generating a User
    """

    class Meta:
        model = User
        django_get_or_create = ('email', 'username')

    _DEFAULT_PASSWORD = 'test'

    username = factory.Sequence('robot{}'.format)
    email = factory.Sequence('robot+test+{}@edx.org'.format)
    password = factory.PostGenerationMethodCall('set_password', _DEFAULT_PASSWORD)
    first_name = factory.Sequence('Robot{}'.format)
    last_name = 'Test'
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = datetime(2012, 1, 1, tzinfo=UTC)
    date_joined = datetime(2011, 1, 1, tzinfo=UTC)


class CourseEnrollmentFactory(DjangoModelFactory):
    """
    Factory class for generating CourseEnrollment
    """

    class Meta:
        model = CourseEnrollment

    user = factory.SubFactory(UserFactory)


class LearnerPathwayProgressFactory(DjangoModelFactory):
    """
    Factory class for generating LearnerPathwayProgress
    """

    class Meta:
        model = LearnerPathwayProgress

    user = factory.SubFactory(UserFactory)
    learner_pathway_uuid = factory.LazyFunction(uuid4)

    @factory.lazy_attribute
    def learner_pathway_progress(self):
        return json.dumps({
            'uuid': str(self.learner_pathway_uuid),
            'status': 'active',
            'steps': [
                {
                    'uuid': '9d91b42a-f3e4-461a-b9e1-e53a4fc927ed',
                    'min_requirement': 2,
                    'courses': [
                        {
                            'key': 'AA+AA101',
                            'course_runs': [
                                {
                                    'key': 'course-v1:test-enterprise+test1+2020'
                                },
                                {
                                    'key': 'course-v1:test-enterprise+test1+2021'
                                }
                            ],
                        },
                        {
                            'key': 'AA+AA102',
                            'course_runs': [
                                {
                                    'key': 'course-v1:test-enterprise+test1+2022'
                                },
                                {
                                    'key': 'course-v1:test-enterprise+test1+2023'
                                }
                            ],
                        }
                    ],
                    'programs': [
                        {
                            'uuid': '1f301a72-f344-4a31-9e9a-e0b04d8d86b2'
                        }
                    ]
                },
                {
                    'uuid': '9d91b42a-f3e4-461a-b9e1-e53a4fc927ef',
                    'min_requirement': 2,
                    'courses': [
                        {
                            'key': 'AA+AA103',
                            'course_runs': [
                                {
                                    'key': 'course-v1:test-enterprise+test1+2024',
                                },
                                {
                                    'key': 'course-v1:test-enterprise+test1+2025'
                                }
                            ],
                        },
                        {
                            'key': 'AA+AA104',
                            'course_runs': [
                                {
                                    'key': 'course-v1:test-enterprise+test1+2026'
                                },
                                {
                                    'key': 'course-v1:test-enterprise+test1+2027'
                                }
                            ],
                        }
                    ],
                    'programs': [
                        {
                            'uuid': '1f301a72-f344-4a31-9e9a-e0b04d8d86b3'
                        }
                    ]
                }
            ]
        })


class LearnerPathwayMembershipFactory(DjangoModelFactory):
    """
    Factory class for generating LearnerPathwayMembership
    """
    class Meta:
        model = LearnerPathwayMembership

    user = factory.SubFactory(UserFactory)
    learner_pathway_uuid = factory.LazyFunction(uuid4)
