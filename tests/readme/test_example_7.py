from dataclasses import dataclass
from src.bluemoss import Node, scrape, Jsonify
from ..constants import README_EXAMPLE_HTML as HTML


@dataclass
class Company(Jsonify):
    id: str
    name: str
    location: str


@dataclass
class Companies(Jsonify):
    companies: list[Company]
    amount_uk_companies: int
    amount_us_companies: int


node = Node(
    target=Companies,
    nodes=[
        Node(
            "count(//div[@class='location_uk'])",
            key='amount_uk_companies',
            transform=lambda count: int(count) if count else None,
        ),
        Node(
            "count(//div[@class='location_us'])",
            key='amount_us_companies',
            transform=lambda count: int(count) if count else None,
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
                    extract='href',
                    transform=lambda href: href.split('=')[1],
                ),
            ],
        ),
    ],
)

companies: Companies = scrape(node, HTML)


def test_instance_type():
    assert isinstance(companies, Companies)


def test_dict_value():
    assert companies.dict == {
        'companies': [
            {'id': 'apple', 'name': 'Apple', 'location': 'Cupertino'},
            {'id': 'google', 'name': 'Google', 'location': 'Mountain View'},
            {'id': 'tesla', 'name': 'Tesla', 'location': 'Austin'},
            {'id': 'deepmind', 'name': 'DeepMind', 'location': 'London'},
        ],
        'amount_uk_companies': 1,
        'amount_us_companies': 3,
    }


def test_json_value():
    assert companies.json == \
        """{
    "companies": [
        {
            "id": "apple",
            "name": "Apple",
            "location": "Cupertino"
        },
        {
            "id": "google",
            "name": "Google",
            "location": "Mountain View"
        },
        {
            "id": "tesla",
            "name": "Tesla",
            "location": "Austin"
        },
        {
            "id": "deepmind",
            "name": "DeepMind",
            "location": "London"
        }
    ],
    "amount_uk_companies": 1,
    "amount_us_companies": 3
}"""
