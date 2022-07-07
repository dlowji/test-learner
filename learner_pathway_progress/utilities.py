"""A lightweight interface to pathway progress helper functions."""
import json
from logging import getLogger
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from enterprise.models import EnterpriseCourseEnrollment
from opaque_keys.edx.locator import CourseLocator
from openedx.core.djangoapps.catalog.utils import check_catalog_integration_and_get_user, get_catalog_api_base_url
from openedx.core.djangoapps.catalog.utils import get_catalog_api_client as create_catalog_api_client
from requests.exceptions import HTTPError

from learner_pathway_progress.constants import CHUNK_SIZE, PATHWAY_LOGS_IDENTIFIER
from learner_pathway_progress.models import LearnerPathwayMembership, LearnerPathwayProgress

log = getLogger(__name__)

User = get_user_model()


def get_learner_pathways_associated_with_course(user, course_key):
    """Return the pathway associated with course."""
    client = create_catalog_api_client(user)  # pylint: disable=assignment-from-none
    learner_pathways_with_course_url = urljoin(f"{get_catalog_api_base_url()}/", "learner-pathway/uuids")
    params = {'course_keys': course_key}
    learner_pathways_with_course = None
    try:
        response = client.get(learner_pathways_with_course_url, params=params)
        response.raise_for_status()
        learner_pathways_with_course = response.json()
    except HTTPError as err:
        log.exception(
            f"{PATHWAY_LOGS_IDENTIFIER}: Encountered HTTPError {err} while getting pathways"
            f" linked with course: {course_key} from discovery. "
        )
    return learner_pathways_with_course


def get_pathway_snapshot(user, pathway_uuid):
    """Return the pathway snapshot."""
    learner_pathway_url = urljoin(
        f"{get_catalog_api_base_url()}/", f"learner-pathway/{pathway_uuid}/snapshot/"
    )
    result = None
    try:
        client = create_catalog_api_client(user)  # pylint: disable=assignment-from-none
        response = client.get(learner_pathway_url)
        response.raise_for_status()
        result = response.json()
    except HTTPError as err:
        log.exception(
            f"{PATHWAY_LOGS_IDENTIFIER}: Encountered HTTPError {err} while getting snapshot of pathway: {pathway_uuid}"
            f" from discovery."
        )

    return result


def update_learner_pathway_progress(user_id, course_id):
    """Update progress of all pathways linked with this course_id."""
    pathways_linked_with_course = None
    course_key = course_id
    user = User.objects.filter(id=user_id).first()
    if isinstance(course_id, CourseLocator):
        course_key = str(course_id)
        log.info(
            f"{PATHWAY_LOGS_IDENTIFIER}: Update pathways associated with course: {course_key} for user {user_id}"
        )
        pathways_linked_with_course = get_learner_pathways_associated_with_course(user, course_key)
    else:
        log.info(
            f"{PATHWAY_LOGS_IDENTIFIER}: course_key: {course_key} not valid for user {user_id} to"
            f" update pathways associated with course "
        )
    if pathways_linked_with_course:
        for learner_pathway_uuid in pathways_linked_with_course:
            pathway_snapshot = get_pathway_snapshot(user, learner_pathway_uuid)
            if pathway_snapshot:
                LearnerPathwayMembership.objects.get_or_create(
                    user=user,
                    learner_pathway_uuid=learner_pathway_uuid
                )
                pathway_progress, _ = LearnerPathwayProgress.objects.get_or_create(
                    user=user,
                    learner_pathway_uuid=learner_pathway_uuid,
                )
                pathway_progress.learner_pathway_progress = json.dumps(pathway_snapshot)
                pathway_progress.save()
                pathway_progress.update_pathway_progress()
                log.info(
                    f"{PATHWAY_LOGS_IDENTIFIER}: Pathway:{learner_pathway_uuid} updated associated "
                    f"with course: {course_key}"
                )


