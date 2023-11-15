<a href="https://ik.imagekit.io/egszdsbs2/bluemoss/news.html?updatedAt=1699980898251">
    Download HTML
</a>
<br>
<br>
<img src="https://ik.imagekit.io/egszdsbs2/bluemoss/news.png?updatedAt=1699980723600" alt="">

<br>

# Goal - Scrape all news-article-previews

### Step 1 - Identify data points to scrape

Looking at the page, we can easily identify 4 datapoints per article preview:

- url
- date
- title
- topic
- img_url


### Step 2 - Analyze the HTML
Before we can start writing code, we need to understand the structure of the HTML, specifically
the nature of the html tags that contain the data we want to scrape.

#### Step 2.1 - Search HTML for the title of an article-preview

After searching for the string *"San Francisco Police"* which is part of the title of an article on the reuters home page,
we can see that the article preview is wrapped in a *li* tag, as are all other article previews:

```html
<li class="story-collection__story__LeZ29 story-collection__default__G33_I story-collection__with-spacing__1E6N5" data-testid="four_columns" id="R2AE2PCAWFKADP6LXQUOJBT6FM">
   <div class="media-story-card__hub__3mHOR story-card" data-testid="MediaStoryCard" jw_key="JoXo2VMr">
    <div class="media-story-card__placement-container__1R55-">
     <a aria-hidden="true" href="/world/us/san-francisco-police-fatally-shoot-driver-car-that-crashed-into-chinese-2023-10-10/" tabindex="-1">
      <div class="media-story-card__image-container__gQPAN">
       <div class="image" data-testid="Image">
        <div class="styles__image-container__skIG1 styles__cover__2dX1S styles__center_center__1AaPV styles__apply-ratio__1_FYQ styles__transition__1DEuZ" style="--aspect-ratio: 1.5;">
         <img alt="Law enforcement members stand on the street near the Chinese consulate in San Francisco, where local media has reported a vehicle may have crashed into the building" height="4333" sizes="(min-width: 746px) 320px, (max-width: 745px) 100vw" src="https://cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg" srcset="https://www.reuters.com/resizer/OrGWJq60G7F0lRxsOJPAYfTkxGM=/120x0/filters:quality(80)/cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg 120w,https://www.reuters.com/resizer/88GbZIuIZfdF9MIpruHI11qLezs=/240x0/filters:quality(80)/cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg 240w,https://www.reuters.com/resizer/ucyWVU-ISTF9p5mbY0IMA4BELVg=/480x0/filters:quality(80)/cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg 480w,https://www.reuters.com/resizer/wwaeVEzJf7AGsUCKX2Ht9u6ULKA=/960x0/filters:quality(80)/cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg 960w" width="6500"/>
        </div>
       </div>
       <div class="media-story-card__media__27Yc8 media__symbol__1-WHq media__corner__-C897" data-testid="Media">
        <svg aria-labelledby="react-aria1488270236-:r11:" role="img" viewbox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
         <title id="react-aria1488270236-:r11:">
          article with video
         </title>
         <path d="m15.499 9.173-14-9.022C1.2-.05.8-.05.5.15c-.3.1-.5.4-.5.802v18.045c0 .4.2.701.5.902.2.1.3.1.5.1s.4-.1.5-.2l14-9.023c.3-.201.5-.502.5-.802 0-.301-.2-.702-.5-.803l-.001.001ZM2 17.193V2.757L13.2 9.975 2 17.193Z" role="presentation">
         </path>
        </svg>
       </div>
      </div>
     </a>
    </div>
    <div class="media-story-card__body__3tRWy">
     <span class="text__text__1FZLe text__dark-grey__3Ml43 text__light__1nZjX text__extra_small__1Mw6v label__label__f9Hew label__kicker__RW9aE media-story-card__section__SyzYF" data-testid="Label">
      <a class="text__text__1FZLe text__inherit-color__3208F text__inherit-font__1Y8w3 text__inherit-size__1DZJi link__underline_on_hover__2zGL4" data-testid="Link" href="/world/us/">
       United States
       <span style="border: 0px; clip: rect(0px, 0px, 0px, 0px); clip-path: inset(50%); height: 1px; margin: -1px; overflow: hidden; padding: 0px; position: absolute; width: 1px; white-space: nowrap;">
        category
       </span>
      </a>
     </span>
     <h3 class="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_6__1qUJ5 heading__base__2T28j heading__heading_6__RtD9P" data-testid="Heading">
      <a class="text__text__1FZLe text__dark-grey__3Ml43 text__inherit-font__1Y8w3 text__inherit-size__1DZJi link__underline_on_hover__2zGL4 media-story-card__heading__eqhp9" data-testid="Link" href="/world/us/san-francisco-police-fatally-shoot-driver-car-that-crashed-into-chinese-2023-10-10/">
       San Francisco police fatally shoot driver of car that crashed into Chinese consulate
      </a>
     </h3>
     <time class="text__text__1FZLe text__inherit-color__3208F text__regular__2N1Xr text__extra_small__1Mw6v label__label__f9Hew label__small__274ei media-story-card__time__2i9EK" data-testid="Label" datetime="2023-10-10T02:50:40Z">
      4:50 AM GMT+2 · Updated 34 min ago
     </time>
    </div>
   </div>
</li> 
```


