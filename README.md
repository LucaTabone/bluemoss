<p style="text-align: center">
  <img src="https://github.com/LucaTabone/bluemoss/blob/main/logo.png?raw=True" width="420px" align="center" alt="bluemoss logo" />
  <h1 align="center">bluemoss</h1>
  <h3 align="center">a simple way to scrape the web</h3>
  <br>
  <p style="text-align: center">
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

<br/>
<br/>

<h3>Example 1</h3>
```python
from bluemoss import Node, scrape


node = Node('a'),                        # scrape(node, HTML) == 'Apple'
node = Node('div/a')                     # scrape(node, HTML) == 'Apple'
node = Node('body//a')                   # scrape(node, HTML) == 'Apple'
node = Node('body//div/a')               # scrape(node, HTML) == 'Apple'
node = Node('a', filter=0)               # scrape(node, HTML) == 'Apple'
```

<br/>
<br/>

<h3>Example 2</h3>
```python
from bluemoss import Node, scrape


node = Node('p')                                       # 'Cupertino, California'
node = Node('li//p')                                   # 'Cupertino, California'
node = Node('div/p')                                   # 'Cupertino, California'
node = Node('div//p')                                  # 'Cupertino, California'
node = Node('p[contains(@class, "location_")]')        # 'Cupertino, California'
node = Node('div//p[contains(@class, "location_")]')   # 'Cupertino, California'
```

<br/>
<br/>

<h3>Example 3</h3>
```python
from bluemoss import Node, scrape


node = Node('a', filter=3),              # 'DeepMind'
node = Node('a', filter=[0, 2]),         # ['Apple', 'Tesla']
node = Node('a', filter=Range(2))        # ['Tesla', 'DeepMind']
node = Node('a', filter=Range(2, 4))     # ['Tesla', 'DeepMind']
node = Node('a', filter=Range(2, 3))     # ['Tesla']
node = Node('a', filter=None)            # ['Apple', 'Google', 'Tesla', 'DeppMind']
```

<br>
<br>

<h3>Example 4</h3>
```python
from bluemoss import Node, Range, Ex, scrape


node_1 = Node(
    'a',
    filter=Range(1),
    extract=Ex.HREF,
    transformer=lambda href: href.split('?')[1]
)
# scrape(node_1, HTML) == ['google', 'tesla', 'deepmind']


node_2 = Node(
    'a',
    filter=Range(1),
    extract="href",
    transformer=lambda href: href.split('?')[1]
)
# scrape(node_2, HTML) == ['google', 'tesla', 'deepmind']


node_3 = Node(
    'a/@href',
    filter=Range(1),
    transformer=lambda href: href.split('?')[1]
)
# scrape(node_3, HTML) == ['google', 'tesla', 'deepmind']
```

<br/>
<br/>

<h3>Example 5</h3>

```python
from bluemoss import Node, scrape


node = Node(
    'li',
    filter=None,
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node(
            'a/@href',
            key='id', 
            transform=lambda href: href.split("=")[1]
        )
    ]
)


print(scrape(node, HTML))
```

**Output**
```python
[
    {
        'id': 'apple',
        'name': 'Apple', 
        'headquarters': 'Cupertino, California'
    },
    {
        'id': 'google',
        'name': 'Google',
        'headquarters': 'Mountain View, California'
    },
    {
        'id': 'tesla',
        'name': 'Tesla', 
        'headquarters': 'Austin, Texas'
    },
    {
        'id': 'deepmind',
        'name': 'DeepMind',
        'headquarters': 'London, United Kingdom'
    }
]
```

<br/>
<br/>

<h3>Example 6</h3>

```python
from bluemoss import Node, scrape


node = Node(
    'li',
    filter=None,
    key='companies',
    nodes=[
        Node('a', key='name'),
        Node('p', key='headquarters'),
        Node(
            'a/@href',
            key='id', 
            transform=lambda href: href.split("=")[1]
        )
    ]
)


print(scrape(node, HTML))
```

**Output**
```python
{
    'companies': [
        {
            'id': 'apple',
            'name': 'Apple', 
            'headquarters': 'Cupertino, California'
        },
        {
            'id': 'google',
            'name': 'Google',
            'headquarters': 'Mountain View, California'
        },
        {
            'id': 'tesla',
            'name': 'Tesla', 
            'headquarters': 'Austin, Texas'
        },
        {
            'id': 'deepmind',
            'name': 'DeepMind',
            'headquarters': 'London, United Kingdom'
        }
    ]
}
```


<br/>
<br/>

<h3>Example 7</h3>

```python
from __future__ import annotations
from dataclasses import dataclass
from bluemoss import Node, Range, Ex, scrape


@dataclass
class Companies:
    companies: list[Company]
    amount_uk_companies: int
    amount_us_companies: int

    
@dataclass
class Company:
    id: str
    name: str
    location: str


node = Node(
    target=Companies,
    nodes=[
        Node(
            key='amount_uk_companies',
            transform=lambda tags: len(tags)
        ),
        Node(
            key='amount_us_companies',
            transform=lambda tags: len(tags)
        ),
        Node(
            'li',
            filter=None,
            key='companies',
            target=Company,
            nodes=[
                Node('a', key='name'),
                Node('p', key='headquarters'),
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
```