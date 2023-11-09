<p align="center">
  <img src="https://github.com/LucaTabone/bluemoss/blob/main/logo.png?raw=True" width="420px" align="center" alt="bluemoss logo" />
  <h1 align="center">bluemoss</h1>
  <h3 align="center">a simple way to scrape the web</h3>
  <br>
  <p align="center">
    <a href="https://github.com/grantjenks/blue">
        <img src="https://camo.githubusercontent.com/dbdbcf26db37abfa1f2ab7e6c28c8b3a199f2dad98e4ef53a50e9c45c7e4ace8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c75652d626c75652e737667" alt="Code style: blue"/>
    </a>
    <img src="https://img.shields.io/github/actions/workflow/status/LucaTabone/bluemoss/test.yml?branch=main&label=tests" alt="GitHub Workflow Status (main)"/>
    <a href="https://LucaTabone.github.io/bluemoss/htmlcov/index.html">
        <img src="https://img.shields.io/codecov/c/github/LucaTabone/bluemoss" alt="Coverage">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/bluemoss" alt="Supported python versions"/>
    <img src="https://img.shields.io/pypi/v/bluemoss" alt="Latest package version"/>
  </p>
</p>

<br>
<br>
<br>

## example html

```html
<html>
    <head>
        <title>Portfolio</title>
    </head>
    <body>
        <li>
            <div>
                <a href="/portfolio?company=apple">
                    Apple
                </a>
                <div class="location_us">
                    <p>Cupertino, California</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                <a href="/portfolio?company=google">
                    Google
                </a>
                <div class="location_us">
                    <p>Mountain View, California</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                 <a href="/portfolio?company=tesla">
                    Tesla
                </a>
                <div class="location_us">
                    <p>Austin, Texas</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                <a href="/portfolio?company=deepmind">
                    DeepMind
                </a>
                <div class="location_uk">
                    <p>London, United Kingdom</p>
                </div>
            </div>
        </li>
    </body>
</html>
```

<br>
<br>

## scraping example 1
```python
from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


nodes: list[Node] = [
    Node('a'),
    Node('div/a'),
    Node('div/a'),
    Node('body//a'),
    Node('body//div/a'),
    Node('a', filter=0),
]

for node in nodes:
    assert scrape(node, HTML) == 'Apple'
```

<br>
<br>

## scraping example 2
```python
from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


nodes: list[Node] = [
    Node('p'),
    Node('li//p'),
    Node('div/p'),
    Node('div//p'),
    Node('div[contains(@class, "location_")]'),
    Node('body//div[contains(@class, "location_")]'),
]

for node in nodes:
    assert scrape(node, HTML) == 'Cupertino, California'
```

<br>
<br>

## scraping example 3
```python
from src.bluemoss import Node, Range, scrape
from ..constants import README_EXAMPLE_HTML as HTML


node = Node('a', filter=3)
assert scrape(node, HTML) == 'DeepMind'

node = Node('a', filter=[0, 2])
assert scrape(node, HTML) == ['Apple', 'Tesla']

node = Node('a', filter=Range(2))
assert scrape(node, HTML) == ['Tesla', 'DeepMind']

node = Node('a', filter=Range(2, 4))
assert scrape(node, HTML) == ['Tesla', 'DeepMind']

node = Node('a', filter=Range(2, 3))
assert scrape(node, HTML) == ['Tesla']

node = Node('a', filter=None)
assert scrape(node, HTML) == ['Apple', 'Google', 'Tesla', 'DeepMind']
```

<br>
<br>

## scraping example 4
```python
from src.bluemoss import Node, Range, Ex, scrape
from ..constants import README_EXAMPLE_HTML as HTML


def get_company_id(hrefs: list[str]) -> list[str]:
    return [href.split('=')[-1] for href in hrefs]


for node in [
    Node('a', filter=Range(1), extract=Ex.HREF, transform=get_company_id),
    Node('a', filter=Range(1), extract='href', transform=get_company_id),
    Node('a/@href', filter=Range(1), transform=get_company_id),
]:
    assert scrape(node, HTML) == ['google', 'tesla', 'deepmind']
```

<br>
<br>

## scraping example 5
```python
from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


node = Node(
    'li',
    filter=None,
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node('a/@href', key='id', transform=lambda href: href.split('=')[1]),
    ],
)


assert scrape(node, HTML) == [
    {'id': 'apple', 'name': 'Apple', 'headquarters': 'Cupertino, California'},
    {'id': 'google', 'name': 'Google', 'headquarters': 'Mountain View, California'},
    {'id': 'tesla', 'name': 'Tesla', 'headquarters': 'Austin, Texas'},
    {'id': 'deepmind', 'name': 'DeepMind', 'headquarters': 'London, United Kingdom'},
]
```

<br>
<br>

## scraping example 6
```python
from src.bluemoss import Node, scrape
from ..constants import README_EXAMPLE_HTML as HTML


node = Node(
    'li',
    filter=None,
    key='companies',
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node('a/@href', key='id', transform=lambda href: href.split('=')[1]),
    ],
)

assert scrape(node, HTML) == {
    'companies': [
        {'id': 'apple', 'name': 'Apple', 'headquarters': 'Cupertino, California'},
        {'id': 'google', 'name': 'Google', 'headquarters': 'Mountain View, California'},
        {'id': 'tesla', 'name': 'Tesla', 'headquarters': 'Austin, Texas'},
        {
            'id': 'deepmind',
            'name': 'DeepMind',
            'headquarters': 'London, United Kingdom',
        },
    ]
}
```

<br>
<br>

## scraping example 7
```python
from __future__ import annotations
from dataclasses import dataclass
from src.bluemoss import Node, scrape, Jsonify
from ..constants import README_EXAMPLE_HTML as HTML


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

assert isinstance(companies, Companies)

assert companies.dict == {
    'companies': [
        {'id': 'apple', 'name': 'Apple', 'location': 'Cupertino, California'},
        {'id': 'google', 'name': 'Google', 'location': 'Mountain View, California'},
        {'id': 'tesla', 'name': 'Tesla', 'location': 'Austin, Texas'},
        {'id': 'deepmind', 'name': 'DeepMind', 'location': 'London, United Kingdom'},
    ],
    'amount_uk_companies': 1,
    'amount_us_companies': 3,
}

assert (
    companies.json
    == """{
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
}"""
)
```

<br>
<br>

