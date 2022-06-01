"""
Admin interface for learner_pathway_progress.
"""
from django.contrib import admin

from learner_pathway_progress.models import LearnerPathwayMembership


@admin.register(LearnerPathwayMembership)
class LearnerPathwayMembershipAdmin(admin.ModelAdmin):
    """
    Admin for LearnerPathwayMembership Model.
    """

    raw_id_fields = ('user', )
    list_display = ('user', 'learner_pathway_uuid', 'created')

    class Meta:
        """
        Metadata for LearnerPathwayMembership model admin.
        """

        model = LearnerPathwayMembership
