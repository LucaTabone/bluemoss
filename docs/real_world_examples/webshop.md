<a href="https://ik.imagekit.io/egszdsbs2/bluemoss/shoes.html?updatedAt=1699980966489">
    Download HTML
</a>
<br>
<img src="https://ik.imagekit.io/egszdsbs2/bluemoss/shoes.png?updatedAt=1699980726403" alt="">

# Goal - Scrape all shoe items

### Step 1 - Identify data points to scrape

Looking at the page, we can identify the following per item:

- url
- price
- brand
- is_deal
- discount
- image_url
- is_sponsored
- short_description

### Step 2 - Analyze the HTML
Before we can start writing code, we need to understand the structure of the HTML, specifically
the nature of the html tags that contain the data we want to scrape.
<br>
<br>
After searching the page html for keywords that we see on the page, e.g. a product-name, we have identified an 
*article* tag which encapsulates all datapoints of one of the products. And by scrolling further down we see
that all the rendered products are encapsulated by an *article* tag
with the same class property, namely  "*z5x6ht _0xLoFW JT3_zV mo6ZnF _78xIQ-*".
Below you find an excerpt of one of the *article* tags.

```html
<article class="z5x6ht _0xLoFW JT3_zV mo6ZnF _78xIQ-" role="link">
  <div class="xCblER KVKCn3 u-C3dd jDGwVr mo6ZnF KLaowZ rQ5pcU Nx0a9q">
  </div>
  <a class="_LM JT3_zV CKDt_l CKDt_l LyRfpJ" data-card-type="media" href="https://en.zalando.de/puma-future-match-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hx-a11.html" rel="" tabindex="0">
   <figure class="heWLCX">
    <div class="JT3_zV ZkIJC- _9QaS6n IN7Kbz K82if3">
     <div class="KVKCn3 u-C3dd jDGwVr mo6ZnF KLaowZ">
      <img alt="FUTURE MATCH FG/AG - Moulded stud football boots - white/black/fire orchid" class="sDq_FX lystZ1 FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF _7ZONEy" draggable="false" fetchpriority="high" height="433" loading="eager" sizes="(min-width: 1280px) 288px, (min-width: 1024px) calc(25vw - 28px), (min-width: 480px) calc(33vw - 24px), calc(50vw - 30px)" src="https://img01.ztat.net/article/spp-media-p1/ace2265559ad4838b27d66810290a4bd/dbf5f855504849c599fa1089652ee2c4.jpg?imwidth=300&amp;filter=packshot" srcset="https://img01.ztat.net/article/spp-media-p1/ace2265559ad4838b27d66810290a4bd/dbf5f855504849c599fa1089652ee2c4.jpg?imwidth=300&amp;filter=packshot 303w, https://img01.ztat.net/article/spp-media-p1/ace2265559ad4838b27d66810290a4bd/dbf5f855504849c599fa1089652ee2c4.jpg?imwidth=400&amp;filter=packshot 429w, https://img01.ztat.net/article/spp-media-p1/ace2265559ad4838b27d66810290a4bd/dbf5f855504849c599fa1089652ee2c4.jpg?imwidth=500&amp;filter=packshot 605w" width="300"/>
     </div>
    </div>
   </figure>
  </a>
  <div class="KVKCn3 _2dqvZS hN9H_L df4QKn _LM">
   <button aria-label="Add to wish list or remove from wish list" aria-pressed="false" class="BXKCcR r9BRio Md_Vex NN8L-8 heWLCX LyRfpJ VWL_Ot _13ipK_ Vn-7c- _5Yd-hZ W4gxOr XfNx0j tDtVvZ AfQRDc aAbDY2 _ZDS_REF_SCOPE_ WtocDo x7LsVH HlZ_Tf" type="button">
    <span class="olm6i5 JT3_zV _0xLoFW u9KIT8 FCIprz uEg2FS _2Pvyxl">
     <i aria-hidden="true" class="OXFOVc font-1srjmmp I_qHp3" role="presentation" translate="no">
      heart_outlined
     </i>
    </span>
   </button>
  </div>
  <div class="KVKCn3 mo6ZnF KLaowZ nXkCf3 _2dqvZS ZkIJC- u-C3dd jDGwVr" style="height: 416px;">
  </div>
  <div class="_0xLoFW _78xIQ- EJ4MLB f4ql6o JT3_zV" tabindex="-1">
   <div>
    <button class="_ZDS_REF_SCOPE_ _0xLoFW FCIprz q84f1m mo6ZnF" type="button">
     <span class="goVnUa FxZV-M sDq_FX _65i7kZ Yb63TQ">
      Sponsored
     </span>
     <svg aria-hidden="true" class="zds-icon RC794g X9n9TI DlJ4rT _5Yd-hZ goVnUa FxZV-M Yb63TQ" fill="currentColor" focusable="false" height="1em" viewbox="0 0 24 24" width="1em">
      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12c6.624-.008 11.992-5.376 12-12 0-6.627-5.373-12-12-12zm0 22.5C6.201 22.5 1.5 17.799 1.5 12S6.201 1.5 12 1.5c5.796.007 10.493 4.704 10.5 10.5 0 5.799-4.701 10.5-10.5 10.5z">
      </path>
      <circle cx="12" cy="5.6" r="1.1">
      </circle>
      <path d="M12 8.25a.75.75 0 0 0-.75.75v9.75a.75.75 0 1 0 1.5 0V9a.75.75 0 0 0-.75-.75z">
      </path>
     </svg>
    </button>
   </div>
   <a aria-hidden="true" class="CKDt_l LyRfpJ JT3_zV CKDt_l _2dqvZS" href="https://en.zalando.de/puma-future-match-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hx-a11.html" rel="" tabindex="-1">
    <header>
     <div class="Zhr-fS">
      <h3 class="FtrEr_ lystZ1 FxZV-M HlZ_Tf ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2">
       Puma
      </h3>
      <h3 class="sDq_FX lystZ1 FxZV-M HlZ_Tf ZkIJC- r9BRio qXofat EKabf7 nBq1-s _2MyPg2">
       FUTURE MATCH FG/AG - Moulded stud football boots - white/black/fire orchid
      </h3>
     </div>
     <section class="_0xLoFW _78xIQ-">
      <p class="sDq_FX lystZ1 FxZV-M HlZ_Tf">
       <span class="sDq_FX lystZ1 FxZV-M HlZ_Tf">
        From
       </span>
       <span class="sDq_FX lystZ1 FxZV-M HlZ_Tf">
        86,55 €
       </span>
      </p>
     </section>
    </header>
   </a>
  </div>
</article>
```



