<style>
    ul {
        padding-left: 25px;
    }
    li {
        margin-bottom: 10px;
    }
</style>

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
<hr>

## Getting Started

```bash
pip install bluemoss
```

<br>
<hr>


## What is bluemoss?

Step into the world of web scraping with **bluemoss**, where you get the precision of XPath 1.0 without the steep learning
curve. Our `Node` class acts as the blueprint for scraping any website, turning complex HTML into neatly 
organized data-structures like JSON, class instances, and more.
<br>
<br>
Forget about piecing together an array of functions for each HTML tag you want to scrape
— Bluemoss lets you craft a single `Node` object that does it all: 
scraping, transforming, and structuring website data seamlessly, into the data format you need.
<br>
<br>
And if you are new to XPath, no problem — ChatGPT has got your back to help kick off those initial queries.
<br>
<br>

<hr>


## How does it work?

This section will show you how you can use bluemoss to scrape websites.
For all examples that follow, let's consider the following html as the document we want to scrape.


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
                    <p>Cupertino</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                <a href="/portfolio?company=google">
                    Google
                </a>
                <div class="location_us">
                    <p>Mountain View</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                 <a href="/portfolio?company=tesla">
                    Tesla
                </a>
                <div class="location_us">
                    <p>Austin</p>
                </div>
            </div>
        </li>

        <li>
            <div>
                <a href="/portfolio?company=deepmind">
                    DeepMind
                </a>
                <div class="location_uk">
                    <p>London</p>
                </div>
            </div>
        </li>
    </body>
</html>
```

<br>
<br>

### Example 1

**Goal** - Scrape the text within the first a-tag: "Apple"

The Node object defined below tells the scrape function to find the first a-tag and extract the text it contains.

```python
from .constants import HTML
from bluemoss import Node, scrape


node = Node('a')

scrape(node, HTML) == 'Apple'
```

<br>
<br>

### Example 2

**Goal** - Scrape the very first company headquarters: "Cupertino"

```python
node = Node('p')

scrape(node, HTML) == 'Cupertino'
```

`Pro Tip: Good Node objects have a short xpath argument.`

<br>
<br>

### Example 3

**Goal** - Scrape the second company headquarters which are located in the US

```python
node = Node('div[contains(@class, "location_")]', filter=1)

scrape(node, HTML) == 'Mountain View'
```

`Pro Tip: Learning XPath is easy and fast with ChatGPT. Bluemoss supports XPath 1.0.`

This example introduces the **filter** argument which determines which of those tag(s) that match the xpath locator
will be scraped. The default value for the **filter** arg is 0 (index 0), which will scrape the very first (index 0)
tag that matches the given xpath. Our goal for this example was to extract the text of the second tag (index 1) 
that matches our xpath, therefor we set **filter = 1**.

<br>
<br>

### Example 4

**Goal** - Scrape **ALL** company headquarters which are located in the US

```python
node = Node('div[contains(@class, "location_")]', filter=None)

scrape(node, HTML) == ['Cupertiino', 'Mountain View', 'Austin']
```

Setting **filter=None** will filter for all tags matched against the given xpath.

<br>
<br>

### Example 5

**Goal** - Scrape the first and third company names.

```python
Node('a', filter=[0, 2])

scrape(node, HTML) == ['Apple', 'Google']
```

In this example we set the **filter** arg a list of ints. Those int values refer to the first and third index (0 and 2).

<br>
<br>

### Example 6

**Goal** - Scrape all company names from index 1 onwards in multiple different ways

The expected scrape result is

```python
['Google', 'Tesla', 'DeepMind']
```

<br>

```python
from bluemoss import Node, Range


Node('a', filter=Range(1))  # match all a-tags from index 1 onwards

Node('li//a', filter=Range(1)) # The xpaths 'a' and 'li//a' match the same tags in our html doc

Node('li/div/a', filter=Range(1))  # 'li/div/a' is just another xpath matching the same tags in our html doc

Node('a', filter=[1, 2, 3])  # the index list [1, 2, 3] will achieve the same result as Range(1)

Node('a', filter=Range(1, 4))  # the Range class accepts a second int argument (the stop index)
```

<br>
<br>

### Example 7

**Goal** - Scrape all company names from index 1 onwards in reverse order, and do it in 3 different ways.

The expected scrape result is

```python
['DeepMind', 'Tesla', 'Google']
```

<br>

```python
Node('a', filter=Range(1, reverse=True))  # set reverse to True

Node('a', filter=Range(1, 4, reverse=True)) # set reverse to True

Node('a', filter=Range(1), transform=lambda res: res[::-1])  # use the transform arg
```

The first two examples simply set the **reverse** arg of the Range object to True.
The last example uses a different approach. It introduces the **transform** arg of the Node class.

The transform function is the function being executed once
-  the tags were matched with the given xpath
-  the matched tags were further filtered

`Pro Tip: The transform function defines the last step in scraping.`

<br>
<br>

### Example 8

**Goal** - Scrape the last two company names and store the result in a dict under the key 'companies'

```python
Node('a', filter=[-2, -1], key='companies')

scrape(node, HTML) == {'companies': ['Tesla', 'DeepMind']}
```

<br>

### Example 9

**Goal** - Scrape the first company name and store the result in a dict under the key 'companies'

```python
Node('a', key='companies')

