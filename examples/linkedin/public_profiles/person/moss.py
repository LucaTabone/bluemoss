from bluemoss.utils import get_infix, get_endpoint
from bluemoss import extract, Extract, Moss, Range
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_moss_list() -> list[Moss]:
    return [
        Moss(key="duration", path="span[contains(@class, 'date-range')]/span"),
        Moss(key="_date_and_duration_text", path="span[contains(@class, 'date-range')]"),
        Moss(key="_description_more_text", path="p[contains(@class, 'show-more-less-text__text--less')]"),
        Moss(key="_description_less_text", path="p[contains(@class, 'show-more-less-text__text--more')]")
    ]


LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS: Moss = Moss(
    path="html",
    path_prefix="/",
    target=PersonProfile,
    children=[
        Moss(
            path="meta[@property='og:url']",
            key="profile_endpoint",
            transform=get_endpoint,
            extract="content"
        ),
        Moss(
            key="about",
            path="h2[contains(@class, 'section-title')]/..//p"
        ),
        Moss(
            path_prefix=".",
            key="publications",
            children=[
                Moss(
                    path="li[contains(@class, 'personal-project')]",
                    target=PublicationItem,
                    range=Range(0, None),
                    children=[
                        Moss(key="date", path="time"),
                        Moss(key="headline", path="h3/a"),
                        Moss(
                            key="journal",
                            path="span[contains(@class, 'text-color-text-low-emphasis')]"
                        ),
                        Moss(
                            path="a",
                            key="url",
                            extract=Extract.HREF_QUERY_PARAMS,
                            transform=lambda params: params.get("url", None)
                        ),
                    ]
                )
            ]
        ),
        Moss(
            key="recommendations",
            path="section[contains(@class, 'recommendations')]",
            children=[
                Moss(
                    path="div[contains(@class, 'endorsement-card')]",
                    target=RecommendationItem,
                    range=Range(0, None),
                    children=[
                        Moss(key="text", path="p"),
                        Moss(key="name", path="h3"),
                        Moss(
                            path="a",
                            key="profile_endpoint",
                            extract=Extract.HREF_ENDPOINT
                        )
                    ]
                )
            ]
        ),
        Moss(
            path_prefix=".",
            key="header",
            target=ProfileHeader,
            children=[
                Moss(
                    key="name",
                    path="div[contains(@class, 'top-card-layout__entity-info')]//h1"
                ),
                Moss(
                    key="headline",
                    path="h2[contains(@class, 'top-card-layout__headline')]"
                ),
                Moss(
                    key="followers",
                    path="span[contains(text(), 'followers')]"
                ),
                Moss(
                    path="head",
                    extract=Extract.TAG,
                    key="_location_text",
                    transform=lambda tag: get_infix(str(tag), 'addressLocality":"', '"')
                ),
            ]
        ),
        Moss(
            key="education",
            path="section[contains(@class, 'education')]",
            children=[
                Moss(
                    path="li",
                    target=EducationItem,
                    range=Range(0, None),
                    children=[
                         Moss(key="institution", path="h3"),
                         Moss(key="degree_info", path="h4"),
                         Moss(
                             key="_description_text",
                             path="div[contains(@class, 'education__item--details')]/p"
                         ),
                         Moss(
                             path="a",
                             extract=Extract.HREF_ENDPOINT,
                             key="school_profile_endpoint"
                         )
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            key="volunteering",
            path="section[contains(@class, 'volunteering')]",
            children=[
                Moss(
                    path="li",
                    target=VolunteerItem,
                    range=Range(0, None),
                    children=[
                        Moss(key="position", path="h3"),
                        Moss(key="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            key="awards",
            path="section[contains(@class, 'awards')]",
            children=[
                Moss(
                    path="li",
                    target=Award,
                    range=Range(0, None),
                    children=[
                        Moss(key="title", path="h3"),
                        Moss(key="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            key="certifications",
            path="section[contains(@class, 'certifications')]",
            children=[
                Moss(
                    path="li",
                    range=Range(0, None),
                    target=Certification,
                    children=[
                        Moss(key="name", path="h3"),
                        Moss(key="institution", path="h4"),
                        Moss(key="date_issued", path="time")
                    ]
                )
            ]
        ),
        Moss(
            key="languages",
            path="section[contains(@class, 'languages')]",
            children=[
                Moss(
                    path="li",
                    target=Language,
                    range=Range(0, None),
                    children=[
                        Moss(key="lang", path="h3"),
                        Moss(key="level", path="h4")
                    ]
                )
            ]
        ),
        Moss(
            path="section[contains(@class, 'experience')]",
            target=Experience,
            key="experience",
            children=[
                Moss(
                    range=Range(0, None),
                    target=ExperienceGroup,
                    key="_experience_groups",
                    path="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    children=[
                        Moss(
                            key="duration",
                            path="p[contains(@class, 'experience-group-header__duration')]"
                        ),
                        Moss(
                            key="company_name",
                            path="h4[contains(@class, 'experience-group-header__company')]"
                        ),
                        Moss(
                            key="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                        Moss(
                            path="li",
                            key="entries",
                            target=ExperienceGroupItem,
                            range=Range(0, None),
                            children=[
                                Moss(key="position", path="h3"),
                                Moss(
                                    key="location",
                                    path="p[contains(@class, 'experience-group-position__location')]"
                                )
                            ] + date_duration_description_moss_list()
                        )
                    ]
                ),
                Moss(
                    range=Range(0, None),
                    target=ExperienceItem,
                    key="_experience_items",
                    path="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    children=[
                        Moss(key="position", path="h3"),
                        Moss(key="company_name", path="h4"),
                        Moss(key="location", path="p[contains(@class, 'location')]"),
                        Moss(
                            key="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            key="people_also_viewed",
            path="section/h2[contains(text(), 'People also viewed')]/..",
            children=[
                Moss(
                    path="li",
                    range=Range(0, None),
                    target=PeopleAlsoViewedItem,
                    children=[
                        Moss(key="name", path="h3"),
                        Moss(key="headline", path="p"),
                        Moss(key="location", path="div[contains(@class, 'text-sm')]"),
                        Moss(
                            key="profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
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
