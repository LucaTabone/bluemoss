<p align="center">
  <h1 align="center">bluemoss</h1>
  <h3 align="center">scrape the web</h3>
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

<hr>

## Full Documentation
<h4>
    <a href="https://bluemoss.readthedocs.io/en/latest/">Read the docs</a>
</h4>

<hr>


## Introduction

```python
from bluemoss import Node, scrape


node = Node('a')  # extract the text contained in the first a-tag

scrape(node, YOUR_HTML)
```
<br>
With **bluemoss**, you create a `Node` object to scrape data from any website. 
Imagine that `Node` object to be like a recipe 👩‍🍳 which describes what to scrape from which tags, 
and how to transform and structure the scraped data it into the format you need.
<br>
<br>
**bluemoss** uses XPath 1.0 to locate html tags. If you are new to XPath, no problem — <a href="chat.openai.com">ChatGPT</a>
has got your back.
<br>

<hr>

## Examples

This section will show you how can to scrape the web with **bluemoss**.
<br>
For all examples that follow, we are going to scrape the html document below.

```html
<html>
    <body>
        <li>
            <a href="/portfolio?company=apple">
                Apple
            </a>
            <div class="location_us">
                <p>Cupertino</p>
            </div>
        </li>

        <li>
            <a href="/portfolio?company=google">
                Google
            </a>
            <div class="location_us">
                <p>Mountain View</p>
            </div>
        </li>

        <li>
            <a href="/portfolio?company=deepmind">
                DeepMind
            </a>
            <div class="location_uk">
                <p>London</p>
            </div>
        </li>
    </body>
</html>
```

<br>
<hr>

**Example 1** - Scrape the text in the first **a** tag.

The **Node** object below instructs the **scrape** function to find the first *a*-tag and extract the text it contains.

```python
from bluemoss import Node, scrape


node = Node('a')

scrape(node, HTML) == 'Apple'
```

<hr>
<br>

**Example 2** - Scrape the **second** company headquarters which are located in the US

```python
node = Node('div[contains(@class, "location_us")]', filter=1)

scrape(node, HTML) == 'Mountain View'
```

`Pro Tip: Learning XPath is easy and fast with ChatGPT.`

This example introduces the **filter** argument which determines which of those tag(s) that match the xpath locator
will be scraped. The default value for the **filter** arg is 0 (index 0), which will scrape the very first
tag that matches the given xpath. Our goal for this example was to extract the text of the second tag (index 1) 
that matches our xpath, therefor we set **filter = 1**.

<hr>
<br>

**Example 3** - Scrape **ALL** company headquarters which are located in the US

```python
node = Node('div[contains(@class, "location_us")]', filter=None)

scrape(node, HTML) == ['Cupertino', 'Mountain View']
```

Setting **filter=None** will filter for all tags matched against the given xpath.

<hr>
<br>

**Example 4** - Scrape the first and third company names.

```python
Node('a', filter=[0, 2])

scrape(node, HTML) == ['Apple', 'DeepMind']
```

In this example we set the **filter** arg to a list of ints. 
Those int values refer to the first and third index (0 and 2).

<hr>
<br>

**Example 5** - Scrape all company names, but exclude the first one.

The expected scrape result is

```python
['Google', 'DeepMind']

# 'Apple' not included, since it is located in the first a-tag (index 0)
```

<br>
Below are a couple of valid solutions, and the first one is the most recommended one, 
since it keeps the arguments provided to the Node object as simple as possible:

```python
# solution 1, the recommended solution

from bluemoss import Node, Range


Node('a', filter=Range(1)) 

# Range(1) filters the matched tags from index 1 onwards
```

```python
# solution 2


Node('li//a', filter=Range(1))

# the xpaths 'a' and 'li//a' match the same tags in our html doc
```

```python
# solution 3

Node('a', filter=[1, 2])
```

```python
# solution 4

Node('a', filter=Range(1, 3)) 

# The Range class accepts a second int argument (the stop index).
# Range(x, y) filters for the matched tags at indices x, ..., y-1
#   e.g. Range(2, 6) filters for indices 2, 3, 4, 5.
```

<hr>
<br>

**Example 6** - Scrape all company names from index 1 onwards in reverse order.

The expected scrape result is

```python
['DeepMind', 'Google']
```

<br>

```python
# solution 1

Node('a', filter=Range(1, reverse=True))  # set reverse to True
```

```python
# solution 2

Node('a', filter=Range(1), transform=lambda res: res[::-1])  # use transform arg
```

The first two examples simply set the **reverse** arg of the Range object to True.
The last example uses a different approach. It introduces the **transform** arg of the **Node** class.

The transform function is the function being executed after

-  the tags were matched with the given xpath
-  the matched tags were further filtered using the **Node.filter** arg

`Pro Tip: The transform-function defines the last step in computing the scrape-result of a Node object.`

<hr>
<br>

**Example 7** - Scrape the last two company names and store the result **in a dict** under the key 'companies'

```python
Node('a', filter=[-2, -1], key='companies')

scrape(node, HTML) == {'companies': ['Google', 'DeepMind']}
```

In the example above we provide the indexes -2 and -1 to the filter-list as those indices represent the last 
two elements in a Python list.

<hr>
<br>

