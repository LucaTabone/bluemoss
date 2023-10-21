from bluemoss import extract, Ex, Root, Node
from bluemoss.utils import get_infix, get_endpoint
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_moss_list() -> list[Node]:
    return [
        Node(key="duration", path="span[contains(@class, 'date-range')]/span"),
        Node(key="_date_and_duration_text", path="span[contains(@class, 'date-range')]"),
        Node(key="_description_more_text", path="p[contains(@class, 'show-more-less-text__text--less')]"),
        Node(key="_description_less_text", path="p[contains(@class, 'show-more-less-text__text--more')]")
    ]


LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS: Root = Root(
    path="html",
    target=PersonProfile,
    nodes=[
        Node(
            path="meta[@property='og:url']",
            key="profile_endpoint",
            transform=get_endpoint,
            extract="content"
        ),
        Node(
            key="about",
            path="h2[contains(@class, 'section-title')]/..//p"
        ),
        Node(
            key="publications",
            path="li[contains(@class, 'personal-project')]",
            target=PublicationItem,
            filter=None,
            nodes=[
                Node(key="date", path="time"),
                Node(key="headline", path="h3/a"),
                Node(
                    key="journal",
                    path="span[contains(@class, 'text-color-text-low-emphasis')]"
                ),
                Node(
                    path="a",
                    key="url",
                    extract=Ex.HREF_QUERY_PARAMS,
                    transform=lambda params: params.get("url", None)
                ),
            ]
        ),
        Node(
            key="recommendations",
            path="section[contains(@class, 'recommendations')]//div[contains(@class, 'endorsement-card')]",
            target=RecommendationItem,
            filter=None,
            nodes=[
                Node("p", key="text"),
                Node("h3", key="name"),
                Node(
                    "a",
                    key="profile_endpoint",
                    extract=Ex.HREF_ENDPOINT
                )
            ]
        ),
        Node(
            key="header",
            target=ProfileHeader,
            nodes=[
                Node(
                    key="name",
                    path="div[contains(@class, 'top-card-layout__entity-info')]//h1"
                ),
                Node(
                    key="headline",
                    path="h2[contains(@class, 'top-card-layout__headline')]"
                ),
                Node(
                    key="followers",
                    path="span[contains(text(), 'followers')]"
                ),
                Node(
                    path="head",
                    extract=Ex.TAG,
                    key="_location_text",
                    transform=lambda tag: get_infix(str(tag), 'addressLocality":"', '"')
                ),
            ]
        ),
        Node(
            key="education",
            path="section[contains(@class, 'education')]//li",
            target=EducationItem,
            filter=None,
            nodes=[
                      Node(key="institution", path="h3"),
                      Node(key="degree_info", path="h4"),
                      Node(
                          key="_description_text",
                          path="div[contains(@class, 'education__item--details')]/p"
                      ),
                      Node(
                          path="a",
                          extract=Ex.HREF_ENDPOINT,
                          key="school_profile_endpoint"
                      )
                  ] + date_duration_description_moss_list()
        ),
        Node(
            key="volunteering",
            path="section[contains(@class, 'volunteering')]//li",
            target=VolunteerItem,
            filter=None,
            nodes=[
                Node(key="position", path="h3"),
                Node(key="institution", path="h4")
            ] + date_duration_description_moss_list()
        ),
        Node(
            key="awards",
            path="section[contains(@class, 'awards')]//li",
            target=Award,
            filter=None,
            nodes=[
                Node(key="title", path="h3"),
                Node(key="institution", path="h4")
            ] + date_duration_description_moss_list()
        ),
        Node(
            key="certifications",
            path="section[contains(@class, 'certifications')]//li",
            filter=None,
            target=Certification,
            nodes=[
                Node(key="name", path="h3"),
                Node(key="institution", path="h4"),
                Node(key="date_issued", path="time")
            ]
        ),
        Node(
            key="languages",
            path="section[contains(@class, 'languages')]//li",
            target=Language,
            filter=None,
            nodes=[
                Node(key="lang", path="h3"),
                Node(key="level", path="h4")
            ]
        ),
        Node(
            path="section[contains(@class, 'experience')]",
            target=Experience,
            key="experience",
            nodes=[
                Node(
                    filter=None,
                    target=ExperienceGroup,
                    key="_experience_groups",
                    path="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    nodes=[
                        Node(
                            key="duration",
                            path="p[contains(@class, 'experience-group-header__duration')]"
                        ),
                        Node(
                            key="company_name",
                            path="h4[contains(@class, 'experience-group-header__company')]"
                        ),
                        Node(
                            key="company_profile_endpoint",
                            extract=Ex.HREF_ENDPOINT,
                            path="a"
                        ),
                        Node(
                            path="li",
                            key="entries",
                            target=ExperienceGroupItem,
                            filter=None,
                            nodes=[
                                Node(key="position", path="h3"),
                                Node(
                                    key="location",
                                    path="p[contains(@class, 'experience-group-position__location')]"
                                )
                            ] + date_duration_description_moss_list()
                        )
                    ]
                ),
                Node(
                    filter=None,
                    target=ExperienceItem,
                    key="_experience_items",
                    path="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    nodes=[
                        Node(key="position", path="h3"),
                        Node(key="company_name", path="h4"),
                        Node(key="location", path="p[contains(@class, 'location')]"),
                        Node(
                            key="company_profile_endpoint",
                            extract=Ex.HREF_ENDPOINT,
                            path="a"
                        ),
                    ] + date_duration_description_moss_list()
                )
            ]
        ),
        Node(
            key="people_also_viewed",
            path="section/h2[contains(text(), 'People also viewed')]/..//li",
            filter=None,
            target=PeopleAlsoViewedItem,
            nodes=[
                Node(key="name", path="h3"),
                Node(key="headline", path="p"),
                Node(key="location", path="div[contains(@class, 'text-sm')]"),
                Node(
                    key="profile_endpoint",
                    extract=Ex.HREF_ENDPOINT,
                    path="a"
                )
            ]
        )
    ]
)


if __name__ == '__main__':
    with open("./static/adam.html", "r") as f:
        profile = extract(LINKEDIN_PUBLIC_PERSON_PROFILE_MOSS, f.read())
        print(profile)
