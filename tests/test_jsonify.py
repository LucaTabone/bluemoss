from __future__ import annotations
from enum import Enum
from json import dumps
from bs4 import BeautifulSoup
from lxml.html import HtmlElement
from dataclasses import dataclass
from collections import OrderedDict
from datetime import date, datetime
from collections import OrderedDict
from .constants import FOUR_DIVS_HTML as HTML
from src.bluemoss.utils.html import lxml_etree_to_bs4
from src.bluemoss import Jsonify, JsonifyWithTag, Node, Ex, scrape


class Job(Enum):
    ENGINEER = 'Engineer'
    FARMER = 'Farmer'
    LAWYER = 'Lawyer'


@dataclass
class Address(Jsonify):
    city: str
    street: str
    zip_code: str
    country_code: str


@dataclass
class Skill(Jsonify):
    name: str
    started_at: date
    experience_level: int


@dataclass
class Employer:
    name: str
    website: str
    headquarters: OrderedDict[str, str]


@dataclass
class Person(Jsonify):
    name: str
    email: str
    birthday: date
    address: Address
    employer: Employer
    last_contacted: datetime
    job: Job
    skills: list[Skill]
    languages: set[str]
    _last_updated: datetime

    @property
    def estimated_age(self) -> int:
        today: date = date.today()
        return today.year - self.birthday.year

    @property
    def dict(self) -> dict:
        return super().dict | {'age': self.estimated_age}


def test_person_dict():
    address = Address(
        city='Los Angeles',
        street='789 Creative Blvd',
        zip_code='90001',
        country_code='US',
    )

    skill1 = Skill(
        name='Software Development',
        started_at=date(2010, 6, 1),
        experience_level=5,
    )

    skill2 = Skill(
        name='Database Management',
        started_at=date(2012, 8, 10),
        experience_level=4,
    )

    person = Person(
        name='Charlie Davis',
        email='charlie.davis@example.com',
        birthday=date(1988, 10, 20),
        address=address,
        last_contacted=datetime(2023, 10, 21, 19, 24, 35),
        job=Job.ENGINEER,
        skills=[skill1, skill2],
        languages={'English', 'French'},
        employer=Employer(
            name='Company',
            website='https://company.com',
            headquarters=OrderedDict([('USA', 'New York'), ('UK', 'London')]),
        ),
        _last_updated=datetime.now(),
    )

    expected_dict: OrderedDict = OrderedDict(
        [
            ('name', 'Charlie Davis'),
            ('email', 'charlie.davis@example.com'),
            ('birthday', '1988-10-20'),
            (
                'address',
                OrderedDict(
                    [
                        ('city', 'Los Angeles'),
                        ('street', '789 Creative Blvd'),
                        ('zip_code', '90001'),
                        ('country_code', 'US'),
                    ]
                ),
            ),
            (
                'employer',
                OrderedDict(
                    [
                        ('name', 'Company'),
                        ('website', 'https://company.com'),
                        (
                            'headquarters',
                            OrderedDict([('USA', 'New York'), ('UK', 'London')]),
                        ),
                    ]
                ),
            ),
            ('last_contacted', '2023-10-21 19:24:35'),
            ('job', 'Engineer'),
            (
                'skills',
                [
                    OrderedDict(
                        [
                            ('name', 'Software Development'),
                            ('started_at', '2010-06-01'),
                            ('experience_level', 5),
                        ]
                    ),
                    OrderedDict(
                        [
                            ('name', 'Database Management'),
                            ('started_at', '2012-08-10'),
                            ('experience_level', 4),
                        ]
                    ),
                ],
            ),
            ('languages', ['English', 'French']),
            ('age', 35),
        ]
    )

    assert person.dict == expected_dict
    assert str(person) == dumps(person.dict, indent=4)


def test_jsonify_with_tag():
    @dataclass
    class Tag(JsonifyWithTag):
        pass

    tag_instance: Tag = scrape(Node('div', target=Tag), HTML)
    assert isinstance(tag_instance, Tag)
    assert isinstance(tag_instance.lxml_tag, HtmlElement)
    assert tag_instance.source_line == 4

    bs4_tag: BeautifulSoup = scrape(Node('div', extract=Ex.BS4_TAG), HTML)
    assert isinstance(bs4_tag, BeautifulSoup)

    assert tag_instance.bs4_tag == bs4_tag
    assert lxml_etree_to_bs4(tag_instance.lxml_tag) == bs4_tag
