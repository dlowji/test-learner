"""
learner_pathway_progress Django application initialization.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from edx_django_utils.plugins.constants import PluginURLs


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
                PluginURLs.REGEX: '^learner_pathway_progress/',
                PluginURLs.RELATIVE_PATH: 'urls',
            }
        },
    }
