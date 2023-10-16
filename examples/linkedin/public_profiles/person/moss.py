from bluemoss.utils import get_infix, get_endpoint
from bluemoss import extract, Ex, Root, Range
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_moss_list() -> list[Root]:
    return [
        Root(key="duration", path="span[contains(@class, 'date-range')]/span"),
        Root(key="_date_and_duration_text", path="span[contains(@class, 'date-range')]"),
        Root(key="_description_more_text", path="p[contains(@class, 'show-more-less-text__text--less')]"),
        Root(key="_description_less_text", path="p[contains(@class, 'show-more-less-text__text--more')]")
    ]


LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS: Root = Root(
    path="html",
    path_prefix="/",
    target=PersonProfile,
    nodes=[
        Root(
            path="meta[@property='og:url']",
            key="profile_endpoint",
            transform=get_endpoint,
            extract="content"
        ),
        Root(
            key="about",
            path="h2[contains(@class, 'section-title')]/..//p"
        ),
        Root(
            path_prefix=".",
            key="publications",
            nodes=[
                Root(
                    path="li[contains(@class, 'personal-project')]",
                    target=PublicationItem,
                    range=Range(0, None),
                    nodes=[
                        Root(key="date", path="time"),
                        Root(key="headline", path="h3/a"),
                        Root(
                            key="journal",
                            path="span[contains(@class, 'text-color-text-low-emphasis')]"
                        ),
                        Root(
                            path="a",
                            key="url",
                            extract=Ex.HREF_QUERY_PARAMS,
                            transform=lambda params: params.get("url", None)
                        ),
                    ]
                )
            ]
        ),
        Root(
            key="recommendations",
            path="section[contains(@class, 'recommendations')]",
            nodes=[
                Root(
                    path="div[contains(@class, 'endorsement-card')]",
                    target=RecommendationItem,
                    range=Range(0, None),
                    nodes=[
                        Root(key="text", path="p"),
                        Root(key="name", path="h3"),
                        Root(
                            path="a",
                            key="profile_endpoint",
                            extract=Ex.HREF_ENDPOINT
                        )
                    ]
                )
            ]
        ),
        Root(
            path_prefix=".",
            key="header",
            target=ProfileHeader,
            nodes=[
                Root(
                    key="name",
                    path="div[contains(@class, 'top-card-layout__entity-info')]//h1"
                ),
                Root(
                    key="headline",
                    path="h2[contains(@class, 'top-card-layout__headline')]"
                ),
                Root(
                    key="followers",
                    path="span[contains(text(), 'followers')]"
                ),
                Root(
                    path="head",
                    extract=Ex.TAG,
                    key="_location_text",
                    transform=lambda tag: get_infix(str(tag), 'addressLocality":"', '"')
                ),
            ]
        ),
        Root(
            key="education",
            path="section[contains(@class, 'education')]",
            nodes=[
                Root(
                    path="li",
                    target=EducationItem,
                    range=Range(0, None),
                    nodes=[
                         Root(key="institution", path="h3"),
                         Root(key="degree_info", path="h4"),
                         Root(
                             key="_description_text",
                             path="div[contains(@class, 'education__item--details')]/p"
                         ),
                         Root(
                             path="a",
                             extract=Ex.HREF_ENDPOINT,
                             key="school_profile_endpoint"
                         )
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Root(
            key="volunteering",
            path="section[contains(@class, 'volunteering')]",
            nodes=[
                Root(
                    path="li",
                    target=VolunteerItem,
                    range=Range(0, None),
                    nodes=[
                        Root(key="position", path="h3"),
                        Root(key="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Root(
            key="awards",
            path="section[contains(@class, 'awards')]",
            nodes=[
                Root(
                    path="li",
                    target=Award,
                    range=Range(0, None),
                    nodes=[
                        Root(key="title", path="h3"),
                        Root(key="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Root(
            key="certifications",
            path="section[contains(@class, 'certifications')]",
            nodes=[
                Root(
                    path="li",
                    range=Range(0, None),
                    target=Certification,
                    nodes=[
                        Root(key="name", path="h3"),
                        Root(key="institution", path="h4"),
                        Root(key="date_issued", path="time")
                    ]
                )
            ]
        ),
        Root(
            key="languages",
            path="section[contains(@class, 'languages')]",
            nodes=[
                Root(
                    path="li",
                    target=Language,
                    range=Range(0, None),
                    nodes=[
                        Root(key="lang", path="h3"),
                        Root(key="level", path="h4")
                    ]
                )
            ]
        ),
        Root(
            path="section[contains(@class, 'experience')]",
            target=Experience,
            key="experience",
            nodes=[
                Root(
                    range=Range(0, None),
                    target=ExperienceGroup,
                    key="_experience_groups",
                    path="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    nodes=[
                        Root(
                            key="duration",
                            path="p[contains(@class, 'experience-group-header__duration')]"
                        ),
                        Root(
                            key="company_name",
                            path="h4[contains(@class, 'experience-group-header__company')]"
                        ),
                        Root(
                            key="company_profile_endpoint",
                            extract=Ex.HREF_ENDPOINT,
                            path="a"
                        ),
                        Root(
                            path="li",
                            key="entries",
                            target=ExperienceGroupItem,
                            range=Range(0, None),
                            nodes=[
                                Root(key="position", path="h3"),
                                Root(
                                    key="location",
                                    path="p[contains(@class, 'experience-group-position__location')]"
                                )
                            ] + date_duration_description_moss_list()
                        )
                    ]
                ),
                Root(
                    range=Range(0, None),
                    target=ExperienceItem,
                    key="_experience_items",
                    path="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    nodes=[
                        Root(key="position", path="h3"),
                        Root(key="company_name", path="h4"),
                        Root(key="location", path="p[contains(@class, 'location')]"),
                        Root(
                            key="company_profile_endpoint",
                            extract=Ex.HREF_ENDPOINT,
                            path="a"
                        ),
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Root(
            key="people_also_viewed",
            path="section/h2[contains(text(), 'People also viewed')]/..",
            nodes=[
                Root(
                    path="li",
                    range=Range(0, None),
                    target=PeopleAlsoViewedItem,
                    nodes=[
                        Root(key="name", path="h3"),
                        Root(key="headline", path="p"),
                        Root(key="location", path="div[contains(@class, 'text-sm')]"),
                        Root(
                            key="profile_endpoint",
                            extract=Ex.HREF_ENDPOINT,
                            path="a"
                        )
                    ]
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    with open("./static/jeff.html", "r") as f:
        profile = extract(LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS, f.read())
        print(profile)
