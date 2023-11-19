<a href="https://ik.imagekit.io/egszdsbs2/bluemoss/adam.html?updatedAt=1699980968550">
    Download HTML
</a>
<br>
<br>
<img src="https://ik.imagekit.io/egszdsbs2/bluemoss/adam_grant_linkedin_profile.png?updatedAt=1699980197496" alt="">

# Goal - Scrape a persons public LinkedIn page

### Step 1 - Identify data points to scrape

- url
- name
- about
- headline
- location
- experience
- education
- skills
- volunteering
- publications
- recommendations
- amount of followers
- awards
- certifications
- languages
- people also viewed

<br>

### Step 2 - Analyze the HTML
Before we start writing our Node object which will capture the entire data of a persons LinkedIn profile, 
we need to understand the structure of the HTML, specifically
the nature of the html tags that contain the different data points we want to scrape.
<br>
<br>
In the other 3 examples (Blog Site, News Site, E-Commerce Site) we were scraping a list of the same items 
(a list of blog posts, a list of article preview, a list of products). In these examples we just needed to identify what these tags
had in common and we would be able to scrape all of them.
<br>
<br>
The LinkedIn profile page is different. We have many more data points to scrape here,
and they do not share a common tag setup. Producing a Node object that is able to capture all the data points
we are interested in is therefor likely to be a lot larger then the ones we produced for the other examples.

<br>

### Step 3 - Create a dataclass per data point

The dataclass **PersonProfile** at the very bottom is our master-class.
It contains all other dataclasses that reflect a data-point each.