### Step 3 - Create a dataclass to represent an article-preview

```python
# examples/reuters/classes.py

from bluemoss import Jsonify
from dataclasses import dataclass


@dataclass
class ArticlePreview(Jsonify):
    url: str
    date: str
    title: str
    topic: str
    img_url: str
```

### Step 4 - Build the Node object to scrape all article previews

```python
# node.py

from bluemoss import Node, Ex
from examples.reuters.classes import ArticlePreview


ARTICLE_PREVIEW_NODE: Node = Node(
    filter=None,
    xpath="li[contains(@class, 'story-collection')]/div[contains(@class, 'media-story-card')]",
    target=ArticlePreview,
    nodes=[
        Node(
            xpath='a',
            key='url',
            extract=Ex.HREF_ENDPOINT,
            transform=lambda endpoint: f'https://reuters.com{endpoint}',
        ),
        Node(key='date', xpath='time'),
        Node(key='title', xpath='h3/a'),
        Node(key='img_url', xpath='img', extract='src'),
        Node(key='topic', xpath='span/a', extract=Ex.TEXT),
    ],
)
```

### Step 5 - Scrape the HTML / Test the Node object
```python
# main.py

from bluemoss import scrape
from examples.reuters.node import NEWS_PAGE_NODE
from examples.reuters.classes import ArticlePreview


with open('./static/reuters.html', 'r') as f:
    previews: list[ArticlePreview] = scrape(NEWS_PAGE_NODE, f.read())
    print(previews)
```

