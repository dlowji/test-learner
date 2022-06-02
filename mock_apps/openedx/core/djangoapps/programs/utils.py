"""Helper functions for working with Programs."""

import logging

log = logging.getLogger(__name__)


class ProgramProgressMeter:
    """Utility for gauging a user's progress towards program completion.

    Arguments:
        user (User): The user for which to find programs.

    Keyword Arguments:
        enrollments (list): List of the user's enrollments.
        uuid (str): UUID identifying a specific program. If provided, the meter
            will only inspect this one program, not all programs the user may be
            engaged with.
    """
    def __init__(self, site, user, enrollments=None, uuid=None, mobile_only=False, include_course_entitlements=True):
        pass

    def progress(self, programs=None, count_only=True):
        """Gauge a user's progress towards program completion.

        Keyword Arguments:
            programs (list): Specific list of programs to check the user's progress
                against. If left unspecified, self.engaged_programs will be used.

            count_only (bool): Whether or not to return counts of completed, in
                progress, and unstarted courses instead of serialized representations
                of the courses.

        Returns:
            list of dict, each containing information about a user's progress
                towards completing a program.
        """

        return []
