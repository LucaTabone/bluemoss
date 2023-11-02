from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from collections import OrderedDict
from datetime import date, datetime
from src.bluemoss.classes.dict import Jsonify


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
class Person(Jsonify):
    name: str
    email: str
    birthday: date
    address: Address
    last_contacted: datetime
    job: Job
    skills: list[Skill]
    languages: set[str]
    _last_updated: datetime

    @property
    def age(self) -> int:
        today: date = date.today()
        age = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    @property
    def dict(self) -> dict:
        return super().dict | {'age': self.age}


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
        ('languages', {'French', 'English'}),
        ('age', 35),
    ]
)


def test_person_dict():
    assert person.dict == expected_dict
