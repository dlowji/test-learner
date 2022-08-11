"""
learner_pathway_progress Django application initialization.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from edx_django_utils.plugins.constants import PluginSignals, PluginURLs


class LearnerPathwayProgressConfig(AppConfig):
    """
    Configuration for the learner_pathway_progress Django application.
    """

    name = 'learner_pathway_progress'
    label = 'learner_pathway_progress'
    verbose_name = _("Learner Pathway Progress")
    plugin_app = {
        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {
            'lms.djangoapp': {
                PluginURLs.NAMESPACE: 'learner_pathway_progress',
                PluginURLs.APP_NAME: 'learner_pathway_progress',
                PluginURLs.REGEX: '^api/learner-pathway-progress/',
                PluginURLs.RELATIVE_PATH: 'api.urls',
            }
        },
        # Configuration setting for Plugin Signals for this app.
        PluginSignals.CONFIG: {
            'lms.djangoapp': {
                PluginSignals.RECEIVERS: [
                    {
                        PluginSignals.SIGNAL_PATH: 'lms.djangoapps.grades.signals.signals'
                                                   '.COURSE_GRADE_PASSED_UPDATE_IN_LEARNER_PATHWAY',
                        PluginSignals.RECEIVER_FUNC_NAME: 'listen_for_course_grade_upgrade_in_learner_pathway',
                    },
                    {
                        PluginSignals.SENDER_PATH: 'enterprise.models.EnterpriseCourseEnrollment',
                        PluginSignals.SIGNAL_PATH: 'django.db.models.signals.post_save',
                        PluginSignals.RECEIVER_FUNC_NAME: 'create_learner_pathway_membership_for_user',
                    },
                ],
            },
        },
    }