```python
from collections import OrderedDict
from dataclasses import dataclass, field
from bluemoss import Jsonify, JsonifyWithTag


@dataclass
class _JsonifyWithDateDurationDescription(Jsonify):
    """
    Many sections within a LI person-profile reference a date, a duration and a descriptive text in the same way.
    The dataclasses which inherit from this abstract dataclass can now access these parameters through the
    .date, .duration and .description properties.
    """

    duration: str | None
    _description_more_text: str | None
    _description_less_text: str | None
    _date_and_duration_text: str | None
    date: str | None = field(default=None, init=False)
    description: str | None = field(default=None, init=False)

    def __post_init__(self):
        super().__post_init__()
        self._set_date()
        self._set_description()

    def _set_date(self):
        if not self._date_and_duration_text:
            self.date = None
        elif self.duration:
            self.date = self._date_and_duration_text[: -len(self.duration)]
        else:
            self.date = self._date_and_duration_text
        if not self.date:
            return
        self.date = (
            self.date.strip()
            .replace('\u2013', '-')
            .replace(' -', '-')
            .replace('- ', '-')
            .replace('-', ' - ')
        )

    def _set_description(self):
        if self._description_more_text:
            self.description = self._description_more_text
        elif self._description_less_text:
            self.description = self._description_less_text

    @property
    def is_current_position(self) -> bool:
        """
        Determine if this object refers to an experience item where the
        date indicates that this is the current position.
        """
        if not self.date:
            return False
        parts: list[str] = self.date.split(' - ')
        if len(parts) != 2:
            return False
        for c in parts[1].strip():
            if c.isdigit():
                return False
        return True


@dataclass
class ProfileHeader(Jsonify):
    """
    Stores the information of the title-tag of a public person-profile
    (name, current company/employer, current position).
    """

    name: str | None
    headline: str | None
    location: str | None
    followers: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class ExperienceItem(_JsonifyWithDateDurationDescription, JsonifyWithTag):
    """
    Stores a simple experience-item. It is used for an entry in a persons experience section
    in case the person was working in ONE position at a company for certain time-period.
    """

    company_name: str
    position: str | None
    location: str | None
    company_profile_endpoint: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class ExperienceGroupItem(_JsonifyWithDateDurationDescription, JsonifyWithTag):
    """
    Stores an experience-item. It is used within an experience-group instance.
    """

    position: str | None
    location: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class ExperienceGroup(JsonifyWithTag):
    """
    Stores an experience-group. An experience-group is used instead of an experience-item in case a person
    was in multiple positions at the same company without any breaks between those positions.
    """

    duration: str
    company_name: str
    company_profile_endpoint: str
    entries: list[ExperienceGroupItem]

    def __post_init__(self):
        super().__post_init__()

    @property
    def is_current_position(self) -> bool:
        if not self.entries:
            return False
        return self.entries[0].is_current_position


@dataclass
class Experience(Jsonify):
    """Stores the entire experience-section of a public person-profile."""

    _experience_items: list[ExperienceItem]
    _experience_groups: list[ExperienceGroup]
    entries: list[ExperienceItem | ExperienceGroup] = field(
        default_factory=list, init=False
    )

    def __post_init__(self):
        super().__post_init__()
        self._set_entries_and_sort_by_tag_source_line()

    def _set_entries_and_sort_by_tag_source_line(self):
        append = self.entries.append
        for li in [self._experience_items, self._experience_groups]:
            if not li:
                continue
            for elem in li:
                append(elem)
        self.entries.sort(key=lambda _elem: _elem.source_line)

    @property
    def dict(self) -> list[dict]:
        return super().dict['entries']


@dataclass
class EducationItem(_JsonifyWithDateDurationDescription, JsonifyWithTag):
    """Stores an entry in the education-section of a public person-profile."""

    degree_info: str | None
    institution: str | None
    school_profile_endpoint: str | None
    _description_text: str | None

    def __post_init__(self):
        super().__post_init__()
        if self.description is None and self._description_text:
            self.description = self._description_text


@dataclass
class VolunteerItem(_JsonifyWithDateDurationDescription, JsonifyWithTag):
    """Stores and entry in the 'Volunteer Experience' section of a public person-profile."""

    position: str | None
    institution: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Award(_JsonifyWithDateDurationDescription, JsonifyWithTag):
    """Stores an entry in the "Honors & Awards" section of a public person-profile."""

    title: str
    institution: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Language(Jsonify):
    """Store an entry in the "Languages" section of a public person-profile."""

    lang: str
    level: str

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Certification(Jsonify):
    """Store an entry in the "Licenses & Certifications" section of a public person-profile."""

    name: str
    institution: str
    date_issued: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class PeopleAlsoViewedItem(Jsonify):
    """Stores an entry from the "People also viewed" section of a public person-profile.."""

    name: str
    headline: str | None
    location: str | None
    profile_endpoint: str

    def __post_init__(self):
        self._headline = self.headline
        super().__post_init__()


@dataclass
class RecommendationItem(Jsonify):
    """Stores an entry from the "Recommendations received" section of a public person-profile."""

    text: str
    name: str
    profile_endpoint: str

    def __post_init__(self):
        super().__post_init__()


@dataclass
class PublicationItem(Jsonify):
    """Stores an entry from the "Publications received" section of a public person-profile."""

    date: str | None
    journal: str | None
    headline: str | None
    url: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Endorsements(Jsonify):
    name: str
    endorsements: int


@dataclass
class PersonProfile(Jsonify):
    """Stores all the information scraped from a public person-profile."""

    profile_endpoint: str
    about: str | None
    header: ProfileHeader
    experience: Experience
    languages: list[Language]
    education: list[EducationItem]
    volunteering: list[VolunteerItem]
    certifications: list[Certification]
    awards: list[Award]
    publications: list[PublicationItem]
    recommendations: list[RecommendationItem]
    people_also_viewed: list[PeopleAlsoViewedItem]
    company_name: str | None = field(default=None, init=False)
    current_employers: list[tuple[str, str]] = field(default_factory=list, init=False)

    def __post_init__(self):
        self._headline = self.header.headline
        self._set_current_employer_data()
        super().__post_init__()

    def _set_current_employer_data(self):
        """
        Set the fields @param company_name and @param company_profile_endpoint
        which represent the current employer.
        """
        if self.experience is None or self.experience.entries is None:
            return
        for item in self.experience.entries:
            if item.company_profile_endpoint and item.is_current_position:
                self.current_employers.append(
                    (item.company_profile_endpoint, item.company_name)
                )

    @property
    def dict(self) -> OrderedDict:
        """
        res: OrderedDict = self.header.dict
        for k, v in super().dict.items():
            if k != "header":
                res[k] = v
        return res
        """
        return super().dict
```