### Step 3 - Create a dataclass to represent an item in the webshop

```python
# examples/webshop/classes.py

from bluemoss import Jsonify
from dataclasses import dataclass


@dataclass
class Article(Jsonify):
    url: str
    brand: str
    img_url: str
    discount: str
    is_deal: bool
    is_sponsored: bool
    short_description: str
    _price_text: str
```

### Step 4 - Build the Node object to scrape all articles

```python
# examples/webshop/node.py

from bluemoss import Ex, Node
from examples.webshop.classes import Article


node: Node = Node(
    filter=None,
    target=Article,
    xpath="article[contains(@class, 'z5x6ht')]",
    nodes=[
        Node(key='brand', xpath='h3'),
        Node(key='img_url', xpath='img/@src'),
        Node(key='url', xpath='a', extract=Ex.HREF),
        Node(key='_price_text', xpath='p/span', filter=-1),
        Node(key='short_description', xpath='h3', filter=-1),
        Node(key='discount', xpath="span[contains(@class, 'Km7l2y r9BRio')]"),
        Node(
            key='is_deal',
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, 'DJxzzA') and contains(text(), 'Deal')]",
        ),
        Node(
            key='is_sponsored',
            extract=Ex.BS4_TAG,
            transform=lambda tag: tag is not None,
            xpath="span[contains(@class, '_65i7kZ') and contains(text(), 'Sponsored')]",
        ),
    ],
)
```

### Step 5 - Scrape the HTML / Test the Node object
```python
# main.py

from bluemoss import scrape
from examples.webshop.classes import Article
from examples.webshop.node import ARTICLES_NODE


with open('./static/webshop.html', 'r') as f:
    posts: list[Article] = scrape(ARTICLES_NODE, f.read())
    print(posts)
```

