"""
Module for learner_pathway_progress related signals.
"""
from logging import getLogger

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from learner_pathway_progress import waffle
from learner_pathway_progress.models import LearnerPathwayMembership
from learner_pathway_progress.utilities import (
    get_learner_pathways_associated_with_course,
    update_learner_pathway_progress,
)

try:
    from enterprise.models import EnterpriseCourseEnrollment
except ImportError:
    EnterpriseCourseEnrollment = None

log = getLogger(__name__)

User = get_user_model()


def listen_for_course_grade_upgrade_in_learner_pathway(sender, user_id, course_id,
                                                       **kwargs):  # pylint: disable=unused-argument
    """
    Listen for a signal indicating that the user has passed course grade.

    Call update_learner_pathway_progress function to update learner course grade in pathway.
    """
    if waffle.ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH.is_enabled():
        update_learner_pathway_progress(user_id, course_id)


def create_learner_pathway_membership_for_user(sender, instance, created, **kwargs):   # pylint: disable=unused-argument
    """
    Watches for post_save signal for creates on the EnterpriseCourseEnrollment table.

    Generate a Learner Pathway Membership for the User
    """
    if waffle.ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH.is_enabled() and created:
        user_id = instance.enterprise_customer_user.user_id
        user = User.objects.filter(id=user_id).first()

        learner_pathways = get_learner_pathways_associated_with_course(user, instance.course_id)
        if learner_pathways:
            for pathway in learner_pathways:
                _, newly_created = LearnerPathwayMembership.objects.get_or_create(
                    user=user,
                    learner_pathway_uuid=pathway
                )
                membership_status = 'updated'
                if newly_created:
                    membership_status = 'created'
                log.info(
                    f"Membership for pathway:{pathway} {membership_status} for user:{user.email}"
                    f" with course: {instance.course_id}"
                )


if EnterpriseCourseEnrollment is not None:
    post_save.connect(create_learner_pathway_membership_for_user, sender=EnterpriseCourseEnrollment)
