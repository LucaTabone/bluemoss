from bluemoss import scrape, Ex, Node
from bluemoss.utils import get_infix, get_endpoint
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_nodes() -> list[Node]:
    return [
        Node(key='duration', xpath="span[contains(@class, 'date-range')]/span"),
        Node(
            key='_date_and_duration_text',
            xpath="span[contains(@class, 'date-range')]",
            transform=lambda text: text.replace('\n', '') if text else None
        ),
        Node(
            key='_description_more_text',
            xpath="p[contains(@class, 'show-more-less-text__text--less')]",
        ),
        Node(
            key='_description_less_text',
            xpath="p[contains(@class, 'show-more-less-text__text--more')]",
        ),
    ]


PERSON_PROFILE_NODE: Node = Node(
    target=PersonProfile,
    nodes=[
        Node(
            xpath="meta[@property='og:url']",
            key='profile_endpoint',
            transform=get_endpoint,
            extract='content',
        ),
        Node(
            key='about',
            xpath="h2[contains(@class, 'top-card-layout__headline')]",
        ),
        Node(
            key='publications',
            xpath="li[contains(@class, 'personal-project')]",
            target=PublicationItem,
            filter=None,
            nodes=[
                Node(key='date', xpath='time'),
                Node(key='headline', xpath='h3/a'),
                Node(
                    key='journal',
                    xpath="span[contains(@class, 'text-color-text-low-emphasis')]",
                ),
                Node(
                    xpath='a',
                    key='url',
                    extract=Ex.HREF_QUERY_PARAMS,
                    transform=lambda params: params.get('url', None),
                ),
            ],
        ),
        Node(
            key='recommendations',
            xpath="section[contains(@class, 'recommendations')]//div[contains(@class, 'endorsement-card')]",
            target=RecommendationItem,
            filter=None,
            nodes=[
                Node('p', key='text'),
                Node('h3', key='name'),
                Node('a', key='profile_endpoint', extract=Ex.HREF_ENDPOINT),
            ],
        ),
        Node(
            key='header',
            target=ProfileHeader,
            nodes=[
                Node(
                    key='name',
                    xpath="div[contains(@class, 'top-card-layout__entity-info')]//h1",
                ),
                Node(
                    key='headline',
                    xpath="h2[contains(@class, 'top-card-layout__headline')]",
                ),
                Node(
                    key='followers',
                    xpath="span[contains(text(), 'followers')]",
                ),
                Node(
                    xpath="script[contains(@type, 'application/ld+json')]",
                    extract=Ex.BS4_TAG,
                    key='location',
                    transform=lambda tag: get_infix(
                        str(tag), 'addressLocality":"', '"'
                    ),
                ),
            ],
        ),
        Node(
            key='education',
            xpath="section[contains(@class, 'education')]//li",
            target=EducationItem,
            filter=None,
            nodes=[
                Node(
                    key='institution',
                    xpath='h3'
                ),
                Node(
                    key='degree_info',
                    xpath='h4',
                    transform=lambda text: text.replace('\n', '') if text else None
                ),
                Node(
                    key='_description_text',
                    xpath="div[contains(@class, 'education__item--details')]/p",
                ),
                Node(
                    xpath='a',
                    extract=Ex.HREF_ENDPOINT,
                    key='school_profile_endpoint',
                ),
            ]
            + date_duration_description_nodes(),
        ),
        Node(
            key='volunteering',
            xpath="section[contains(@class, 'volunteering')]//li",
            target=VolunteerItem,
            filter=None,
            nodes=[
                Node(key='position', xpath='h3'),
                Node(key='institution', xpath='h4'),
            ]
            + date_duration_description_nodes(),
        ),
        Node(
            key='awards',
            xpath="section[contains(@class, 'awards')]//li",
            target=Award,
            filter=None,
            nodes=[
                Node(key='title', xpath='h3'),
                Node(key='institution', xpath='h4'),
            ]
            + date_duration_description_nodes(),
        ),
        Node(
            key='certifications',
            xpath="section[contains(@class, 'certifications')]//li",
            filter=None,
            target=Certification,
            nodes=[
                Node(key='name', xpath='h3'),
                Node(key='institution', xpath='h4'),
                Node(key='date_issued', xpath='time'),
            ],
        ),
        Node(
            key='languages',
            xpath="section[contains(@class, 'languages')]//li",
            target=Language,
            filter=None,
            nodes=[
                Node(key='lang', xpath='h3'),
                Node(key='level', xpath='h4'),
            ],
        ),
        Node(
            xpath="section[contains(@class, 'experience')]",
            target=Experience,
            key='experience',
            nodes=[
                Node(
                    filter=None,
                    target=ExperienceGroup,
                    key='_experience_groups',
                    xpath="li[contains(@class, 'experience-group') and contains(@class, 'experience-item')]",
                    nodes=[
                        Node(
                            key='duration',
                            xpath="p[contains(@class, 'experience-group-header__duration')]",
                        ),
                        Node(
                            key='company_name',
                            xpath="h4[contains(@class, 'experience-group-header__company')]",
                        ),
                        Node(
                            key='company_profile_endpoint',
                            extract=Ex.HREF_ENDPOINT,
                            xpath='a',
                        ),
                        Node(
                            xpath='li',
                            key='entries',
                            target=ExperienceGroupItem,
                            filter=None,
                            nodes=[
                                Node(key='position', xpath='h3'),
                                Node(
                                    key='location',
                                    xpath="p[contains(@class, 'experience-group-position__location')]",
                                ),
                            ]
                            + date_duration_description_nodes(),
                        ),
                    ],
                ),
                Node(
                    filter=None,
                    target=ExperienceItem,
                    key='_experience_items',
                    xpath="li[contains(@class, 'profile-section-card') and contains(@class, 'experience-item')]",
                    nodes=[
                        Node(key='position', xpath='h3'),
                        Node(key='company_name', xpath='h4'),
                        Node(
                            key='location',
                            xpath="p[contains(@class, 'location')]",
                        ),
                        Node(
                            key='company_profile_endpoint',
                            extract=Ex.HREF_ENDPOINT,
                            xpath='a',
                        ),
                    ]
                    + date_duration_description_nodes(),
                ),
            ],
        ),
        Node(
            key='people_also_viewed',
            xpath="section/h2[contains(text(), 'People also viewed')]/..//li",
            filter=None,
            target=PeopleAlsoViewedItem,
            nodes=[
                Node(key='name', xpath='h3'),
                Node(key='headline', xpath='p'),
                Node(key='location', xpath="div[contains(@class, 'text-sm')]"),
                Node(key='profile_endpoint', extract=Ex.HREF_ENDPOINT, xpath='a'),
            ],
        ),
    ],
)


if __name__ == '__main__':
    with open('./static/adam.html', 'r') as f:
        profile = scrape(PERSON_PROFILE_NODE, f.read())
        print(profile)
