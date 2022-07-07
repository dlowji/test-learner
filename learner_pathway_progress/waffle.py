"""This module contains various configuration settings via waffle switches for the pathway progress app."""
from edx_toggles.toggles import WaffleSwitch

# The switch and namespace names variables are preserved for backward compatibility
WAFFLE_NAMESPACE = "learner_pathway_progress"
ENABLE_PATHWAY_PROGRESS_UPDATE = "enable_pathway_progress_update"  # pylint: disable=annotation-missing-token
# .. toggle_name: learner_pathway_progress.enable_pathway_progress_update
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: Indicates whether to update learner pathway progress when course grade is changed.
# .. toggle_use_cases: open_edx
ENABLE_PATHWAY_PROGRESS_UPDATE_SWITCH = WaffleSwitch(
    f"{WAFFLE_NAMESPACE}.{ENABLE_PATHWAY_PROGRESS_UPDATE}",
    module_name=__name__,
)
