from bluemoss.utils import get_infix, get_endpoint
from bluemoss import extract, Extract, Moss, Range
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_moss_list() -> list[Moss]:
    return [
        Moss(context="duration", path="span[contains(@class, 'date-range')]/span"),
        Moss(context="_date_and_duration_text", path="span[contains(@class, 'date-range')]"),
        Moss(context="_description_more_text", path="p[contains(@class, 'show-more-less-text__text--less')]"),
        Moss(context="_description_less_text", path="p[contains(@class, 'show-more-less-text__text--more')]")
    ]


LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS: Moss = Moss(
    path="html",
    path_prefix="/",
    target=PersonProfile,
    children=[
        Moss(
            path="meta[@property='og:url']",
            context="profile_endpoint",
            transform=get_endpoint,
            extract="content"
        ),
        Moss(
            context="about",
            path="h2[contains(@class, 'section-title')]/..//p"
        ),
        Moss(
            path_prefix=".",
            context="publications",
            children=[
                Moss(
                    path="li[contains(@class, 'personal-project')]",
                    target=PublicationItem,
                    range=Range(0, None),
                    children=[
                        Moss(context="date", path="time"),
                        Moss(context="headline", path="h3/a"),
                        Moss(
                            context="journal",
                            path="span[contains(@class, 'text-color-text-low-emphasis')]"
                        ),
                        Moss(
                            path="a",
                            context="url",
                            extract=Extract.HREF_QUERY_PARAMS,
                            transform=lambda params: params.get("url", None)
                        ),
                    ]
                )
            ]
        ),
        Moss(
            context="recommendations",
            path="section[contains(@class, 'recommendations')]",
            children=[
                Moss(
                    path="div[contains(@class, 'endorsement-card')]",
                    target=RecommendationItem,
                    range=Range(0, None),
                    children=[
                        Moss(context="text", path="p"),
                        Moss(context="name", path="h3"),
                        Moss(
                            path="a",
                            context="profile_endpoint",
                            extract=Extract.HREF_ENDPOINT
                        )
                    ]
                )
            ]
        ),
        Moss(
            path_prefix=".",
            context="header",
            target=ProfileHeader,
            children=[
                Moss(
                    context="name",
                    path="div[contains(@class, 'top-card-layout__entity-info')]//h1"
                ),
                Moss(
                    context="headline",
                    path="h2[contains(@class, 'top-card-layout__headline')]"
                ),
                Moss(
                    context="followers",
                    path="span[contains(text(), 'followers')]"
                ),
                Moss(
                    path="head",
                    extract=Extract.TAG,
                    context="_location_text",
                    transform=lambda tag: get_infix(str(tag), 'addressLocality":"', '"')
                ),
            ]
        ),
        Moss(
            context="education",
            path="section[contains(@class, 'education')]",
            children=[
                Moss(
                    path="li",
                    target=EducationItem,
                    range=Range(0, None),
                    children=[
                         Moss(context="institution", path="h3"),
                         Moss(context="degree_info", path="h4"),
                         Moss(
                             context="_description_text",
                             path="div[contains(@class, 'education__item--details')]/p"
                         ),
                         Moss(
                             path="a",
                             extract=Extract.HREF_ENDPOINT,
                             context="school_profile_endpoint"
                         )
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            context="volunteering",
            path="section[contains(@class, 'volunteering')]",
            children=[
                Moss(
                    path="li",
                    target=VolunteerItem,
                    range=Range(0, None),
                    children=[
                        Moss(context="position", path="h3"),
                        Moss(context="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            context="awards",
            path="section[contains(@class, 'awards')]",
            children=[
                Moss(
                    path="li",
                    target=Award,
                    range=Range(0, None),
                    children=[
                        Moss(context="title", path="h3"),
                        Moss(context="institution", path="h4")
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            context="certifications",
            path="section[contains(@class, 'certifications')]",
            children=[
                Moss(
                    path="li",
                    range=Range(0, None),
                    target=Certification,
                    children=[
                        Moss(context="name", path="h3"),
                        Moss(context="institution", path="h4"),
                        Moss(context="date_issued", path="time")
                    ]
                )
            ]
        ),
        Moss(
            context="languages",
            path="section[contains(@class, 'languages')]",
            children=[
                Moss(
                    path="li",
                    target=Language,
                    range=Range(0, None),
                    children=[
                        Moss(context="lang", path="h3"),
                        Moss(context="level", path="h4")
                    ]
                )
            ]
        ),
        Moss(
            path="section[contains(@class, 'experience')]",
            target=Experience,
            context="experience",
            children=[
                Moss(
                    range=Range(0, None),
                    target=ExperienceGroup,
                    context="_experience_groups",
                    path="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    children=[
                        Moss(
                            context="duration",
                            path="p[contains(@class, 'experience-group-header__duration')]"
                        ),
                        Moss(
                            context="company_name",
                            path="h4[contains(@class, 'experience-group-header__company')]"
                        ),
                        Moss(
                            context="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                        Moss(
                            path="li",
                            context="entries",
                            target=ExperienceGroupItem,
                            range=Range(0, None),
                            children=[
                                Moss(context="position", path="h3"),
                                Moss(
                                    context="location",
                                    path="p[contains(@class, 'experience-group-position__location')]"
                                )
                            ] + date_duration_description_moss_list()
                        )
                    ]
                ),
                Moss(
                    range=Range(0, None),
                    target=ExperienceItem,
                    context="_experience_items",
                    path="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    children=[
                        Moss(context="position", path="h3"),
                        Moss(context="company_name", path="h4"),
                        Moss(context="location", path="p[contains(@class, 'location')]"),
                        Moss(
                            context="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Moss(
            context="people_also_viewed",
            path="section/h2[contains(text(), 'People also viewed')]/..",
            children=[
                Moss(
                    path="li",
                    range=Range(0, None),
                    target=PeopleAlsoViewedItem,
                    children=[
                        Moss(context="name", path="h3"),
                        Moss(context="headline", path="p"),
                        Moss(context="location", path="div[contains(@class, 'text-sm')]"),
                        Moss(
                            context="profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        )
                    ]
                )
            ]
        )
    ]
)


with open("./static/jeff.html", "r") as f:
    profile = extract(LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS, f.read())
    print(profile)