def get_all_learner_pathways(user_id):
    """Return the all pathways."""
    user = User.objects.filter(id=user_id).first()
    client = create_catalog_api_client(user)  # pylint: disable=assignment-from-none
    learner_pathways_url = urljoin(f"{get_catalog_api_base_url()}/", "learner-pathway/")
    learner_pathways = None
    try:
        response = client.get(learner_pathways_url)
        response.raise_for_status()
        learner_pathways = response.json()
        learner_pathways_count = len(learner_pathways['results'])
        log.info(
            f"{PATHWAY_LOGS_IDENTIFIER}: Total Learner Pathways are : {learner_pathways_count}"
        )
    except HTTPError as err:
        log.exception(
            f"{PATHWAY_LOGS_IDENTIFIER}: Encountered HTTPError {err} while getting all pathways from discovery. "
        )
    return learner_pathways


def back_fill_learner_pathway_membership_and_progress(pathways):
    """Update the pathway progress and create membership for user if not already exist."""
    enrollments_count = EnterpriseCourseEnrollment.objects.all().count()
    log.info(
        f"{PATHWAY_LOGS_IDENTIFIER}: Total Enterprise Course Enrollment Count: {enrollments_count}"
    )
    queryset = EnterpriseCourseEnrollment.objects.all().select_related('enterprise_customer_user').only(
        'course_id',
        'enterprise_customer_user__user_id',
    )
    paginator = Paginator(queryset, CHUNK_SIZE)
    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        log.info(
            f"{PATHWAY_LOGS_IDENTIFIER}: Enterprise Course Enrollment records accessed with page: {page}"
        )
        for pathway in pathways:
            pathway_course_runs = pathway['pathway-course-runs']
            for enrollment in page.object_list:
                user = User.objects.filter(id=enrollment.enterprise_customer_user.user_id).first()
                pathway_progress_exist = LearnerPathwayProgress.objects.filter(
                    user=user,
                    learner_pathway_uuid=pathway['pathway-uuid'],
                ).exists()
                if not pathway_progress_exist and enrollment.course_id in pathway_course_runs:

                    LearnerPathwayMembership.objects.get_or_create(
                        user=user,
                        learner_pathway_uuid=pathway['pathway-uuid']
                    )
                    pathway_progress = LearnerPathwayProgress.objects.create(
                        user=user,
                        learner_pathway_uuid=pathway['pathway-uuid'],
                    )
                    pathway_progress.learner_pathway_progress = json.dumps(pathway['snapshot'])
                    pathway_progress.save()
                    pathway_progress.update_pathway_progress()

                    log.info(
                        f"{PATHWAY_LOGS_IDENTIFIER}: Pathway Progress and Membership created for user:{user.email}"
                        f" with pathway:{pathway['pathway-uuid']}"
                    )


def get_pathway_course_run_keys(step_courses, step_programs, pathway_course_runs):
    """Return all the course run keys linked with pathway step."""
    for course in step_courses:
        course_runs = course.get('course_runs') or []
        for course_run in course_runs:
            pathway_course_runs.append(course_run['key'])
    for program in step_programs:
        program_courses = program.get('courses') or []
        for program_course in program_courses:
            program_course_runs = program_course.get('course_runs') or []
            for program_course_run in program_course_runs:
                pathway_course_runs.append(program_course_run['key'])


def update_progress_all_pathways():
    """Update progress of all pathways."""
    user, _ = check_catalog_integration_and_get_user(
        error_message_field='Call to fetch pathways from pathway progress management command'
    )
    if user:
        learner_pathways = get_all_learner_pathways(user.id)
        pathway_data = {"data": []}
        pathway_snapshots = learner_pathways.get('results') or []
        for pathway_snapshot in pathway_snapshots:
            pathway_details = {}
            pathway_course_runs = []
            pathway_steps = pathway_snapshot.get('steps') or []
            for step in pathway_steps:
                step_courses = step.get('courses') or []
                step_programs = step.get('programs') or []

                get_pathway_course_run_keys(
                    step_courses,
                    step_programs,
                    pathway_course_runs,
                )
            pathway_details['pathway-uuid'] = pathway_snapshot['uuid']
            pathway_details['pathway-course-runs'] = pathway_course_runs
            pathway_details['snapshot'] = pathway_snapshot
            pathway_data["data"].append(pathway_details)
        back_fill_learner_pathway_membership_and_progress(pathway_data['data'])
    else:
        log.warning(
            f"{PATHWAY_LOGS_IDENTIFIER}: check_catalog_integration_and_get_user not returning user"
            f" to update learner_pathway_progress"
        )
