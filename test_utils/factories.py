"""
factories for learner_pathway_progress.
"""
from datetime import datetime
from uuid import uuid4

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from pytz import UTC

from learner_pathway_progress.models import LearnerPathwayMembership

User = get_user_model()

class UserFactory(DjangoModelFactory):  # lint-amnesty, pylint: disable=missing-class-docstring
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


class LearnerPathwayMembershipFactory(DjangoModelFactory):
    """
    LearnerPathwayMembership factory
    """
    class Meta:
        model = LearnerPathwayMembership

    user = factory.SubFactory(UserFactory)
    learner_pathway_uuid = factory.LazyFunction(uuid4)