scrape(node, HTML) == {'companies': 'Tesla'}
```

<br>

### Example 10

**Goal** - Scrape the first company id in 3 different ways. 
<br>
<br>What is the company id? Every a-tag in our html doc defines an href property.
The first a-tag declares the href */portfolio?company=apple*, and we regard the company-id to be the value of the **company** 
key extracted from the href-query-string. Therefor, in our html doc, the first company-id is **apple**, which is the value we expect to extract.


Let us first define a helper function that will receive the href-value as an argument and return the company id:
```python
def get_company_id(href: str) -> str:
    return href.split('=')[-1]
```

#### Solution 10.1
```python
from src.bluemoss import Node, Ex


# Declare the tag-property to be extracted by using the 'extract' arg.
# Introducing the 'Ex' Enum which provides handy types of extraction.

Node('a', extract=Ex.HREF, transform=get_company_id)
```

#### Solution 10.2
```python
# The 'extract' arg also accept string values.

Node('a', extract='href', transform=get_company_id)
```

#### Solution 10.3
```python
Node('a/@href', transform=get_company_id)  # use xpath to extract the href property value
```

<br>

### Example 11 - Scraping multiple tags

**Goal** - Scrape the name and headquarters of every company.

The expected result:
```python
[
    ['Apple', 'Cupertino'],
    ['Google', 'Mountain View'],
    ['Tesla', 'Austin'],
    ['DeepMind', 'London']
]
```


Solution
```python
Node(
    'li',  # match 'li' tags
    filter=None,  # scrape all the matched 'li' tags
    nodes=[
        Node('a'),  # within the 'li' tag, match the first 'a' tag and extract the text
        Node('p')  # within the 'li' tag, match the first 'p' tag and extract the text
    ]
)
```

`Pro Tip: The **nodes** arg let's you scrape multiple tags within a tag.`

<br>


### Example 12

**Goal** - Scrape the name and headquarters of every company, where each item in the result list is a dict.


The expected result:
```python
[
    {'name': 'Apple', 'location': 'Cupertino'},
    {'name': 'Google', 'location':  'Mountain View'},
    {'name': 'Tesla', 'location':  'Austin'},
    {'name': 'DeepMind', 'location':  'London'}
]
```


Solution
```python
Node(
    'li', 
    filter=None,
    nodes=[
        Node('a', key='name'),
        Node('p', key='location')
    ]
)
```

`Pro Tip: All Nodes in a nodes list either define the 'key' arg or none of them do.`

<br>

### Example 13 - Building class instances

**Goal** - In this last example, we want to scrape the name and location of every company, 
as well as the total amount of companies located in the US and UK. We also want to store the scraped data 
not in a dict or list as we did in the previous examples, but instead want to store the data in dataclass instances.

**Info** - The code snippet below shows that we assume a dataclass called **Companies** in which we will store the 
entire scrape-result. The expected result also assumes, that the **Companies** instance exposed two properties 
**dict** and **json**

```python
# expected result

companies: Companies = scrape(node, HTML)

companies.dict == {
    'companies': [
        {'name': 'Apple', 'location': 'Cupertino'},
        {'name': 'Google', 'location': 'Mountain View'},
        {'name': 'Tesla', 'location': 'Austin'},
        {'name': 'DeepMind', 'location': 'London'},
    ],
    'amount_uk_companies': 1,
    'amount_us_companies': 3,
}

companies.json == """{
    "companies": [
        {
            "name": "Apple",
            "location": "Cupertino"
        },
        {
            "name": "Google",
            "location": "Mountain View"
        },
        {
            "name": "Tesla",
            "location": "Austin"
        },
        {
            "name": "DeepMind",
            "location": "London"
        }
    ],
    "amount_uk_companies": 1,
    "amount_us_companies": 3
}"""
```

```python
# solution

from dataclasses import dataclass
from bluemoss import Node, Jsonify


@dataclass
class Company(Jsonify):
    name: str
    location: str


@dataclass
class Companies(Jsonify):
    companies: list[Company]
    amount_uk_companies: int
    amount_us_companies: int
    
    @property
    def total_amount_companies(self) -> int:
        return self.amount_us_companies + self.amount_uk_companies


Node(
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
                Node('p', key='location')
            ]
        )
    ]
)
```

The solution in the code snippet introduces two new things:
- The **Node.target** parameter allows us to specify what class or dataclass to use in order 
to store the data scraped in the **Node.nodes** list. If a Node instance sets a **target**, then all instances in
Node.nodes must set their **key** parameter and every key must map to one of the init parameters of **Node.target**.
- The **Jsonify** class exposes the two properties **dict** and **json**. It therefor makes it easy transform the 
scraped data stored in dataclass instances into a Python dict or json string.

<br>

`Pro Tip: The Jsonify class will exclude any parameters starting with an underscore "_" from appearing in the return of
the .dict and .json properties. This enables us to hide certain parameters from appearing in those returns.`

<br>

#### Why store the scrape result in a dataclass?
- **type safety** - Dataclass instances as used in this example enforce typed parameters.
- **properties** - Sometimes we want our data transformations to take place inside the dataclass, e.g. through properties. Properties provide a simple way to derive data from the instance parameters of a class instance. By moving the data transformation step from the **Node.transform** parameter to a **dataclass property**, we make the transformation explicitly available to the dataclass.
- **post_init** - The __post_init__ method that is available in Python dataclasses is yet another nice step to manipulate the instance parameters and therefore move the data transformation step partially or as a whole from the **Node.transform** parameter to the __post_init__ method of the dataclass.


<br>
<hr>


### Supported Platforms

- Linux
- MacOS
- Windows

<br>
<hr>


### Supported Python Versions

- 3.9
- 3.10
- 3.11
- 3.12

<br>
<hr>


### License

- Apache 2.0

<br>
<hr>