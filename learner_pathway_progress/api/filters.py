"""
Filters for the Learner Pathway Progress APIs.
"""

from django_filters import rest_framework as filters

from learner_pathway_progress.models import LearnerPathwayProgress


class PathwayProgressUUIDFilter(filters.FilterSet):
    """
    Filter pathways progress by uuid. Supports filtering by comma-delimited list of uuids.
    """
    uuid = filters.CharFilter(method='filter_by_uuid')

    class Meta:
        model = LearnerPathwayProgress
        fields = ['learner_pathway_uuid']

    def filter_by_uuid(self, queryset, name, value):  # pylint: disable=unused-argument
        uuid_values = value.strip().split(',')
        return queryset.filter(learner_pathway_uuid__in=uuid_values)
