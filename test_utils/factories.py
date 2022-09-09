"""
factories for learner_pathway_progress.
"""

import json
from datetime import datetime
from uuid import UUID, uuid4

import factory
from common.djangoapps.student.models import CourseEnrollment
from django.contrib.auth import get_user_model
from enterprise.models import EnterpriseCourseEnrollment, EnterpriseCustomer, EnterpriseCustomerUser
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytz import UTC

from learner_pathway_progress.models import LearnerEnterprisePathwayMembership, LearnerPathwayProgress

FAKER = FakerFactory.create()
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


class LearnerEnterprisePathwayMembershipFactory(DjangoModelFactory):
    """
    Factory class for generating LearnerEnterprisePathwayMembership
    """

    class Meta:
        model = LearnerEnterprisePathwayMembership

    user = factory.SubFactory(UserFactory)
    learner_pathway_uuid = factory.LazyFunction(uuid4)
    enterprise_customer_uuid = factory.LazyFunction(uuid4)


class EnterpriseCustomerFactory(factory.django.DjangoModelFactory):
    """
    EnterpriseCustomer factory.

    Creates an instance of EnterpriseCustomer with minimal boilerplate - uses this class' attributes as default
    parameters for EnterpriseCustomer constructor.
    """

    class Meta:
        """
        Meta for EnterpriseCustomerFactory.
        """

        model = EnterpriseCustomer

    uuid = factory.LazyAttribute(lambda x: UUID(FAKER.uuid4()))  # pylint: disable=no-member
    name = factory.LazyAttribute(lambda x: FAKER.company())  # pylint: disable=no-member
    slug = factory.LazyAttribute(lambda x: FAKER.slug())  # pylint: disable=no-member
    active = True


class EnterpriseCustomerUserFactory(factory.django.DjangoModelFactory):
    """
    EnterpriseCustomer factory.

    Creates an instance of EnterpriseCustomerUser with minimal boilerplate - uses this class' attributes as default
    parameters for EnterpriseCustomerUser constructor.
    """

    class Meta:
        """
        Meta for EnterpriseCustomerFactory.
        """

        model = EnterpriseCustomerUser

    enterprise_customer = factory.SubFactory(EnterpriseCustomerFactory)
    user_id = factory.LazyAttribute(lambda x: FAKER.pyint())  # pylint: disable=no-member


class EnterpriseCourseEnrollmentFactory(factory.django.DjangoModelFactory):
    """
    EnterpriseCourseEnrollment factory.

    Creates an instance of EnterpriseCourseEnrollment with minimal boilerplate.
    """

    class Meta:
        """
        Meta for EnterpriseCourseEnrollmentFactory.
        """

        model = EnterpriseCourseEnrollment

    course_id = factory.LazyAttribute(lambda x: FAKER.slug())  # pylint: disable=no-member
    enterprise_customer_user = factory.SubFactory(EnterpriseCustomerUserFactory)
