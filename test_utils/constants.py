"""
Constants for the learner pathway application tests
"""

import json

TEST_USER_EMAIL = 'test@example.com'
LEARNER_PATHWAY_UUID = '1f301a72-f344-4a31-9e9a-e0b04d8d86b1'
LEARNER_PATHWAY_UUID2 = '1f301a72-f344-4a31-9e9a-e0b04d8d86b2'
LEARNER_PATHWAY_UUID3 = '1f301a72-f344-4a31-9e9a-e0b04d8d86b3'
LEARNER_PATHWAY_UUID4 = '1f301a72-f344-4a31-9e9a-e0b04d8d86b3'
ENTERPRISE_CUSTOMER_UUID = '1f301a72-f344-4a31-9e9a-e0b04d8d86b6'
ENTERPRISE_CUSTOMER_UUID2 = '1f301a72-f344-4a31-9e9a-e0b04d8d86c1'


class LearnerPathwayProgressOutputs:
    """
    Model tests constants for the learner pathway progress model.

    .. no_pii:
    """
    all_pathways_from_discovery = {
        "results": [
            {
                "id": 1,
                "uuid": LEARNER_PATHWAY_UUID,
                "status": "active",
                "steps": [
                    {
                        "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ed",
                        "min_requirement": 2,
                        "courses": [
                            {
                                "key": "AA+AA101",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-enterprise+test1+2020"
                                    },
                                    {
                                        "key": "course-v1:test-enterprise+test1+2021"
                                    }
                                ]
                            },
                            {
                                "key": "AA+AA102",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-enterprise+test1+2022"
                                    },
                                    {
                                        "key": "course-v1:test-enterprise+test1+2023"
                                    }
                                ]
                            }
                        ],
                        "programs": [
                            {
                                "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2"
                            }
                        ]
                    },
                ]
            },

            {
                "id": 2,
                "uuid": LEARNER_PATHWAY_UUID2,
                "status": "active",
                "steps": [
                    {
                        "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927e3",
                        "min_requirement": 2,
                        "courses": [
                            {
                                "key": "AA+AA105",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-enterprise+test1+2024"
                                    },
                                    {
                                        "key": "course-v1:test-enterprise+test1+2025"
                                    }
                                ]
                            },
                            {
                                "key": "AA+AA106",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-enterprise+test1+2026"
                                    },
                                ]
                            }
                        ],
                        "programs": [
                            {
                                "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2"
                            }
                        ]
                    },
                ]
            },
            {
                "id": 3,
                "uuid": LEARNER_PATHWAY_UUID3,
                "status": "active",
                "steps": [
                    {
                        "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927h3",
                        "min_requirement": 2,
                        "programs": [
                            {
                                "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86d2"
                            }
                        ]
                    },
                ]
            },

            {
                "id": 4,
                "uuid": LEARNER_PATHWAY_UUID4,
                "status": "active",
                "steps": [
                    {
                        "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927e3",
                        "min_requirement": 2,
                        "courses": [
                            {
                                "key": "AA+AA105",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-enterprise+test1+2078"
                                    },
                                    {
                                        "key": "course-v1:test-enterprise+test1+2045"
                                    }
                                ]
                            },
                        ],
                        "programs": [
                            {
                                "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2"
                            }
                        ]
                    },
                ]
            },
        ]
    }
    single_pathway_from_discovery = {
        "uuid": LEARNER_PATHWAY_UUID,
        "status": "active",
        "steps": [
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ed",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA101",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2020"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2021"
                            }
                        ]
                    },
                    {
                        "key": "AA+AA102",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2022"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2023"
                            }
                        ]
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2",
                        "title": "edX Demonstration Program",
                        "content_type": "program",
                        "courses": [
                            {
                                "key": "edX+DemoX",
                                "course_runs": [
                                    {
                                        "key": "course-v1:edX+DemoX+Demo_Course"
                                    }
                                ]
                            },
                            {
                                "key": "test-course-generator+6724",
                                "course_runs": []
                            },
                            {
                                "key": "test-course-generator+8344",
                                "course_runs": [
                                    {
                                        "key": "course-v1:test-course-generator+8344+1"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ef",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA103",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2024"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2025"
                            }
                        ]
                    },
                    {
                        "key": "AA+AA104",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2026"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2027"
                            }
                        ]
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b3"
                    }
                ]
            }
        ]
    }
    snapshot_from_discovery = json.dumps({
        "uuid": LEARNER_PATHWAY_UUID,
        "status": "active",
        "steps": [
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ed",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA101",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2020"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2021"
                            }
                        ]
                    },
                    {
                        "key": "AA+AA102",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2022"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2023"
                            }
                        ]
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2"
                    }
                ]
            },
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ef",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA103",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2024"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2025"
                            }
                        ]
                    },
                    {
                        "key": "AA+AA104",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2026"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2027"
                            }
                        ]
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b3"
                    }
                ]
            }
        ]
    })
    updated_learner_progress1 = json.dumps({
        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b1",
        "status": "active",
        "steps": [
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ed",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA101",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2020"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2021"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]",
                    },
                    {
                        "key": "AA+AA102",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2022"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2023"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]",
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2",
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "status": 0.0
            },
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ef",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA103",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2024"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2025"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]"
                    },
                    {
                        "key": "AA+AA104",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2026"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2027"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]"
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b3",
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "status": 0.0
            }
        ]
    })
    updated_learner_progress2 = json.dumps({
        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b1",
        "status": "active",
        "steps": [
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ed",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA101",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2020"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2021"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]"
                    },
                    {
                        "key": "AA+AA102",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2022"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2023"
                            }
                        ],
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b2",
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "status": 0.0
            },
            {
                "uuid": "9d91b42a-f3e4-461a-b9e1-e53a4fc927ef",
                "min_requirement": 2,
                "courses": [
                    {
                        "key": "AA+AA103",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2024"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2025"
                            }
                        ],
                        "status": "IN_PROGRESS",
                        "enterprises": "[]"
                    },
                    {
                        "key": "AA+AA104",
                        "course_runs": [
                            {
                                "key": "course-v1:test-enterprise+test1+2026"
                            },
                            {
                                "key": "course-v1:test-enterprise+test1+2027"
                            }
                        ],
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "programs": [
                    {
                        "uuid": "1f301a72-f344-4a31-9e9a-e0b04d8d86b3",
                        "status": "NOT_STARTED",
                        "enterprises": "[]"
                    }
                ],
                "status": 0.0
            }
        ]
    })