```json
// the print output

[
    {
        "url": "https://reuters.com/world/middle-east/hamas-official-says-group-is-open-discussions-over-truce-with-israel-2023-10-09",
        "date": null,
        "title": "Hamas official says group is open to discussions over truce with Israel",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/OHKPUTT6SVIINPGQUTXQMLPF5A.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/how-israel-was-duped-hamas-planned-devastating-assault-2023-10-08",
        "date": "October 9, 2023",
        "title": "How Hamas duped Israel as it planned devastating attack",
        "topic": null,
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/OHFKGCVG6FJWZJZAAJ34IWMMPM.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/hamas-threatens-kill-captives-if-israel-strikes-civilians-2023-10-09",
        "date": "5:15 AM GMT+2 \u00b7 Updated 9 min ago",
        "title": "Hamas threatens to kill captives if Israel strikes civilians",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/OHKPUTT6SVIINPGQUTXQMLPF5A.jpg"
    },
    {
        "url": "https://reuters.com/world/do-not-get-involved-israel-crisis-top-us-general-warns-iran-2023-10-10",
        "date": "3:10 AM GMT+2",
        "title": "Do not get involved in Israel crisis, top U.S. general warns Iran",
        "topic": "World",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/V7ZJDY2INZPBJAVAADOQQGSFE4.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/iran-prisoner-swap-6-billion-spotlight-after-hamas-attacks-israel-2023-10-09",
        "date": "October 9, 2023",
        "title": "Iran prisoner swap for $6 billion in spotlight after Hamas attacks Israel",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/QFQ6M762PFKDLJIYRJCVXGKHNY.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/israeli-military-says-its-troops-killed-gunmen-who-infiltrated-lebanon-2023-10-09",
        "date": "1:35 AM GMT+2",
        "title": "Israel kills three Lebanon militants; Israeli officer killed in raid",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/XQIBLHPCCVPDTKK33HWAU3YFQ4.jpg"
    },
    {
        "url": "https://reuters.com/world/us/san-francisco-police-fatally-shoot-driver-car-that-crashed-into-chinese-2023-10-10",
        "date": "4:50 AM GMT+2 \u00b7 Updated 34 min ago",
        "title": "San Francisco police fatally shoot driver of car that crashed into Chinese consulate",
        "topic": "United States",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/3DSZHMD3NFP2FMVBS2IQHBGP6M.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/israel-palestinian-war-what-you-need-know-right-now-2023-10-09",
        "date": "October 9, 2023",
        "title": "Israel and Palestinian war: What you need to know right now",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/MHRIM7FSGZIGBPSMCDB3NNYEG4.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/israel-retaliates-after-hamas-attacks-deaths-pass-1100-2023-10-09",
        "date": "October 9, 2023",
        "title": "Israel on war footing, Hamas threatens to kill captives",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/OKORXMAR45KXPN2ARSALBZS3I4.jpg"
    },
    {
        "url": "https://reuters.com/world/germany-austria-suspend-bilateral-aid-palestinians-after-hamas-attack-2023-10-09",
        "date": "October 9, 2023",
        "title": "EU backtracks on Palestinian aid freeze over Hamas attack",
        "topic": "World",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/ZIKVM4WHJZOOPOJEBPMKMPL2R4.jpg"
    },
    {
        "url": "https://reuters.com/world/us/biden-interviewed-by-special-counsel-classified-documents-case-2023-10-09",
        "date": "2:55 AM GMT+2",
        "title": "Biden interviewed by special counsel in classified documents case",
        "topic": "United States",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/XURURDYC2FL57CN3C6Y3XJJEPE.jpg"
    },
    {
        "url": "https://reuters.com/world/us/pro-palestinian-letter-harvard-students-provokes-alumni-outrage-2023-10-10",
        "date": "3:23 AM GMT+2",
        "title": "Pro-Palestinian letter from Harvard students provokes alumni outrage",
        "topic": "United States",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/F6EKG62LRROZBMVD7KPA2A7NHM.jpg"
    },
    {
        "url": "https://reuters.com/world/israel-hamas-war-forces-biden-netanyahu-into-uneasy-partnership-2023-10-09",
        "date": "October 9, 2023",
        "title": "Israel-Hamas war forces Biden and Netanyahu into uneasy partnership",
        "topic": "World",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/JRYZVME5CNNKDERQ6B4PWTCARY.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/hamas-deployed-specialised-units-attack-israel-says-source-2023-10-09",
        "date": "October 9, 2023",
        "title": "Hamas deployed specialised units to attack Israel, says source",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/HTBBGH4QGFJETDP2JEJKAQ7ZMM.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/qatar-leads-talks-swap-hamas-held-hostages-palestinians-israeli-jails-2023-10-09",
        "date": "October 9, 2023",
        "title": "Qatar in talks with Hamas, Israel to swap hostages for prisoners",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/7CIKA7TUABLPBOKCMOGWPQBRGM.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/israel-hamas-war-latest-news-market-response-business-impact-2023-10-09",
        "date": "3:17 AM GMT+2",
        "title": "Israel-Hamas war: Latest news, market response and foreign aid",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/5F45TGWKDZLZTP5QSR72UFJXFY.jpg"
    },
    {
        "url": "https://reuters.com/world/us/chinese-consulate-san-francisco-says-attacked-by-violent-vehicle-crash-2023-10-10",
        "date": "4:18 AM GMT+2",
        "title": "Chinese consulate in San Francisco says attacked by 'violent' vehicle crash",
        "topic": "United States",
        "img_url": null
    },
    {
        "url": "https://reuters.com/world/middle-east/netanyahu-says-israels-response-gaza-attack-will-change-middle-east-2023-10-09",
        "date": "October 9, 2023",
        "title": "Netanyahu says Israel's response to Gaza attack will 'change the Middle East'",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/TSCRWCFPJRK3PMV74RC3D7FSTM.jpg"
    },
    {
        "url": "https://reuters.com/world/middle-east/fact-checking-online-misinformation-israel-hamas-conflict-2023-10-09",
        "date": "October 9, 2023",
        "title": "Israel-Hamas war: Fact-checking online misinformation",
        "topic": "Middle East",
        "img_url": "https://cloudfront-us-east-2.images.arcpublishing.com/reuters/5F45TGWKDZLZTP5QSR72UFJXFY.jpg"
    }
]

```