"""
Database models for learner_pathway_progress.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

User = get_user_model()


class LearnerPathwayMembership(TimeStampedModel):
    """
    Model to store membership of learner in learner pathway.

    .. no_pii:
    """

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    learner_pathway_uuid = models.UUIDField(
        editable=False,
        verbose_name=_('LEARNER_PATHWAY_UUID'),
        help_text=_("UUID of associated pathway"),
    )

    class Meta:
        """
        Learner pathway progress metadata.
        """

        unique_together = ('user', 'learner_pathway_uuid')

    def __str__(self):
        """
        Create a human-readable string representation of the object.
        """
        return f'User: {self.user}, Pathway UUID: {self.learner_pathway_uuid}'

    def __repr__(self):
        """
        Return string representation.
        """
        return f'<LearnerPathwayMembership user={self.user} pathway_uuid="{self.learner_pathway_uuid}">'