```json
// the print output  (108 articles scraped)

[
    {
        "url": "https://en.zalando.de/puma-future-match-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hx-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ace2265559ad4838b27d66810290a4bd/dbf5f855504849c599fa1089652ee2c4.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "FUTURE MATCH FG/AG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-match-energy-fgag-moulded-stud-football-boots-luminous-pinkyellow-alertultra-blue-pu142a1ik-j11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/38ec314bed7f4b12a06c9d2c58b0788f/fbed77485c2c4a8f97eaffcb0bbd7c4b.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "ULTRA MATCH ENERGY FG/AG - Moulded stud football boots - luminous pink/yellow alert/ultra blue"
    },
    {
        "url": "https://en.zalando.de/puma-future-ultimate-energy-fgag-moulded-stud-football-boots-ultra-blueyellow-alertluminous-pink-pu142a1hi-k11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/7eb5fe935567465fa4103b502a83f688/71c67e2e655c40ea8da9b1792047aaec.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "FUTURE ULTIMATE ENERGY FG/AG - Moulded stud football boots - ultra blue/yellow alert/luminous pink"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-academy-sg-pro-ac-unisex-screw-in-stud-football-boots-blackchromehyper-royal-n1242a2f5-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/1b7483106a5442ac858e902b0ae90a42/bdf785b1cf6a4553b6f71ff2e8026ca4.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL 9 ACADEMY SG-PRO ANTI CLOG TRACTION - Screw-in stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-gx-academy-df-fgmg-moulded-stud-football-boots-bright-crimsonblackwhite-n1242a2iw-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2758af70851441d6baa4cb94cf7a3bfe/8f1310e75a7f4afda4ae01fa19b2f3a4.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 ACADEMY DF FG/MG - Moulded stud football boots - bright crimson/black/white"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-mxsg-screw-in-stud-football-boots-blacksilver-pu142a1ig-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/0c9fb09b1f04457393fe637ca7358fea/dec20387bf684e438da2f83f960938b8.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "Screw-in stud football boots - black/silver"
    },
    {
        "url": "https://en.zalando.de/new-balance-fresh-foam-x-more-neutral-running-shoes-quartz-grey-ne242a0hg-h11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2fdddc14742e4ce9ab75d72b530bde64/ab151fffb2a042f2908e607d534652b0.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM X MORE V4 - Neutral running shoes - quartz grey"
    },
    {
        "url": "https://en.zalando.de/new-balance-fresh-foam-trail-more-v3-trainers-white-ne242a0kw-a11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/56ba5f1672f445d3b972cbf3fc7489cc/f5f29e26b58940cdb96a43afbd7b4ed8.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM X MORE TRAIL V3 - Trail running shoes - white"
    },
    {
        "url": "https://en.zalando.de/new-balance-fresh-foam-garoe-trail-running-shoes-hot-marigold-ne242a0la-q11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/8e19b0869c954aa89c8da3c906a7aff6/b48d4973ebe743fdb4e2c95f1d9dfb8b.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM GARO\u00c9 - Trail running shoes - hot marigold"
    },
    {
        "url": "https://en.zalando.de/new-balance-fresh-foam-x-1080v12-neutral-running-shoes-black-ne242a0kn-q11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/df1f869cb87e4caa918ff84200b1689e/82bcae35b6ee450a871fe7b34d52f74b.jpg?imwidth=300&filter=packshot",
        "discount": "-20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM X 1080V12 - Neutral running shoes - black"
    },
    {
        "url": "https://en.zalando.de/new-balance-fuelcell-propel-v4-neutral-running-shoes-whitemulti-coloured-ne242a0j5-a13.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/d4ce04a4dfe348e48125433d3d7df39c/2fa2c163c33c4d2b9b67a910b06e9788.jpg?imwidth=300&filter=packshot",
        "discount": "up to -25%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUELCELL PROPEL V4 - Neutral running shoes - white/multi-coloured"
    },
    {
        "url": "https://en.zalando.de/new-balance-fresh-foam-x-1080v12-neutral-running-shoes-mercury-blue-ne242a0kn-k11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/5c7772f7fe6343cea889c1aa0d9d93c8/5d9b8a5b6bf34c699bb251ff8e97e230.jpg?imwidth=300&filter=packshot",
        "discount": "-10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM X 1080V12 - Neutral running shoes - mercury blue"
    },
    {
        "url": "https://en.zalando.de/new-balance-fuelcell-propel-v4-neutral-running-shoes-sea-salt-ne242a0j5-a12.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/1767fe3afec640359a38c5009d169326/b35e600a3a5f4603b06414d36635e1f9.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUELCELL PROPEL V4 - Neutral running shoes - sea salt"
    },
    {
        "url": "https://en.zalando.de/new-balance-trainers-cayenne-ne242a0hy-h11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/b5af13c19c2d40ecb11f345af54eaf8b/19e11c9f4763412cbaa09116f8110e7f.jpg?imwidth=300&filter=packshot",
        "discount": "-25%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FRESH FOAM X HIERRO V7 - Trail running shoes - cayenne"
    },
    {
        "url": "https://en.zalando.de/new-balance-fuelcell-rebel-v3-neutral-running-shoes-neon-dragonfly-ne242a0h9-q12.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/e1be054b32e6467a8275b06d06128f37/f9b54448fae94b949bc210668cd95a7d.jpg?imwidth=300&filter=packshot",
        "discount": "-20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUELCELL REBEL V2 - Neutral running shoes - neon dragonfly"
    },
    {
        "url": "https://en.zalando.de/new-balance-fuelcell-summit-v3-trail-running-shoes-yellow-ne242a0j6-e11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/68d27741a0cb48108ccd15e61ef50024/eff723880ec44f6590cce5619f95d665.jpg?imwidth=300",
        "discount": "up to -23%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "MENS UNKNOWN - Trail running shoes - yellow"
    },
    {
        "url": "https://en.zalando.de/new-balance-fuelcell-summit-unknown-v4-trail-running-shoes-high-desert-ne242a0l6-o11.html",
        "brand": "New Balance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/dd44389f6dff4df3a2b55d78b53f3324/2916609cf0a6462dad60cd5f86f98c08.jpg?imwidth=300&filter=packshot",
        "discount": "-20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUELCELL SUMMIT UNKNOWN V4 - Trail running shoes - high desert"
    },
    {
        "url": "https://en.zalando.de/nike-performance-mercurial-9-club-mg-moulded-stud-football-boots-bright-crimsonwhiteblack-n1242a2f4-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6ecaacf0b2a845baafdd9ba31f0a4031/ea585e319404422d8771eb5a7748e82a.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MERCURIAL 9 CLUB MG - Moulded stud football boots - bright crimson/white/black"
    },
    {
        "url": "https://en.zalando.de/nike-performance-mercurial-9-club-fgmg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2f4-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/fa51f232b3b24daf97eee5a60a4702e1/88b96221e24344e79e4d3a7f79cf81cf.jpg?imwidth=300&filter=packshot",
        "discount": "-10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "MERCURIAL 9 CLUB MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-tiempo-legend-10-club-mg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2lj-q11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ddb35c8782e74e479c37ebd22df86d9a/f0166be678b04e9e94504ad208bfc5a2.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "LEGEND 10 CLUB FG/MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/collections/ICSIfJewQDe/",
        "brand": "with Altra shoes",
        "img_url": "https://img01.ztat.net/crt/creative-content/6fe212eb-7fe3-4d18-ba3f-c2cdc326b2ce.jpg?imwidth=300",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "with Altra shoes"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-predator-accuracy3-laceless-fg-moulded-stud-football-boots-core-blackfootwear-white-ad542a4rv-q12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/3f53b6456bdc482382bfba9a0dc418c2/78d19771322340c0b01c55384569f712.jpg?imwidth=300&filter=packshot",
        "discount": "up to -25%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PREDATOR ACCURACY 3 FG - Moulded stud football boots - core black/footwear white"
    },
    {
        "url": "https://en.zalando.de/nike-performance-legend-10-club-mg-moulded-stud-football-boots-whiteblackbright-crimson-n1242a2lj-a11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/8c7e68652e2b48799289e26bfcba73a8/aaa893f2ce114e82a8b7f07bf43ed7ce.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "LEGEND 10 CLUB FG/MG - Moulded stud football boots - white/black/bright crimson"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-gx-pro-fg-moulded-stud-football-boots-bright-crimsonblackwhite-n1242a2j5-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/c78277bd1c2d44e2a3a68cf6ae1c51ec/34436b6a4bb04c8b93c4c1835b9caa04.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 PRO FG - Moulded stud football boots - bright crimson/black/white"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-predator-accuracy-3-fg-moulded-stud-football-boots-core-blackcloud-white-ad542a4sd-q12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2b629e2e26f74cc3bdad34831b6feda7/4a76209c5e2e4f0d90f5409d989c7eea.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PREDATOR ACCURACY 3 FG - Moulded stud football boots - core black/cloud white"
    },
    {
        "url": "https://en.zalando.de/puma-future-pro-fgag-moulded-stud-football-boots-fire-orchidinky-blue-pu142a1i7-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/4b201ea7fdac493594576827d6778a3d/77e45c7535444988bdb13437ab747dbe.jpg?imwidth=300&filter=packshot",
        "discount": "up to -11%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE PRO FG/AG - Moulded stud football boots - fire orchid/inky blue"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-copa-pure4-fxg-moulded-stud-football-boots-core-black-ad542a4ti-q12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/5312d400ddad49a1a54c99dc5f2f3d87/2cc933166cc647478ec0bfab907ea421.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "COPA PURE 4 FXG - Moulded stud football boots - core black"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-play-fgag-moulded-stud-football-boots-fire-orchidinky-blue-pu142a1hh-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/b52c5be4a77f4b09833cac833d002751/3dd396643795403ebf4a065f93c5f11f.jpg?imwidth=300&filter=packshot",
        "discount": "up to -11%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA PLAY FG/AG - Moulded stud football boots - fire orchid/inky blue"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-match-laceless-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hm-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/d83039c58aa342f59710baa25cda4a66/e3b7c8b1b06b45e686567775ecb2b847.jpg?imwidth=300&filter=packshot",
        "discount": "up to -30%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA MATCH+ LL FG/AG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-match-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hq-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/f824493040c0439685eac467863bf3f5/531cdfdaf353477ea2aaeb6f368ee955.jpg?imwidth=300&filter=packshot",
        "discount": "up to -25%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA MATCH FG/AG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-fgag-moulded-stud-football-boots-blacksilver-pu142a1hx-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/cdea2ef6047945d08e6d031c169f230a/03cf61176a1043fcbf83d843818eef7b.jpg?imwidth=300&filter=packshot",
        "discount": "up to -11%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE MATCH FG/AG - Moulded stud football boots - black/silver"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-academy-mg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2fd-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/74e4dfb651334a6faac275a97bc64584/a080e6ddc218449db96ed57faf26060b.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL 9 ACADEMY MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-energy-fgag-moulded-stud-football-boots-ultra-blueyellow-alertluminous-pink-pu142a1i9-k11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/4f11ddb2dd6042708052aebc9194abc0/ec281be998f54f3691783b51bcb7a33c.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "FUTURE MATCH ENERGY FG/AG - Moulded stud football boots - ultra blue/yellow alert/luminous pink"
    },
    {
        "url": "https://en.zalando.de/campaigns/rituals-the-artists-of-a-soulful-life-2/",
        "brand": "Rituals",
        "img_url": "https://mosaic03.ztat.net/crt/creative-content/98362cf2-2f33-4a57-bbe1-a4748da69760.gif?imwidth=300",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "Rituals"
    },
    {
        "url": "https://en.zalando.de/nike-performance-moulded-stud-football-boots-guava-ice-black-n1244a0ig-h11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/480d61ccf30549b6a08d8d8c45dadc34/d0c4d1efdb2846379dc9cdc703ff248c.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MERCURIAL VAPOR ZOOM 15 ACADEMY FG/AG - Moulded stud football boots - guava ice black"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-gx-pro-dynamic-fit-fg-moulded-stud-football-boots-bright-crimsonblackwhite-n1242a2j8-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/bcd8a5e7c63a47f9ba481bbdf9d7223c/25dcb601bf464d619af6a29c18d5add1.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 PRO DF FG - Moulded stud football boots - bright crimson/black/white"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-academy-mg-moulded-stud-football-boots-bright-crimsonwhiteblack-n1242a2fd-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/a6fa3ac6e3ca4f2a806be89c1cd2b27c/6c188b985c484de0a5d6feadcf9f9f59.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL 9 ACADEMY MG - Moulded stud football boots - bright crimson/white/black"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-3-fg-moulded-stud-football-boots-core-black-ad542a4wc-q11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/09944e660ab648e084daa8ff2aa39c60/95cceab4982446fc82719fd886f78935.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST.3 FG - Moulded stud football boots - core black"
    },
    {
        "url": "https://en.zalando.de/puma-future-pro-mxsg-screw-in-stud-football-boots-whiteblackfire-orchid-pu142a1ic-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/1443d13f05e54eb680de5c3480a06904/b009b2865466458d94b1f29793ce6436.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE PRO MXSG - Screw-in stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-future-play-fgag-moulded-stud-football-boots-whitefire-orchid-pu142a1hc-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/c2ec4e8422fc4222a314b09d82538f64/116f5fdd0a6a40c8968056ec7f12b690.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE PLAY FG/AG - Moulded stud football boots - white/fire orchid"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-academy-km-mg-moulded-stud-football-boots-baltic-bluewhite-n1242a2fh-k11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/cf4471285602432fbf09150db178a434/e04c671b779d4d0592feefaefcebbc58.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL 9 ACADEMY KM MG - Moulded stud football boots - baltic blue/white"
    },
    {
        "url": "https://en.zalando.de/nike-performance-mercurial-vapor-15-club-mg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2fq-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ae7afcd7765445909adedef2fcfa22c7/b40807653ff341f9be71e0dc8cf7c3a1.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MERCURIAL VAPOR 15 CLUB MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-screw-in-stud-football-boots-baltic-bluewhite-n1242a2p8-k11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/c1fa0400c5e4499fb3109215cc8d2aa5/34d5732b75c4458781ed1ca03dd8b236.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL VAPOR 15 ELITE KM FG - Screw-in stud football boots - baltic blue/white"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-neymar-jr-fgag-moulded-stud-football-boots-white-racing-blue-lemon-meringue-parakeet-green-pu142a1o8-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/279406af9d44496086830832a4f4bb6b/1362d30c4acc4b20a6239dc79c21ab66.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "FUTURE MATCH NEYMAR JR FG/AG - Moulded stud football boots - white racing blue lemon meringue parakeet green"
    },
    {
        "url": "https://en.zalando.de/nike-performance-mercurial-zoom-vapor-15-academy-mg-moulded-stud-football-boots-pink-blastvoltgridiron-n1242a2fl-j11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6684abb6527144e581d941bd8d3728d8/b2327ccb04054dedaac898b6686fdacb.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM VAPOR 15 ACADEMY FG/MG - Moulded stud football boots - pink blast/volt/gridiron"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-laceless-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1h6-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/f2de0cf8b42c4291aebd21a37c403f85/ddd98bcbfc26491daff932caefac29dd.jpg?imwidth=300&filter=packshot",
        "discount": "up to -15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-ultimate-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hb-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6365aa2cfcb14daa9e0ccd78adb89bee/738408d704034ffb93ee5fe2837bb1ca.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA ULTIMATE FG/AG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-match-fgag-moulded-stud-football-boots-blackasphalt-pu142a1hq-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/062ce86824f444dbbf955ea02f8b7918/cb140c433a204cf8bcad9dff4be19ad4.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "ULTRA MATCH FG/AG - Moulded stud football boots - black/asphalt"
    },
    {
        "url": "https://en.zalando.de/campaigns/aldo-global-campaign-h2/",
        "brand": "ALDO Pillow Walk\u2122\u200b",
        "img_url": "https://img01.ztat.net/crt/creative-content/02f017c4-1ebd-467b-86be-969af740125e.jpg?imwidth=300",
        "discount": null,
        "is_deal": false,
        "is_sponsored": true,
        "short_description": "ALDO Pillow Walk\u2122\u200b"
    },
    {
        "url": "https://en.zalando.de/puma-king-ultimate-fgag-moulded-stud-football-boots-silver-skyblackfire-orchid-pu142a1ho-d11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/932e8144a8594f52885c339a1b77cf6c/9f8b58f751304be8a521da86a8232f09.jpg?imwidth=300&filter=packshot",
        "discount": "-20%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "KING ULTIMATE FG/AG UNISEX - Moulded stud football boots - silver sky/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-future-pro-fgag-moulded-stud-football-boots-blacksilver-pu142a1i7-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/74a5b38e63424d858b39d98cd0259a94/04b88f63822342259724cfdf33228760.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE PRO FG/AG - Moulded stud football boots - black/silver"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-predator-accuracy-3-mg-moulded-stud-football-boots-core-blackfootwear-white-ad542a4s6-q12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/1fa832ab21174a37852f02cbdcca02ff/95267b73c9dc4987aabe7bdd3251eafb.jpg?imwidth=300&filter=packshot",
        "discount": "up to -25%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PREDATOR ACCURACY 3 MG - Moulded stud football boots - core black/footwear white"
    },
    {
        "url": "https://en.zalando.de/nike-performance-lunar-gato-ii-ic-indoor-football-boots-whitelight-brown-n1242a0j8-a21.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/938f1de0c1fa4a8d91b7e40518af918f/890c5a72e06b4102ac993920254f479f.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "NIKE LUNARGATO II - Indoor football boots - white/light brown"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-x-crazyfast-3-sg-screw-in-stud-football-boots-footwear-whitecore-blacklucid-lemon-ad542a4yq-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/f1a6bce5d69a42319ae53c70fdd47461/3d0df8bc6c5649699fe43e580b1084ec.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST 3 SG - Screw-in stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast1-laceless-fg-moulded-stud-football-boots-footwear-whitecore-blacklucid-lemon-ad542a4vz-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/c0ccd7ee6aff4dfcbd1fc7052a05cae8/52229dabdbcc453e91aed4f685a344a0.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "CRAZYFAST LACELESS FG - Moulded stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-academy-sg-pro-unisex-screw-in-stud-football-boots-bright-crimsonwhiteblack-n1242a2f5-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/0a6f3a0f10554fdcb8923a86201180a3/a661e4b6bff24753afee777b414829b3.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL 9 ACADEMY SG-PRO ANTI CLOG TRACTION - Screw-in stud football boots - bright crimson/white/black"
    },
    {
        "url": "https://en.zalando.de/mizuno-morelia-neo-iv-elite-moulded-stud-football-boots-blackgold-m2742a0gu-q11.html",
        "brand": "Mizuno",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/f641a16561d4451ba2aa56f79a9ffe7b/4c52fdfcce664536a79117c0e46e0d2d.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MORELIA NEO IV ELITE - Moulded stud football boots - black/gold"
    },
    {
        "url": "https://en.zalando.de/puma-future-ultimate-fgag-moulded-stud-football-boots-whitefire-orchid-pu142a1hn-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/9664243fa67341658a0ff05d6a846e1d/6a6ef9d655784cfa8a7ed0a0a8578071.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE ULTIMATE FG/AG - Moulded stud football boots - white/fire orchid"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-club-fgmg-moulded-stud-football-boots-bright-crimsonblackwhite-n1242a2ix-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/b2081d19b27e4f34b2de5d51aa27e0cf/9f5ad5dc84fe4c989ad127a231be5afb.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PHANTOM CLUB FG/MG - Moulded stud football boots - bright crimson/black/white"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-9-pro-fg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2fa-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/f4765f2c21bd4dc0ba5161e26f0f10b5/197d5a91a9a548bfaa9e93e29bfeaf2c.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL PRO FG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-x-crazyfast4-fxg-moulded-stud-football-boots-core-black-ad542a4wf-q11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/dfe27d8995e949088b0259931d0c7116/b8f94e6b72f847c1abeaad973bb14210.jpg?imwidth=300&filter=packshot",
        "discount": "up to -15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST 4 FXG - Moulded stud football boots - core black"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-3-fg-moulded-stud-football-boots-footwear-whitecore-blacklucid-lemon-ad542a4wc-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/4b68d46aec034647ad4899f1192ea0a8/db9fd1273b23419c99d7019c0c1e8322.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST.3 FG - Moulded stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-2-fg-moulded-stud-football-boots-footwear-whitecore-blacklucid-lemon-ad542a4ww-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/fe6fed0466a44cbea140baaf00dc31af/3129e40958dd40f5a7106b98446cf5d2.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST.2 FG - Moulded stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-gx-academy-df-fg-mg-moulded-stud-football-boots-black-chrome-hyper-royal-n1242a2iw-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/dcb21c36aa614b55930b4019caba57ba/f9826039a15f4f4b80c1dc7cd47a4d5c.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 ACADEMY DF FG/MG - Moulded stud football boots - black chrome hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-high-top-trainers-black-hyper-royal-chrome-n1242a2p2-q11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/78d07de416b442268eb316d48186a721/7c5231fce8b2419faaed38b6c63755ac.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM VAPOR 15 ACADEMY AG - Moulded stud football boots - black hyper royal chrome"
    },
    {
        "url": "https://en.zalando.de/puma-future-ultimate-low-fgag-moulded-stud-football-boots-puma-white-puma-black-fire-orchid-pu142a1h8-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/31803e995089478bb16f5d75bfc8b155/565ebcab4d2045169659a02dc713d4ce.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "FUTURE ULTIMATE FG/AG - Moulded stud football boots - white- black-fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-king-pro-moulded-stud-football-boots-blackwhite-pu142a1he-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6ad4e2fe8988471b95ccb8dbe491b0d3/32e945e7e10a46e08bfb733688cbe4f7.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "KING PRO FG/AG - Moulded stud football boots - black/white"
    },
    {
        "url": "https://en.zalando.de/puma-king-ultimate-fgag-moulded-stud-football-boots-blackasphalt-pu142a1ho-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/8028797034b74c0a960513cba4aed8d6/ad74f185aaf24bf0a4ee0ec5ff4bcef7.jpg?imwidth=300&filter=packshot",
        "discount": "up to -30%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "KING ULTIMATE FG/AG UNISEX - Moulded stud football boots - black/asphalt"
    },
    {
        "url": "https://en.zalando.de/nike-performance-zoom-mercurial-vapor-15-academy-km-mg-moulded-stud-football-boots-baltic-bluewhite-n1242a2fj-k11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/00739fdc1d2e4335835b76b824e00976/3ccbd5ee07d74f9bb66e06fc6dccea5d.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM MERCURIAL VAPOR 15 ACADEMY KM MG - Moulded stud football boots - baltic blue/white"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-3-fg-moulded-stud-football-boots-core-black-ad542a4wn-q11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/62a03288b77146aaae99c2f0331e96ce/a893e74253d844e7b4f63d6f8190e4d6.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "CRAZYFAST 3 LACELESS FG - Moulded stud football boots - core black"
    },
    {
        "url": "https://en.zalando.de/nike-performance-fussball-phantom-gx-elite-fg-moulded-stud-football-boots-baltic-blue-white-laser-blue-pink-blast-n1244a0i5-k11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/02f9fad95c82430d8c4e9ab0228f0753/b2fa49e732414a3287fa11d47eecb267.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 ELITE FG - Moulded stud football boots - baltic blue white laser blue pink blast"
    },
    {
        "url": "https://en.zalando.de/nike-performance-tiempo-legend-10-academy-sg-pro-ac-screw-in-stud-football-boots-blackchromehyper-royal-n1242a2ld-q11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/44df1a933ba14ca8a51a3b8852d0c205/ad1b9b92e1204591baaeba8b7b3d59b6.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "LEGEND 10 ACADEMY SG-PRO AC - Screw-in stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/puma-future-pro-fgag-moulded-stud-football-boots-persian-bluewhitepro-green-pu142a1i7-k11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/4f12fb0fe4f14eb98d20021eb6d8d942/77f0748fefc446bdbafdc016f1afa82f.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "FUTURE PRO FG/AG - Moulded stud football boots - persian blue/white/pro green"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-dynamic-moulded-stud-football-boots-blackchromehyper-royal-n1242a2j8-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2d5c7482466e473f89b35e6471f207ff/6196e931cfc34bf0a97b15cdb6259c17.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 PRO DF FG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-3-fg-moulded-stud-football-boots-footwear-white-ad542a4wn-a12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ad67b6a4444548ef8b8111ddff061e0f/0b6e3f7b22b14b13921680e90e821347.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "CRAZYFAST 3 LACELESS FG - Moulded stud football boots - footwear white"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-fgag-moulded-stud-football-boots-persian-bluewhitepro-green-pu142a1hx-k11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/065dd63148d94aec8bb78f8f6cf7ed84/8292ce09cc764add8dc7514875cbc092.jpg?imwidth=300&filter=packshot",
        "discount": "up to -15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE MATCH FG/AG - Moulded stud football boots - persian blue/white/pro green"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-predator-accuracy3-sg-screw-in-stud-football-boots-footwear-whitecore-blacklucid-lemon-ad542a4wi-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6d7b567bc475430aa020ba40c716dee7/a6678a190d5846679e2b0980fe521e8d.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PREDATOR ACCURACY.3 SG - Screw-in stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-moulded-stud-football-boots-footwaer-whitecore-blacklucid-lemon-ad542a4wf-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/d2590ff92d4a441caf3bd933f6296b79/de1d98e3df564b2b8fc4ba19dc61fe75.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST 4 FXG - Moulded stud football boots - footwear white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/nike-performance-fussball-kunstrasen-zoom-mercurial-moulded-stud-football-boots-schwarzblau-n1242a2jq-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/77c473f4ddae48d991c47af2a5a4373c/e074be57f6d74ecfb02e37485f5555c6.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "ZOOM VAPOR 15 ELITE AG-PRO - Moulded stud football boots - schwarz/blau"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-academy-sg-pro-ac-screw-in-stud-football-boots-bright-crimsonblackwhite-n1242a2jb-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/d2bc03b449194893934271b5a1da1690/684d178ba7c643cb86172c7bd8bd4ff8.jpg?imwidth=300&filter=packshot",
        "discount": "-10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 ACADEMY SG-PRO AC - Screw-in stud football boots - bright crimson/black/white"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-crazyfast-1-fg-moulded-stud-football-boots-core-blacksolar-yellowgrey-ad542a4wz-q11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/5413cbe1d9134edea6a6a952b4a9ccb0/81067d87c6e64640837cccd379a57812.jpg?imwidth=300&filter=packshot",
        "discount": "-20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "CRAZYFAST 1 FG - Moulded stud football boots - core black/solar yellow/grey"
    },
    {
        "url": "https://en.zalando.de/joma-maxima-indoor-football-boots-black-j3342a0g7-q11.html",
        "brand": "Joma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/25f98bb8ae1f4cc89bc2654ffa99d941/6a2ff9b4f66e45f385026dd06f4dd1c0.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MAXIMA - Indoor football boots - black"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-predator-accuracy-3-laceless-fg-moulded-stud-football-boots-footwaer-whitecore-blacklucid-lemon-ad542a4wv-a11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/21ecac087ef041989cfa88a71dcabaa7/5798d65bfff54fa096ac351d97811d6d.jpg?imwidth=300&filter=packshot",
        "discount": "up to -10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PREDATOR ACCURACY 3 LACELESS FG - Moulded stud football boots - footwaer white/core black/lucid lemon"
    },
    {
        "url": "https://en.zalando.de/puma-king-pro-mxsg-screw-in-stud-football-boots-blackwhite-pu142a1il-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/5757e63c88e5441ead3a7f5b28544041/d86f2ec4ea5b466ab1fcde0b3f62b0cb.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "KING PRO MXSG - Screw-in stud football boots - black/white"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-pro-fgag-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1hg-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/15315928c320433c9e0da49c65e0559b/33d0804ad76a494eb2c3bb03e0ae2ad6.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA PRO FG/AG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/puma-ultra-match-tt-astro-turf-trainers-whiteblackfire-orchid-pu142a1hy-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ee035a750e02400091799f9d7f624875/a999e48fb0654e698d37edb9c3c836f0.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": true,
        "short_description": "ULTRA MATCH TT - Astro turf trainers - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/nike-performance-mercurial-zoom-vapor-15-academy-fgmg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2fl-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/38e0a79eb52f4b1c8bf45195146e71cc/41f3d62401484fb480f122c9378eee5a.jpg?imwidth=300&filter=packshot",
        "discount": "up to -11%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "ZOOM VAPOR 15 ACADEMY FG/MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-x-crazyfast-2-fg-moulded-stud-football-boots-footwear-white-ad542a4ww-a12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/810220a27f8a4560bf87a9f506e1ceb9/7c4e7ea13e0840c5be524e26dc0e2229.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST.2 FG - Moulded stud football boots - footwear white"
    },
    {
        "url": "https://en.zalando.de/joma-maxima-astro-turf-trainers-black-j3342a0g5-q11.html",
        "brand": "Joma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2db6c3bcfc3b4ffab9563186790342ca/788e5b64881c42e6ad78d945cb77033b.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "MAXIMA - Astro turf trainers - black"
    },
    {
        "url": "https://en.zalando.de/nike-performance-nike-zoom-mercurial-vapor-15-academy-mg-moulded-stud-football-boots-bright-crimsonwhiteblack-n1242a2fl-g11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/8b651025c6494ff69c0ad74ee645321d/0e64a828265f41ee8a8cf8949c68b05d.jpg?imwidth=300&filter=packshot",
        "discount": "up to -6%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "ZOOM VAPOR 15 ACADEMY FG/MG - Moulded stud football boots - bright crimson/white/black"
    },
    {
        "url": "https://en.zalando.de/nike-performance-tiempo-legend-unisex-indoor-football-boots-blackchromehyper-royal-n1242a2li-q11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/883578a365434900b552a23dfb09e9bd/d4fa42146a114ab5b84e8c0446477a30.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "LEGEND 10 CLUB IC - Indoor football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-x-crazyfast-4-fxg-moulded-stud-football-boots-footwear-white-ad542a4wf-a12.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/97d0060cf1ba4081a090a0366a858257/3e3585fc567540ee8411df1f73689564.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST 4 FXG - Moulded stud football boots - footwear white"
    },
    {
        "url": "https://en.zalando.de/puma-future-play-fgag-moulded-stud-football-boots-blacksilver-pu142a1hc-q11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/7757631e906a44329ee74e008113014c/c14a77772d1244c39acc1128e5e64d8a.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "FUTURE PLAY FG/AG - Moulded stud football boots - black/silver"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-gx-club-mg-moulded-stud-football-boots-blackchromehyper-royal-n1242a2j1-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/d6320a53920e44d7a1b5665250d05738/3b51f807811142d9a3469d2a9ab1dab8.jpg?imwidth=300&filter=packshot",
        "discount": "-10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 CLUB FG/MG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-phantom-unisex-moulded-stud-football-boots-blackchromehyper-royal-n1242a2j5-q12.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/c9379b5803214a4385174ce6cfb54596/8ba94d492b6d45989013ed9ebcc29957.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "PHANTOM GT3 PRO FG - Moulded stud football boots - black/chrome/hyper royal"
    },
    {
        "url": "https://en.zalando.de/nike-performance-tiempo-legend-10-pro-ag-moulded-stud-football-boots-black-hyper-royal-chrome-n1242a2lf-q11.html",
        "brand": "Nike Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/46315289def84f4fa5e0db3e4e60613e/af2dd4967d3b45c69c4261c8d3977ca3.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "TIEMPO LEGEND 10 PRO AG - Moulded stud football boots - black hyper royal chrome"
    },
    {
        "url": "https://en.zalando.de/puma-future-match-mg-moulded-stud-football-boots-whiteblackfire-orchid-pu142a1i8-a11.html",
        "brand": "Puma",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/950ac2880b90421ebb2a79256473efee/154807b040c545b69c7c1177e224791e.jpg?imwidth=300&filter=packshot",
        "discount": "-10%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "FUTURE MATCH MG - Moulded stud football boots - white/black/fire orchid"
    },
    {
        "url": "https://en.zalando.de/adidas-performance-x-crazyfast-2-fg-moulded-stud-football-boots-core-black-ad542a4ww-q11.html",
        "brand": "adidas Performance",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6727a57f2fff4decb8f91da8b30a4eb7/118649e05c7d4931ae8a3c8f36baa9ef.jpg?imwidth=300&filter=packshot",
        "discount": "up to -20%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "X CRAZYFAST.2 FG - Moulded stud football boots - core black"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-trainers-blackvintage-white-co415o0jo-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/2a5635d1a1904be78ddb2e94dfb3143c/cbc8c94c3a19460fabc6a892866ac7fe.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - Trainers - black/vintage white"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-unisex-trainers-vintage-whiteblack-co415o0jn-a11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6dc50415834546b2aeb1a068336a143c/3ebaa77833f84c7fbbf4a63f3e30a635.jpg?imwidth=300",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER UNISEX - Trainers - vintage white/black"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-unisex-trainers-egretpale-putty-co415o0l9-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/e80f8938af4a464f87410d61e4e0fe39/a211d49328254851b128a51260e74f26.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER UNISEX - Trainers - egret/pale putty"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-high-top-trainers-blackvintage-whiteegret-co415n0ud-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/18c2794495ea4a8c93fb2d54b04eb74b/08647ba75cb64c68861262a0f6ccdb8f.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - High-top trainers - black/vintage white/egret"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-trainers-utilityvintage-whiteblack-co415o0kc-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/ed8792b7a76d425db870d84735e922bd/4c5804e9af3f4f48b34cb4eee58c1311.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - Trainers - utility/vintage white/black"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-mono-trainers-blackstorm-windanthracite-co415o0ll-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/8f1d7cd8d3c14422b09d4e38b193fc1a/c1574aab09fb4385868c50d3924bfa1c.jpg?imwidth=300&filter=packshot",
        "discount": "-15%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 MONO - Trainers - black/storm wind/anthracite"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-fall-unisex-trainers-blackvintage-whitesilver-co415o0ln-q11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/4dfafac82e614da7836db86088972e6d/72bd1213c2da4481b016914d68043f29.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 FALL UNISEX - Trainers - black/vintage white/silver"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-high-top-trainers-ghostedvintage-whiteblack-co415n0u8-k11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/6cf74a48900e47549b3a610518b45925/494cec1a7e954d02a9009a4268b7cac4.jpg?imwidth=300&filter=packshot",
        "discount": "-11%",
        "is_deal": true,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - High-top trainers - ghosted/vintage white/black"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-trainers-offwhitedark-blue-co415o0ls-a11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/faaf149acf7146daab85277298593f8e/584901a6fbd3419789cb0e8f4a09855e.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - Trainers - offwhite/dark blue"
    },
    {
        "url": "https://en.zalando.de/converse-star-player-76-unisex-trainers-vintage-whitemidnight-cloveregret-co415o0l1-a11.html",
        "brand": "Converse",
        "img_url": "https://img01.ztat.net/article/spp-media-p1/5b5fbf97da604a158548abc93a3f62ba/82e5ed7ce1574b7a87c8bd7e477c82dc.jpg?imwidth=300&filter=packshot",
        "discount": null,
        "is_deal": false,
        "is_sponsored": false,
        "short_description": "STAR PLAYER 76 UNISEX - Trainers - vintage white/midnight clover/egret"
    }, 
]
```