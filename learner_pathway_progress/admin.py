"""
Admin interface for learner_pathway_progress.
"""
from django.contrib import admin

from learner_pathway_progress.models import LearnerEnterprisePathwayMembership, LearnerPathwayProgress


class LearnerEnterprisePathwayMembershipAdmin(admin.ModelAdmin):
    """
    Admin for LearnerEnterprisePathwayMembership Model.
    """

    raw_id_fields = ('user', )
    list_display = ('user', 'learner_pathway_uuid', 'enterprise_customer_uuid', 'created')

    class Meta:
        """
        Metadata for LearnerEnterprisePathwayMembership model admin.
        """

        model = LearnerEnterprisePathwayMembership


class LearnerPathwayProgressAdmin(admin.ModelAdmin):
    """
    Admin for LearnerPathwayProgress Model.
    """

    raw_id_fields = ('user', )
    list_display = ('user', 'learner_pathway_uuid', 'created')

    class Meta:
        """
        Metadata for LearnerPathwayProgress model admin.
        """

        model = LearnerPathwayProgress

    def has_add_permission(self, request):
        """
        Admin should not able to add a new progress instance.
        """
        return False


admin.site.register(LearnerEnterprisePathwayMembership, LearnerEnterprisePathwayMembershipAdmin)
admin.site.register(LearnerPathwayProgress, LearnerPathwayProgressAdmin)
