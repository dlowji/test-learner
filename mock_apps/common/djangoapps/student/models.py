"""
Database models for bulk_grades.
"""

from django.contrib.auth import get_user_model
from django.db import models


class CourseEnrollment(models.Model):
    """
    Represents a Student's Enrollment record for a single Course. You should
    generally not manipulate CourseEnrollment objects directly, but use the
    classmethods provided to enroll, unenroll, or check on the enrollment status
    of a given student.

    We're starting to consolidate course enrollment logic in this class, but
    more should be brought in (such as checking against CourseEnrollmentAllowed,
    checking course dates, user permissions, etc.) This logic is currently
    scattered across our views.

    .. no_pii:
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    course_id = models.CharField(max_length=255, db_index=True)

    created = models.DateTimeField(auto_now_add=True, null=True, db_index=True)

    # If is_active is False, then the student is not considered to be enrolled
    # in the course (is_enrolled() will return False)
    is_active = models.BooleanField(default=True)

    # Represents the modes that are possible. We'll update this later with a
    # list of possible values.
    mode = models.CharField(default='audit', max_length=100)

    class Meta:
        app_label = "student"
        unique_together = (('user', 'course_id'),)
        ordering = ('user', 'course_id')

    @classmethod
    def get_enrollment(cls, user, course_key, select_related=None):
        """Returns a CourseEnrollment object.

        Args:
            user (User): The user associated with the enrollment.
            course_key (CourseKey): The key of the course associated with the enrollment.

        Returns:
            Course enrollment object or None
        """
        assert user
        try:
            query = cls.objects
            enrollment = query.get(
                user=user,
                course_id=course_key
            )
            return enrollment
        except cls.DoesNotExist:
            return None
