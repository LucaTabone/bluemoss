from src.typings import Extract
from src.utils.text import get_infix
from src.utils.url import get_endpoint
from src.classes.recipe import Recipe
from src.extract import extract
from src.classes.range import Range
from examples.linkedin.public_profiles.person.person_classes \
    import (Language, Certification, Award, EducationItem, VolunteerItem, PersonProfile, ProfileHeader,
            Experience, PublicationItem, ExperienceGroup, ExperienceItem, ExperienceGroupItem,
            PeopleAlsoViewedItem, RecommendationItem)


def date_duration_description_recipes() -> list[Recipe]:
    return [
        Recipe(context="duration", path="span[contains(@class, 'date-range')]/span"),
        Recipe(context="_date_and_duration_text", path="span[contains(@class, 'date-range')]"),
        Recipe(context="_description_more_text", path="p[contains(@class, 'show-more-less-text__text--less')]"),
        Recipe(context="_description_less_text", path="p[contains(@class, 'show-more-less-text__text--more')]")
    ]


LINKEDIN_PUBLIC_PERSON_PROFILE_RECIPE: Recipe = Recipe(
    path="html",
    path_prefix="/",
    target=PersonProfile,
    children=[
        Recipe(
            path="meta[@property='og:url']",
            context="profile_endpoint",
            transform=get_endpoint,
            extract="content"
        ),
        Recipe(
            context="about",
            path="h2[contains(@class, 'section-title')]/..//p"
        ),
        Recipe(
            path_prefix=".",
            context="publications",
            children=[
                Recipe(
                    path="li[contains(@class, 'personal-project')]",
                    target=PublicationItem,
                    range=Range(0, None),
                    children=[
                        Recipe(context="date", path="time"),
                        Recipe(context="headline", path="h3/a"),
                        Recipe(
                            context="journal",
                            path="span[contains(@class, 'text-color-text-low-emphasis')]"
                        ),
                        Recipe(
                            path="a",
                            context="url",
                            extract=Extract.HREF_QUERY_PARAMS,
                            transform=lambda params: params.get("url", None)
                        ),
                    ]
                )
            ]
        ),
        Recipe(
            context="recommendations",
            path="section[contains(@class, 'recommendations')]",
            children=[
                Recipe(
                    path="div[contains(@class, 'endorsement-card')]",
                    target=RecommendationItem,
                    range=Range(0, None),
                    children=[
                        Recipe(context="text", path="p"),
                        Recipe(context="name", path="h3"),
                        Recipe(
                            path="a",
                            context="profile_endpoint",
                            extract=Extract.HREF_ENDPOINT
                        )
                    ]
                )
            ]
        ),
        Recipe(
            path_prefix=".",
            context="header",
            target=ProfileHeader,
            children=[
                Recipe(
                    context="name",
                    path="div[contains(@class, 'top-card-layout__entity-info')]//h1"
                ),
                Recipe(
                    context="headline",
                    path="h2[contains(@class, 'top-card-layout__headline')]"
                ),
                Recipe(
                    context="followers",
                    path="span[contains(text(), 'followers')]"
                ),
                Recipe(
                    path="head",
                    extract=Extract.TAG,
                    context="_location_text",
                    transform=lambda tag: get_infix(str(tag), 'addressLocality":"', '"')
                ),
            ]
        ),
        Recipe(
            context="education",
            path="section[contains(@class, 'education')]",
            children=[
                Recipe(
                    path="li",
                    target=EducationItem,
                    range=Range(0, None),
                    children=[
                         Recipe(context="institution", path="h3"),
                         Recipe(context="degree_info", path="h4"),
                         Recipe(
                             context="_description_text",
                             path="div[contains(@class, 'education__item--details')]/p"
                         ),
                         Recipe(
                             path="a",
                             extract=Extract.HREF_ENDPOINT,
                             context="school_profile_endpoint"
                         )
                    ] + date_duration_description_recipes()
                )
            ]
        ),
        Recipe(
            context="volunteering",
            path="section[contains(@class, 'volunteering')]",
            children=[
                Recipe(
                    path="li",
                    target=VolunteerItem,
                    range=Range(0, None),
                    children=[
                        Recipe(context="position", path="h3"),
                        Recipe(context="institution", path="h4")
                    ] + date_duration_description_recipes()
                )
            ]
        ),
        Recipe(
            context="awards",
            path="section[contains(@class, 'awards')]",
            children=[
                Recipe(
                    path="li",
                    target=Award,
                    range=Range(0, None),
                    children=[
                        Recipe(context="title", path="h3"),
                        Recipe(context="institution", path="h4")
                    ] + date_duration_description_recipes()
                )
            ]
        ),
        Recipe(
            context="certifications",
            path="section[contains(@class, 'certifications')]",
            children=[
                Recipe(
                    path="li",
                    range=Range(0, None),
                    target=Certification,
                    children=[
                        Recipe(context="name", path="h3"),
                        Recipe(context="institution", path="h4"),
                        Recipe(context="date_issued", path="time")
                    ]
                )
            ]
        ),
        Recipe(
            context="languages",
            path="section[contains(@class, 'languages')]",
            children=[
                Recipe(
                    path="li",
                    target=Language,
                    range=Range(0, None),
                    children=[
                        Recipe(context="lang", path="h3"),
                        Recipe(context="level", path="h4")
                    ]
                )
            ]
        ),
        Recipe(
            path="section[contains(@class, 'experience')]",
            target=Experience,
            context="experience",
            children=[
                Recipe(
                    range=Range(0, None),
                    target=ExperienceGroup,
                    context="_experience_groups",
                    path="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    children=[
                        Recipe(
                            context="duration",
                            path="p[contains(@class, 'experience-group-header__duration')]"
                        ),
                        Recipe(
                            context="company_name",
                            path="h4[contains(@class, 'experience-group-header__company')]"
                        ),
                        Recipe(
                            context="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                        Recipe(
                            path="li",
                            context="entries",
                            target=ExperienceGroupItem,
                            range=Range(0, None),
                            children=[
                                Recipe(context="position", path="h3"),
                                Recipe(
                                    context="location",
                                    path="p[contains(@class, 'experience-group-position__location')]"
                                )
                            ] + date_duration_description_recipes()
                        )
                    ]
                ),
                Recipe(
                    range=Range(0, None),
                    target=ExperienceItem,
                    context="_experience_items",
                    path="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    children=[
                        Recipe(context="position", path="h3"),
                        Recipe(context="company_name", path="h4"),
                        Recipe(context="location", path="p[contains(@class, 'location')]"),
                        Recipe(
                            context="company_profile_endpoint",
                            extract=Extract.HREF_ENDPOINT,
                            path="a"
                        ),
                    ] + date_duration_description_recipes()
                )
            ]
        ),
        Recipe(
            context="people_also_viewed",
            path="section/h2[contains(text(), 'People also viewed')]/..",
            children=[
                Recipe(
                    path="li",
                    range=Range(0, None),
                    target=PeopleAlsoViewedItem,
                    children=[
                        Recipe(context="name", path="h3"),
                        Recipe(context="headline", path="p"),
                        Recipe(context="location", path="div[contains(@class, 'text-sm')]"),
                        Recipe(
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
    profile = extract(LINKEDIN_PUBLIC_PERSON_PROFILE_RECIPE, f.read())
    print(profile)
