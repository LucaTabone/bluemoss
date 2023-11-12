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

### Example 2

**Goal** - Scrape the very first company headquarters: "Cupertino, California"

```python
node = Node('p')

scrape(node, HTML) == 'Cupertino, California'
```

`Pro Tip: Good Node objects have a short xpath argument.`

<br>

### Example 3

**Goal** - Scrape the second company headquarters which are located in the US

```python
node = Node('div[contains(@class, "location_")]', filter=1)

scrape(node, HTML) == 'Mountain View, California'
```

`Pro Tip: Learning XPath is easy and fast with ChatGPT. Bluemoss supports XPath 1.0.`

This example introduces the **filter** argument which determines which of those tag(s) that match the xpath locator
will be scraped. The default value for the **filter** arg is 0 (index 0), which will scrape the very first (index 0)
tag that matches the given xpath. Our goal for this example was to extract the text of the second tag (index 1) 
that matches our xpath, therefor we set **filter = 1**.

<br>

### Example 4

**Goal** - Scrape the first and third company names.

```python
Node('a', filter=[0, 2])

scrape(node, HTML) == ['Apple', 'Google']
```

In this example we set the **filter** arg a list of ints. Those int values refer to the first and third index (0 and 2).

<br>

### Example 5

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