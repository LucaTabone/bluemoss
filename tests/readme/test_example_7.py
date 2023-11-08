from __future__ import annotations
from constants import HTML
from dataclasses import dataclass
from src.bluemoss import Node, scrape, Jsonify


@dataclass
class Companies(Jsonify):
    companies: list[Company]
    amount_uk_companies: int
    amount_us_companies: int


@dataclass
class Company(Jsonify):
    id: str
    name: str
    location: str


node = Node(
    target=Companies,
    nodes=[
        Node(
            "count(//div[@class='location_uk'])",
            key='amount_uk_companies',
            transform=lambda count: int(count) if count else None
        ),
        Node(
            "count(//div[@class='location_us'])",
            key='amount_us_companies',
            transform=lambda count: int(count) if count else None
        ),
        Node(
            'li',
            filter=None,
            key='companies',
            target=Company,
            nodes=[
                Node('a', key='name'),
                Node('p', key='location'),
                Node(
                    'a',
                    key='id',
                    extract="href",
                    transform=lambda href: href.split("=")[1]
                )
            ]
        )
    ]
)

companies: Companies = scrape(node, HTML)

assert isinstance(companies, Companies)

assert companies.dict == {
    "companies": [
        {
            "id": "apple",
            "name": "Apple",
            "location": "Cupertino, California"
        },
        {
            "id": "google",
            "name": "Google",
            "location": "Mountain View, California"
        },
        {
            "id": "tesla",
            "name": "Tesla",
            "location": "Austin, Texas"
        },
        {
            "id": "deepmind",
            "name": "DeepMind",
            "location": "London, United Kingdom"
        }
    ],
    "amount_uk_companies": 1,
    "amount_us_companies": 3
}