**Example 8** - Scrape the first company name and store the result **in a dict** under the key 'companies'

```python
Node('a', key='companies')

scrape(node, HTML) == {'companies': 'Apple'}
```

<hr>
<br>

**Example 9** - Scrape the first company-id.

Let us first define a helper function that will receive the href-value as an argument and return the company id:

```python
# helper function to the solutions

def get_company_id(href: str) -> str:
    return href.split('=')[-1]
```
<br>

```python
# solution 1

from src.bluemoss import Node, Ex


Node('a', extract=Ex.HREF, transform=get_company_id)

# Declare the tag-property to be extracted by using the 'extract' arg.
# Introducing the 'Ex' Enum which provides handy types of extraction.
```

```python
# solution 2

Node('a', extract='href', transform=get_company_id)

# The 'extract' arg also accept string values.
```

```python
# solution 3

Node('a/@href', transform=get_company_id)

# We can also just use xpath to extract the href property.
```

<hr>
<br>

**Example 10 - Advanced Scraping** - Scrape the name and headquarters of every company.

The expected result:
```python
[
    ['Apple', 'Cupertino'],
    ['Google', 'Mountain View'],
    ['DeepMind', 'London']
]
```

<br>

```python
# solution 
Node(
    'li',  # match 'li' tags
    filter=None,  # scrape all the matched 'li' tags
    nodes=[
        Node('a'),  # within the 'li' tag, match the first 'a' tag and extract the text
        Node('p')  # within the 'li' tag, match the first 'p' tag and extract the text
    ]
)
```

`Pro Tip: The **nodes** arg let's you scrape multiple different tags within the same parent tag.`

<hr>
<br>

**Example 11 - Advanced Scraping** - 
Scrape the name and headquarters of every company. The result shall be a list of dicts.


The expected result:
```python
[
    {'name': 'Apple', 'location': 'Cupertino'},
    {'name': 'Google', 'location':  'Mountain View'},
    {'name': 'DeepMind', 'location':  'London'}
]
```

<br>

```python
# solution

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

<hr>
<br>

**Example 12 - Advanced Scraping** - In this last example, we want to scrape the name and location of every company, 
as well as the total amount of companies located in the US and UK. We also want to store the scraped data 
not in a dict or list as we did in the previous examples, but instead want to store the data in dataclass instances.

**Info** - The code snippet below shows that we assume a dataclass called **Companies** in which we will store the 
entire scrape-result. The expected result also assumes, that the **Companies** instance exposes two properties 
**dict** and **json**

```python
# expected result

companies: Companies = scrape(node, HTML)

companies.dict == {
    'companies': [
        {'name': 'Apple', 'location': 'Cupertino'},
        {'name': 'Google', 'location': 'Mountain View'},
        {'name': 'DeepMind', 'location': 'London'},
    ],
    'amount_uk_companies': 1,
    'amount_us_companies': 2,
    'amount_companies': 3
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
            "name": "DeepMind",
            "location": "London"
        }
    ],
    "amount_uk_companies": 1,
    "amount_us_companies": 2,
    "amount_companies": 3
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
    def amount_companies(self) -> int:
        return self.amount_us_companies + self.amount_uk_companies
    
    @property
    def dict(self):
        return super().dict | {'amount_companies': self.amount_companies}


Node(
    target=Companies,
    nodes=[
        Node(
            'li',
            filter=None,     # makes sure to filter all matched 'li' tags
            key='companies', # will store the scrape-result as a dict under the key 'companies'
            target=Company,  # the data scraped from every 'li' tag will be transformed into a 'Company' instance
            nodes=[          # every 'Company' instance will be initialized with the parameters 'name' and 'location'
                Node('a', key='name'), # extracts the text from the 'li/a' tag and stores it in the Company.name parameter
                Node('p', key='location')  # extracts the text from the 'li/p' tag and stores it in the Company.location parameter
            ]
        ),
        Node(
            "div[@class='location_uk']",  # finds all 'div' tags whose class property contains the text 'location_uk'
            filter=None,                  # filter all matched tags
            key='amount_uk_companies',    # stores the result in the Companies.amount_uk_companies parameter
            transform=lambda companies: len(companies) # The initial result is a list (due to filter=None) and it 
                                                       # will then be mapped to its length.
                                                       # Therefor the final scrape-result is an int.
        ),
        Node(
            "div[@class='location_us']",
            filter=None,
            key='amount_us_companies',
            transform=lambda companies: len(companies)
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

- **type safety** - Dataclass instances as used in this example enforce typed parameters.
- **properties** - Sometimes we want our data transformations to take place inside the dataclass, e.g. through properties. Properties provide a simple way to derive data from the instance parameters of a class instance. By moving the data transformation step from the **Node.transform** parameter to a **dataclass property**, we make the transformation explicitly available to the dataclass.
- **post_init** - The __post_init__ method that is available in Python dataclasses is yet another nice step to manipulate the instance parameters and therefore move the data transformation step partially or as a whole from the **Node.transform** parameter to the __post_init__ method of the dataclass.


<br>
<hr>


## Supported Platforms

- Linux
- MacOS
- Windows

<br>
<hr>


## Supported Python Versions

- 3.9
- 3.10
- 3.11
- 3.12

<br>
<hr>


## License

- Apache 2.0

<br>
<hr>