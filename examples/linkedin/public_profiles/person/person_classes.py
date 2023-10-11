from collections import OrderedDict
from dataclasses import dataclass, field
from typings import Dictable, DictableWithTag


@dataclass
class _DictableWithDateDurationDescription(Dictable):
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
            self.date = self._date_and_duration_text[:-len(self.duration)]
        else:
            self.date = self._date_and_duration_text
        if not self.date:
            return
        self.date = (
            self.date.strip()
                .replace("\u2013", "-")
                .replace(" -", "-")
                .replace("- ", "-")
                .replace("-", " - ")
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
        parts: list[str] = self.date.split(" - ")
        if len(parts) != 2:
            return False
        for c in parts[1].strip():
            if c.isdigit():
                return False
        return True


@dataclass
class ProfileHeader(Dictable):
    """
    Stores the information of the title-tag of a public person-profile
    (name, current company/employer, current position).
    """
    name: str | None
    headline: str | None
    followers: str | None
    _location_text: str | None
    location: str | None = field(default=None, init=False)

    def __post_init__(self):
        super().__post_init__()
        self._set_location()

    def _set_location(self):
        self.location = self._location_text


@dataclass
class ExperienceItem(_DictableWithDateDurationDescription, DictableWithTag):
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
class ExperienceGroupItem(_DictableWithDateDurationDescription, DictableWithTag):
    """
    Stores an experience-item. It is used within an experience-group instance.
    """
    position: str | None
    location: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class ExperienceGroup(DictableWithTag):
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
class Experience(Dictable):
    """ Stores the entire experience-section of a public person-profile. """
    _experience_items: list[ExperienceItem]
    _experience_groups: list[ExperienceGroup]
    entries: list[ExperienceItem | ExperienceGroup] = field(default_factory=list, init=False)

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
        return super().dict["entries"]


@dataclass
class EducationItem(_DictableWithDateDurationDescription, DictableWithTag):
    """ Stores an entry in the education-section of a public person-profile. """
    degree_info: str | None
    institution: str | None
    school_profile_endpoint: str | None
    _description_text: str | None

    def __post_init__(self):
        super().__post_init__()
        if self.description is None and self._description_text:
            self.description = self._description_text


@dataclass
class VolunteerItem(_DictableWithDateDurationDescription, DictableWithTag):
    """ Stores and entry in the 'Volunteer Experience' section of a public person-profile. """
    position: str | None
    institution: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Award(_DictableWithDateDurationDescription, DictableWithTag):
    """ Stores an entry in the "Honors & Awards" section of a public person-profile. """
    title: str
    institution: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Language(Dictable):
    """ Store an entry in the "Languages" section of a public person-profile. """
    lang: str
    level: str

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Certification(Dictable):
    """ Store an entry in the "Licenses & Certifications" section of a public person-profile. """
    name: str
    institution: str
    date_issued: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class PeopleAlsoViewedItem(Dictable):
    """ Stores an entry from the "People also viewed" section of a public person-profile.. """
    name: str
    headline: str | None
    location: str | None
    profile_endpoint: str

    def __post_init__(self):
        self._headline = self.headline
        super().__post_init__()


@dataclass
class RecommendationItem(Dictable):
    """ Stores an entry from the "Recommendations received" section of a public person-profile. """
    text: str
    name: str
    profile_endpoint: str

    def __post_init__(self):
        super().__post_init__()


@dataclass
class PublicationItem(Dictable):
    """ Stores an entry from the "Publications received" section of a public person-profile. """
    date: str | None
    journal: str | None
    headline: str | None
    url: str | None

    def __post_init__(self):
        super().__post_init__()


@dataclass
class Endorsements(Dictable):
    name: str
    endorsements: int


@dataclass
class PersonProfile(Dictable):
    """ Stores all the information scraped from a public person-profile. """
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
                self.current_employers.append((
                    item.company_profile_endpoint,
                    item.company_name
                ))

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
