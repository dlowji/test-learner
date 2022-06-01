"""
Models used for robust grading.

Robust grading allows student scores to be saved per-subsection independent
of any changes that may occur to the course after the score is achieved.
We also persist students' course-level grades, and update them whenever
a student's score or the course grading policy changes. As they are
persisted, course grades are also immune to changes in course content.
"""

import logging

from django.db import models
from model_utils.models import TimeStampedModel
from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField

log = logging.getLogger(__name__)


class PersistentCourseGrade(TimeStampedModel):
    """
    A django model tracking persistent course grades.

    .. no_pii:
    """

    class Meta:
        app_label = "grades"
        # Indices:
        # (course_id, user_id) for individual grades
        # (course_id) for instructors to see all course grades, implicitly created via the unique_together constraint
        # (user_id) for course dashboard; explicitly declared as an index below
        # (passed_timestamp, course_id) for tracking when users first earned a passing grade.
        # (modified): find all the grades updated within a certain timespan
        # (modified, course_id): find all the grades updated within a certain timespan for a course
        unique_together = [
            ('course_id', 'user_id'),
        ]
        index_together = [
            ('passed_timestamp', 'course_id'),
            ('modified', 'course_id')
        ]

    user_id = models.IntegerField(blank=False, db_index=True)
    course_id = CourseKeyField(blank=False, max_length=255)

    # Information about the course grade itself
    percent_grade = models.FloatField(blank=False)
    letter_grade = models.CharField('Letter grade for course', blank=False, max_length=255)

    # Information related to course completion
    passed_timestamp = models.DateTimeField('Date learner earned a passing grade', blank=True, null=True)

    _CACHE_NAMESPACE = "grades.models.PersistentCourseGrade"
