""" API v1 views """

from django_filters.rest_framework import DjangoFilterBackend
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from learner_pathway_progress.api.filters import PathwayProgressUUIDFilter
from learner_pathway_progress.api.serializers import LearnerPathwayProgressSerializer
from learner_pathway_progress.models import LearnerPathwayProgress


class LearnerPathwayProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """
        **Use Case**

            * Get a detailed list of all Pathways or single pathway which user have in progress.

        **Example Request**

            GET /api/learner-pathway-progress/v1/progress/
            GET /api/learner-pathway-progress/v1/progress/{learner_pathway_uuid}/
            GET /api/learner-pathway-progress/v1/progress/?uuid={learner_pathway_uuid}
            GET /api/learner-pathway-progress/v1/progress/?uuid={learner_pathway_uuid1},{learner_pathway_uuid2}

        **GET Parameters**

            A GET request may include the following parameters if wants to fetch data of particular pathways.

            * learner_pathway_uuid: UUID of a LearnerPathway.

        **Example GET Response**

            [
                {
                "learner_pathway_progress": {
                    "id": 117,
                    "uuid": "29efa34c-60c6-4791-88c0-ab3b5fbd7503",
                    "title": "test 1",
                    "status": "active",
                    "banner_image": null,
                    "card_image": null,
                    "overview": "",
                    "steps": [
                        {
                            "uuid": "7d95ae15-821e-447a-be2e-9fbfa4d777b4",
                            "min_requirement": 2,
                            "courses": [],
                            "programs": [
                                {
                                    "uuid": "919e68dd-8147-482f-8666-72240380c251",
                                    "title": "edX Demonstration Program",
                                    "short_description": "",
                                    "card_image_url": "http://edx.com/logos",
                                    "content_type": "program",
                                    "courses": [
                                        {
                                            "key": "edX+DemoX",
                                            "course_runs": [
                                                {
                                                    "key": "course-v1:edX+DemoX+Demo_Course"
                                                }
                                            ]
                                        }
                                    ],
                                    "status": "NOT_STARTED"
                                }
                            ],
                            "status": 0.0
                        },
                        {
                            "uuid": "768e4081-901d-4913-8e7c-434ad25636ac",
                            "min_requirement": 2,
                            "courses": [
                                {
                                    "key": "",
                                    "course_runs": [],
                                    "title": "test course 2",
                                    "short_description": "",
                                    "card_image_url": null,
                                    "content_type": "course",
                                    "status": "NOT_STARTED"
                                }
                            ],
                            "programs": [
                                {
                                    "uuid": "919e68dd-8147-482f-8666-72240380c251",
                                    "title": "edX Demonstration Program",
                                    "short_description": "",
                                    "card_image_url": "http://edx.com/logo",
                                    "content_type": "program",
                                    "courses": [
                                        {
                                            "key": "edX+DemoX",
                                            "course_runs": [
                                                {
                                                    "key": "course-v1:edX+DemoX+Demo_Course"
                                                }
                                            ]
                                        }
                                    ],
                                    "status": "NOT_STARTED"
                                }
                            ],
                            "status": 0.0
                        },
                        {
                            "uuid": "ced544b3-c1e8-47b5-b7fa-76ef75c3fcc2",
                            "min_requirement": 1,
                            "courses": [
                                {
                                    "key": "edX+DemoX",
                                    "course_runs": [
                                        {
                                            "key": "course-v1:edX+DemoX+Demo_Course"
                                        }
                                    ],
                                    "title": "Demonstration Course",
                                    "short_description": "dummy desc",
                                    "card_image_url": null,
                                    "content_type": "course",
                                    "status": "IN_PROGRESS"
                                }
                            ],
                            "programs": [],
                            "status": 0.0
                        }
                        ]
                    }
                }
            ]

    """

    authentication_classes = (JwtAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'learner_pathway_uuid'
    lookup_value_regex = '[0-9a-f-]+'
    filter_backends = (DjangoFilterBackend,)
    serializer_class = LearnerPathwayProgressSerializer
    filterset_class = PathwayProgressUUIDFilter

    def get_queryset(self):
        user = self.request.user
        return LearnerPathwayProgress.objects.filter(user=user)
