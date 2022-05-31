"""
Tests for the `learner-pathway-progress` apps module.
"""

from edx_django_utils.plugins.constants import PluginURLs

from learner_pathway_progress.apps import LearnerPathwayProgressConfig


class TestLearnerPathwayProgressConfig:
    """
    Test learner-pathway-progress app config.
    """

    def test_config(self):
        """
        Test required attributes for configuration are present.
        """
        assert LearnerPathwayProgressConfig.name == 'learner_pathway_progress'
        assert hasattr(LearnerPathwayProgressConfig, 'plugin_app')
        assert PluginURLs.CONFIG in LearnerPathwayProgressConfig.plugin_app