<br>

### Step 4 - Build the Node object to scrape all articles

```python
# examples/linkedin/node.py

from bluemoss import Ex, Node
from bluemoss.utils import get_infix, get_endpoint
from examples.linkedin.public_profiles.person.classes import *


def date_duration_description_nodes() -> list[Node]:
    return [
        Node(key='duration', xpath="span[contains(@class, 'date-range')]/span"),
        Node(
            key='_date_and_duration_text',
            xpath="span[contains(@class, 'date-range')]",
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
```

### Step 5 - Scrape the HTML / Test the Node object
```python
# main.py

from bluemoss import scrape
from examples.linkedin.public_profiles.person.classes import PersonProfile
from examples.linkedin.public_profiles.person.node import PERSON_PROFILE_NODE


with open('../../examples/linkedin/public_profiles/person/static/adam.png.html', 'r') as f:
    profile: PersonProfile = scrape(PERSON_PROFILE_NODE, f.read())
    print(profile)
```

```json
// the print output


{
    "profile_endpoint": "/in/adammgrant",
    "about": "Organizational psychologist at Wharton, #1 NYT bestselling author of THINK AGAIN, and host of the TED podcast WorkLife",
    "header": {
        "name": "Adam Grant",
        "headline": "Organizational psychologist at Wharton, #1 NYT bestselling author of THINK AGAIN, and host of the TED podcast WorkLife",
        "location": "Philadelphia, Pennsylvania, United States",
        "followers": "5M followers"
    },
    "experience": [
        {
            "duration": "10 years 7 months",
            "date": "Apr 2013 - Present",
            "company_name": "Penguin Publishing Group",
            "position": "Author, THINK AGAIN, GIVE AND TAKE, ORIGINALS, OPTION B",
            "location": null,
            "company_profile_endpoint": "/company/penguin-group-usa"
        },
        {
            "duration": "8 years 8 months",
            "date": "Mar 2015 - Present",
            "company_name": "The New York Times",
            "position": "Contributing Op-Ed Writer",
            "location": null,
            "company_profile_endpoint": "/company/the-new-york-times"
        },
        {
            "duration": "10 years 10 months",
            "date": "Jan 2013 - Present",
            "company_name": "Washington Speakers Bureau",
            "position": "Keynote Speaker",
            "location": null,
            "company_profile_endpoint": "/company/thewsbexperience"
        },
        {
            "duration": "3 years",
            "date": "Jul 2010 - Jun 2013",
            "company_name": "Academy of Management Journal",
            "position": "Associate Editor",
            "location": null,
            "company_profile_endpoint": null
        },
        {
            "duration": "2 years",
            "date": "2007 - 2009",
            "company_name": "University of North Carolina at Chapel Hill",
            "position": "Assistant Professor of Organizational Behavior",
            "location": null,
            "company_profile_endpoint": "/school/university-of-north-carolina-at-chapel-hill"
        }
    ],
    "languages": [
        {
            "lang": "English",
            "level": "Native or bilingual proficiency"
        },
        {
            "lang": "Spanish",
            "level": "Limited working proficiency"
        }
    ],
    "education": [
        {
            "duration": null,
            "date": "1999 - 2003",
            "degree_info": "B.A.Psychology",
            "institution": "Harvard University",
            "school_profile_endpoint": "/school/harvard-university"
        },
        {
            "duration": null,
            "date": "2003 - 2006",
            "degree_info": "Ph.D. and M.S.Organizational Psychology",
            "institution": "University of Michigan",
            "school_profile_endpoint": "/school/university-of-michigan"
        }
    ],
    "volunteering": [],
    "certifications": [],
    "awards": [
        {
            "duration": null,
            "date": "May 2016",
            "title": "100 Most Creative People in Business",
            "institution": "Fast Company"
        },
        {
            "duration": null,
            "date": "Apr 2016",
            "description": "Highest-rated Wharton MBA professor",
            "title": "Class of 1984 Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Mar 2016",
            "title": "#1 New York Times bestseller",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Nov 2015",
            "title": "Thinkers 50 Most Influential Management Thinkers",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2015",
            "description": "Highest-rated Wharton MBA professor",
            "title": "Class of 1984 Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Mar 2015",
            "title": "World Economic Forum Young Global Leader",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Nov 2014",
            "description": "http://www.rotman.utoronto.ca/Connect/MediaCentre/NewsReleases/20141110.aspx",
            "title": "Fellow, Martin Prosperity Institute",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Oct 2014",
            "description": "http://www.hrmagazine.co.uk/static/thinkers-os",
            "title": "HR's Most Influential International Thinkers",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2014",
            "title": "\"Goes Above and Beyond the Call of Duty\" MBA Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2014",
            "description": "Highest-rated Wharton MBA professor",
            "title": "Class of 1984 Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2014",
            "description": "MBA Curriculum",
            "title": "Excellence in Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2014",
            "description": "Wharton Undergraduate Division",
            "title": "Excellence in Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Dec 2013",
            "description": "http://www.forbes.com/sites/susanmcpherson/2013/12/16/the-most-dynamic-social-innovation-initiatives-of-2013/",
            "title": "Forbes Most Dynamic Social Innovation Initiatives of 2013",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Dec 2013",
            "description": "http://blogs.hbr.org/2013/12/the-ideas-that-shaped-management-in-2013/",
            "title": "Harvard Business Review Ideas that Shaped Management",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Dec 2013",
            "description": "http://online.wsj.com/news/articles/SB10001424052702303670804579234504183150672",
            "title": "Wall Street Journal Favorite Books of 2013",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Dec 2013",
            "description": "http://www.washingtonpost.com/national/on-leadership/2013-books-every-leader-should-read/2013/12/16/290d326e-6426-11e3-aa81-e1dab1360323_gallery.html#item0",
            "title": "Washington Post Books Every Leader Should Read",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Nov 2013",
            "title": "Amazon Best Books of the Year",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Nov 2013",
            "description": "http://www.ft.com/intl/cms/s/2/f60b681e-529f-11e3-8586-00144feabdc0.html#axzz2m8Iif2bZ",
            "title": "Financial Times Books of the Year",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Nov 2013",
            "description": "www.inc.com/ss/jeff-haden/best-2013-books-entrepreneurs",
            "title": "Inc. Best Books of 2013 for Entrepreneurs",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Oct 2013",
            "description": "http://money.cnn.com/gallery/leadership/2013/10/31/best-business-books.fortune/5.html",
            "title": "Fortune's Five Must-Read Business Books",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "May 2013",
            "description": "http://www.oprah.com/book-list/14-Riveting-Reads-to-Pick-Up-in-May-2013",
            "title": "Oprah Magazine 15 riveting reads to pick up in May",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2013",
            "description": "Highest-rated Wharton MBA professor",
            "title": "Class of 1984 Teaching Award",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2013",
            "title": "Excellence in Teaching Award, MBA Curriculum",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2013",
            "title": "New York Times bestseller",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2013",
            "title": "Wall Street Journal bestseller",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2013",
            "title": "\u201cGoes Above and Beyond the Call of Duty\u201d MBA Teaching Award",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Aug 2012",
            "title": "BusinessWeek Favorite Professors",
            "institution": "-"
        },
        {
            "duration": null,
            "date": "Apr 2012",
            "description": "Highest-rated Wharton MBA professor",
            "title": "Class of 1984 Teaching Award",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Apr 2012",
            "title": "\u201cGoes Above and Beyond the Call of Duty\u201d MBA Teaching Award",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Mar 2012",
            "title": "Excellence in Teaching Award, MBA Elective Curriculum",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "May 2011",
            "title": "Cummings Scholarly Achievement Award",
            "institution": "Academy of Management, Organizational Behavior Division"
        },
        {
            "duration": null,
            "date": "May 2011",
            "title": "Distinguished Scientific Award for Early Career Contribution to Applied Psychology",
            "institution": "American Psychological Association"
        },
        {
            "duration": null,
            "date": "Apr 2011",
            "title": "Distinguished Early Career Contributions Award \u2013 Science",
            "institution": "Society for Industrial and Organizational Psychology"
        },
        {
            "duration": null,
            "date": "Apr 2011",
            "title": "Excellence in Teaching Award, MBA Core Curriculum",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Apr 2011",
            "title": "Excellence in Teaching Award, Undergraduate Division",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Apr 2011",
            "title": "\u201cGoes Above and Beyond the Call of Duty\u201d MBA Teaching Award",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Feb 2011",
            "title": "World\u2019s 40 Best Business School Professors Under 40",
            "institution": "Poets and Quants"
        },
        {
            "duration": null,
            "date": "May 2010",
            "title": "Owens Scholarly Achievement Award, Best Publication in I/O Psychology",
            "institution": "Society for Industrial and Organizational Psychology"
        },
        {
            "duration": null,
            "date": "Apr 2010",
            "title": "Excellence in Teaching Award, MBA Elective Curriculum",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Apr 2010",
            "title": "Excellence in Teaching Award, Undergraduate Division",
            "institution": "The Wharton School"
        },
        {
            "duration": null,
            "date": "Apr 2009",
            "title": "MBA Teaching All-Star",
            "institution": "Kenan-Flagler Business School"
        },
        {
            "duration": null,
            "date": "Mar 2009",
            "title": "Tanner Award for Excellence in Undergraduate Teaching",
            "institution": "University of North Carolina at Chapel Hill"
        },
        {
            "duration": null,
            "date": "Apr 2008",
            "title": "Rensis Likert Prize, Best Paper from a Dissertation in Organization Studies",
            "institution": "University of Michigan"
        },
        {
            "duration": null,
            "date": "Mar 2008",
            "title": "Weatherspoon Award for Excellence in Undergraduate Teaching",
            "institution": "Kenan-Flagler Business School"
        },
        {
            "duration": null,
            "date": "Jan 2008",
            "title": "Best Published Scholarly Article",
            "institution": "Center for Positive Organizational Scholarship"
        },
        {
            "duration": null,
            "date": "May 2005",
            "title": "Early Research Award, Applied Science",
            "institution": "American Psychological Association"
        },
        {
            "duration": null,
            "date": "Sep 2004",
            "title": "Graduate Research Fellowship",
            "institution": "National Science Foundation"
        },
        {
            "duration": null,
            "date": "Apr 2003",
            "title": "Junior Fellow",
            "institution": "American Academy of Political and Social Science"
        },
        {
            "duration": null,
            "date": "Feb 2001",
            "description": "For leadership, commitment, and business acumen",
            "title": "Manager of the Year",
            "institution": "Harvard Student Agencies"
        }
    ],
    "publications": [],
    "recommendations": [],
    "people_also_viewed": [
        {
            "name": "Simon Sinek",
            "headline": "Author and Founder of The Optimism Company",
            "location": "New York, NY",
            "profile_endpoint": "/in/simonsinek"
        },
        {
            "name": "Bren\u00e9 Brown",
            "headline": "University of Houston + University of Texas at Austin | Researcher. Storyteller. Courage-builder.",
            "location": "Houston, TX",
            "profile_endpoint": "/in/brenebrown"
        },
        {
            "name": "Amy Cuddy",
            "headline": "Social Psychologist, Bestselling Author, International Keynote Speaker",
            "location": "Los Angeles, CA",
            "profile_endpoint": "/in/amy-cuddy-3654034"
        },
        {
            "name": "Arianna Huffington",
            "headline": "Founder and CEO at Thrive Global",
            "location": "New York, NY",
            "profile_endpoint": "/in/ariannahuffington"
        },
        {
            "name": "Bill Gates",
            "headline": "Co-chair, Bill & Melinda Gates Foundation",
            "location": "Seattle, WA",
            "profile_endpoint": "/in/williamhgates"
        },
        {
            "name": "Satya Nadella",
            "headline": "Chairman and CEO at Microsoft",
            "location": "Redmond, WA",
            "profile_endpoint": "/in/satyanadella"
        },
        {
            "name": "Marshall Goldsmith",
            "headline": "WSJ Bestseller Becoming Coachable Out NOW | Thinkers50 Hall of Fame | #1 Executive Coach | #1 Leadership Thought Leader | #1 NYT Bestselling Author",
            "location": "Rancho Santa Fe, CA",
            "profile_endpoint": "/in/marshallgoldsmith"
        },
        {
            "name": "Tony Robbins",
            "headline": "#1 New York Times best-selling author, life and business strategist, philanthropist, entrepreneur",
            "location": "San Diego, CA",
            "profile_endpoint": "/in/officialtonyrobbins"
        },
        {
            "name": "Daniel Goleman",
            "headline": "Director of Daniel Goleman Emotional Intelligence Online Courses and Senior Consultant at Goleman Consulting Group",
            "location": "Northampton, MA",
            "profile_endpoint": "/in/danielgoleman"
        },
        {
            "name": "Jeff Weiner",
            "headline": "Executive Chairman at LinkedIn / Founding Partner Next Play Ventures",
            "location": "United States",
            "profile_endpoint": "/in/jeffweiner08"
        },
        {
            "name": "Richard Branson",
            "headline": "Founder at Virgin Group",
            "location": null,
            "profile_endpoint": "/in/rbranson"
        },
        {
            "name": "Gretchen Rubin",
            "headline": "Bestselling writer about habits and happiness at gretchenrubin.com",
            "location": "New York City Metropolitan Area",
            "profile_endpoint": "/in/gretchenrubin"
        },
        {
            "name": "Patrick Lencioni",
            "headline": "Founder & President at The Table Group | Six Types of Working Genius | Five Dysfunctions of a Team | The Organizational Health People",
            "location": "Lafayette, CA",
            "profile_endpoint": "/in/patrick-lencioni-orghealth"
        },
        {
            "name": "Susan Cain",
            "headline": "#1 bestselling author of BITTERSWEET and QUIET. Unlikely award-winning speaker. Top 10 LinkedIn Influencer. Join 475,000 subscribers to my Kindred Letters newsletter: sign up at susancain.net/newsletter/ (see link below)",
            "location": "New York, NY",
            "profile_endpoint": "/in/susancain"
        },
        {
            "name": "Sara Blakely",
            "headline": "Founder of SPANX",
            "location": "Atlanta, GA",
            "profile_endpoint": "/in/sarablakely27"
        },
        {
            "name": "Ryan Reynolds",
            "headline": "Part-Time Actor, Business Owner",
            "location": "New York, NY",
            "profile_endpoint": "/in/vancityreynolds"
        },
        {
            "name": "Tim Ferriss",
            "headline": "Author of 5 #1 NYT/WSJ bestsellers, early-stage investor, host of The Tim Ferriss Show podcast (900M+ downloads), and collector of the strange.",
            "location": "Austin, TX",
            "profile_endpoint": "/in/timferriss"
        },
        {
            "name": "Andrew Huberman",
            "headline": "Professor and Neuroscientist at Stanford University and Host of the Huberman Lab podcast",
            "location": "Stanford, CA",
            "profile_endpoint": "/in/andrew-huberman"
        },
        {
            "name": "Sahil Bloom",
            "headline": "Exploring my curiosity and sharing what I learn along the way.",
            "location": "New York, NY",
            "profile_endpoint": "/in/sahilbloom"
        },
        {
            "name": "Alex Hilleary",
            "headline": "People Ops Community + Job Board (& Partnerships) @ ChartHop | Prev. Co-Founder @ Gather (YC S20, acq 2022)",
            "location": "United States",
            "profile_endpoint": "/in/alex-hilleary"
        }
    ],
    "current_employers": [
        [
            "/company/penguin-group-usa",
            "Penguin Publishing Group"
        ],
        [
            "/company/the-new-york-times",
            "The New York Times"
        ],
        [
            "/company/thewsbexperience",
            "Washington Speakers Bureau"
        ]
    ]
}
```