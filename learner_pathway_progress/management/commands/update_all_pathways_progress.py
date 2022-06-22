"""
Management command to update learner progress in pathway.
"""
from textwrap import dedent

from django.core.management import BaseCommand

from learner_pathway_progress.utilities import update_progress_all_pathways


class Command(BaseCommand):
    """
    Command to update learner progress in pathway.

    Update pathway progress for all enterprise learners who have any course enrollments.

    Examples:

        ./manage.py lms update_all_pathways_progress
    """
    help = dedent(__doc__)

    def handle(self, *args, **options):
        """
        Handle the pathway progress update for enterprise learners.
        """
        update_progress_all_pathways()