LEARNER_PATHWAY_PROGRESS_DATA = [
    {
        "learner_pathway_progress": {
            "id": 118,
            "uuid": "0a017cbe-0f1c-4e5f-9095-2101823fac93",
            "title": "test 3",
            "status": "active",
            "banner_image": "example.com/banner_image",
            "card_image": 'example.com',
            "overview": "",
            "steps": [
                {
                    "uuid": "a230a2f4-d84b-41d0-9756-6bf56d9b51c3",
                    "min_requirement": 1,
                    "courses": [
                        {
                            "key": "",
                            "course_runs": [],
                            "title": "test course 2",
                            "short_description": "",
                            "card_image_url": 'example.com',
                            "content_type": "course",
                            "status": "NOT_STARTED"
                        }
                    ],
                    "programs": [
                        {
                            "uuid": "919e68dd-8147-482f-8666-72240380c251",
                            "title": "edX Demonstration Program",
                            "short_description": "",
                            "card_image_url": "example.com/course_image.jpg",
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
                    "uuid": "ea54f31a-be7c-4cfc-8d1f-23a4704c9eaf",
                    "min_requirement": 1,
                    "courses": [
                        {
                            "key": "",
                            "course_runs": [],
                            "title": "test course 2",
                            "short_description": "",
                            "card_image_url": 'example.com',
                            "content_type": "course",
                            "status": "NOT_STARTED"
                        }
                    ],
                    "programs": [],
                    "status": 0.0
                }
            ]
        }
    },
    {
        "learner_pathway_progress": {
            "id": 117,
            "uuid": "29efa34c-60c6-4791-88c0-ab3b5fbd7503",
            "title": "test 1",
            "status": "active",
            "banner_image": 'example.com',
            "card_image": 'example.com',
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
                            "card_image_url": "example.com/course_image.jpg",
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
                            "card_image_url": 'example.com',
                            "content_type": "course",
                            "status": "NOT_STARTED"
                        }
                    ],
                    "programs": [
                        {
                            "uuid": "919e68dd-8147-482f-8666-72240380c251",
                            "title": "edX Demonstration Program",
                            "short_description": "",
                            "card_image_url": "example.com/course_image.jpg",
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
                            "short_description": "Lorem ipsum",
                            "card_image_url": 'example.com',
                            "content_type": "course",
                            "status": "IN_PROGRESS"
                        }
                    ],
                    "programs": [],
                    "status": 0.0
                }
            ]
        }
    },
    {
        "learner_pathway_progress": {
            "id": 119,
            "uuid": "52970da6-888d-4867-baf3-d970759fb11f",
            "title": "test 2",
            "status": "active",
            "banner_image": "example.com/dude.png",
            "card_image": "example.com/dude.jpeg",
            "overview": "Lorem ipsum",
            "steps": [
                {
                    "uuid": "ae44cc82-1413-434a-9005-14e69fafd840",
                    "min_requirement": 1,
                    "courses": [
                        {
                            "key": "",
                            "course_runs": [],
                            "title": "test course 2",
                            "short_description": "",
                            "card_image_url": 'example.com',
                            "content_type": "course",
                            "status": "NOT_STARTED"
                        }
                    ],
                    "programs": [
                        {
                            "uuid": "919e68dd-8147-482f-8666-72240380c251",
                            "title": "edX Demonstration Program",
                            "short_description": "",
                            "card_image_url": "example.com/course_image.jpg",
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
                    "uuid": "d792fd72-151c-4a2a-8fef-01ca562c4180",
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
                            "short_description": "Lorem ipsum",
                            "card_image_url": 'example.com',
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

LEARNER_PATHWAY_A_UUID = LEARNER_PATHWAY_PROGRESS_DATA[0]['learner_pathway_progress']['uuid']
LEARNER_PATHWAY_B_UUID = LEARNER_PATHWAY_PROGRESS_DATA[1]['learner_pathway_progress']['uuid']
LEARNER_PATHWAY_C_UUID = LEARNER_PATHWAY_PROGRESS_DATA[2]['learner_pathway_progress']['uuid']
