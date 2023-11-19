<a href="https://ik.imagekit.io/egszdsbs2/bluemoss/blog.html?updatedAt=1699980966189">
    Download HTML
</a>
<br>
<br>
<img src="https://ik.imagekit.io/egszdsbs2/bluemoss/blog.png?updatedAt=1699980728541" alt="">

<br>

# Goal - Scrape all blogposts

### Step 1 - Identify data points to scrape

Looking at the page, we can easily identify 4 datapoints per blogpost:

- url
- date
- title
- text

### Step 2 - Analyze the HTML
Before we can start writing code, we need to understand the structure of the HTML, specifically
the nature of the html tags that contain the data we want to scrape.

#### Open the HTML in your editor and search for a blog post title

After searching for the string *"Input choice is easily"* which is a part of the first blog posts title,
we find the following HTML. It also seems to encapsulate all 4 datapoints we are interested in.

```html
...
<div class="post">
      <h2>
       <a href="https://seths.blog/2023/10/input-choice-is-easily-overlooked/">
        Input choice is easily taken for granted
       </a>
      </h2>
      <p>
       We can give instructions to a fellow human by:
      </p>
      <ul>
       <li>
        Talking to them
       </li>
       <li>
        Handwriting a note
       </li>
       <li>
        Typing a text
       </li>
       <li>
        Waving a flag
       </li>
       <li>
        Triggering a traffic device
       </li>
       <li>
        Sounding a siren
       </li>
       <li>
        Sending a memo
       </li>
       <li>
        Choosing from a list of choices on a menu
       </li>
       <li>
        Making a facial expression
       </li>
       <li>
        and perhaps a dozen or more other methods…
       </li>
      </ul>
      <p>
       Most people develop voiceboxes and limbs and facial expressions that make any of these usable. Computers, over the decades, have had to have them engineered.
      </p>
      <p>
       In 1983, Dan Lovy built a parser for the adventure games I was marketing at Spinnaker. Suddenly, you could type instructions into the game instead of relying on the more emotional but crude joystick for input. So, “pick up the dragon’s pearl” was something the game could understand.
      </p>
      <p>
       There’s a restaurant in the Bronx where the waiter asks, “what do you want?” There’s no menu. If you imagine something in a certain range, they’ll make it. This is stressful, because we’re used to the paradigm of multiple choice in this setting.
      </p>
      <p>
       A smart doctor doesn’t ask, “what’s wrong?” Instead, she takes a few minutes to notice, converse and connect, because our fear of mortality gets in the way of a truthful analysis.
      </p>
      <p>
       As the worlds of tech and humanity merge, it’s worth thinking hard about the right way to engage with a device. When a car invites you to talk with it, the car designer is betting our lives that the car will actually respond to the vagaries of speech in a specific way. Perhaps a steering wheel is a better user interface.
      </p>
      <p>
       (And it’s not just a car–sometimes we fail to communicate with each other in a useful and specific way that matches the work to be done…)
      </p>
      <div class="has-social-placeholder has-content-area" data-hashtags="" data-post-id="47446" data-title="Input choice is easily taken for granted" data-url="https://seths.blog/2023/10/input-choice-is-easily-overlooked/">
      </div>
      <p class="byline">
       <span class="date">
        October 11, 2023
       </span>
    ...
```



### Step 3 - Create a dataclass to represent a blogpost

```python
# examples/blog/classes.py

from bluemoss import Jsonify
from dataclasses import dataclass, field


@dataclass
class BlogPost(Jsonify):
    url: str
    date: str
    title: str
    text: str | None = field(default=None, init=False)
    _text_lines: list[str]

    def __post_init__(self):
        self.text = '\n\n'.join(
            [line.strip() for line in self._text_lines if line.strip()]
        )
```

### Step 4 - Build the Node object to scrape all posts

```python
# node.py

from bluemoss import Node
from examples.blog.classes import BlogPost


BLOG_PAGE_NODE: Node = Node(
    filter=None,
    target=BlogPost,
    xpath="div[@class='post']",
    nodes=[
        Node('a', key='title'),
        Node('a/@href', key='url'),
        Node("span[@class='date']", key='date'),
        Node('p[not(@*)] | .//li[not(@*)]', key='_text_lines', filter=None),
    ],
)
```

### Step 5 - Scrape the HTML / Test the Node object
```python
# main.py

from bluemoss import scrape
from examples.blog.classes import BlogPost
from examples.blog.node import BLOG_PAGE_NODE


with open('./static/blog.html', 'r') as f:
    posts: list[BlogPost] = scrape(BLOG_PAGE_NODE, f.read())
    print(posts)
```

```json
// the print output

[
    {
        "url": "https://seths.blog/2023/10/input-choice-is-easily-overlooked/",
        "date": "October 11, 2023",
        "title": "Input choice is easily taken for granted",
        "text": "We can give instructions to a fellow human by:\n\nTalking to them\n\nHandwriting a note\n\nTyping a text\n\nWaving a flag\n\nTriggering a traffic device\n\nSounding a siren\n\nSending a memo\n\nChoosing from a list of choices on a menu\n\nMaking a facial expression\n\nand perhaps a dozen or more other methods\u2026\n\nMost people develop voiceboxes and limbs and facial expressions that make any of these usable. Computers, over the decades, have had to have them engineered.\n\nIn 1983, Dan Lovy built a parser for the adventure games I was marketing at Spinnaker. Suddenly, you could type instructions into the game instead of relying on the more emotional but crude joystick for input. So, \u201cpick up the dragon\u2019s pearl\u201d was something the game could understand.\n\nThere\u2019s a restaurant in the Bronx where the waiter asks, \u201cwhat do you want?\u201d There\u2019s no menu. If you imagine something in a certain range, they\u2019ll make it. This is stressful, because we\u2019re used to the paradigm of multiple choice in this setting.\n\nA smart doctor doesn\u2019t ask, \u201cwhat\u2019s wrong?\u201d Instead, she takes a few minutes to notice, converse and connect, because our fear of mortality gets in the way of a truthful analysis.\n\nAs the worlds of tech and humanity merge, it\u2019s worth thinking hard about the right way to engage with a device. When a car invites you to talk with it, the car designer is betting our lives that the car will actually respond to the vagaries of speech in a specific way. Perhaps a steering wheel is a better user interface.\n\n(And it\u2019s not just a car\u2013sometimes we fail to communicate with each other in a useful and specific way that matches the work to be done\u2026)"
    },
    {
        "url": "https://seths.blog/2023/10/no-thank-you/",
        "date": "October 10, 2023",
        "title": "No thank you",
        "text": "Failing to acknowledge a favor or a courtesy is a triple mistake, and it\u2019s becoming more common. ChatGPT is now promoting the idea that it can write a thank you note for you, and a text is a lot easier than a handwritten note, and yet, the level of \u2018thank you\u2019 seems to be falling.\n\nIt\u2019s not that people don\u2019t have the time to offer an honest \u2018thank you\u2019. It\u2019s that they don\u2019t want to acknowledge the obligation or connection.\n\nMinimizing a favor is an easy way to stay focused on the noise in our own heads, as opposed to realizing that we\u2019re surrounded by other people.\n\nHustle culture has discovered that \u2018asking for a favor\u2019 often triggers a positive response. This effort on the part of the other person happens because the favor-giver is seeking connection. When the recipient minimizes the favor or fails to say thank you, they create distance, not connection.\n\nThe fact that an expression of gratitude requires so little effort makes it even more striking.\n\nTo pick a tiny example, if someone lets you into the flow of traffic, a small nod or hand wave costs nothing. But sometimes it feels easier to assert that it was yours to take, as opposed to a kind gesture that you received.\n\nOur failure to take a moment to acknowledge the favor also makes it harder for the next person. If connection isn\u2019t on offer, why not be selfish?\n\nCivility fades in the face of entitlement.\n\nThe magic of an honest expression of gratitude is that the person saying thank you might benefit from it as much as the recipient."
    },
    {
        "url": "https://seths.blog/2023/10/possibility-and-opportunity/",
        "date": "October 9, 2023",
        "title": "Possibility and opportunity",
        "text": "We have the chance to build something that creates connection and generates value. On the other hand, a system that diminishes agency and dignity is inherently unstable.\n\nWhen we seek to create scarcity and control and optimize output at the expense of our humanity, it may pay off for a while, but it\u2019s brittle and will ultimately fail. As it falters, it\u2019s easy to see how the forces seeking control can double down and simply make the situation even worse.\n\nThe alternative is to realize that finding opportunities and seeking connection is the path worth following.\n\nIt takes compassion and confidence to offer resilience, responsibility and agency instead of insisting on power and control."
    },
    {
        "url": "https://seths.blog/2023/10/getting-it-right-the-first-time/",
        "date": "October 8, 2023",
        "title": "Getting it right the first time",
        "text": "How unlikely is this?\n\nThe artist who paints a masterpiece, from scratch, without hesitation. The playwright who doesn\u2019t need a workshop or a reading. The architect who designs a food hall that has a layout and vibe that works without one alteration\u2026\n\nEvolution is powerful. It gives us the chance to revise, edit and do what works while removing what doesn\u2019t.\n\nOnce we realize that there is almost no chance we\u2019ll get it right the first time, we can embrace the opportunity to sign up for better instead of perfect.\n\nGet it wrong the first time.\n\nThen make it better."
    },
    {
        "url": "https://seths.blog/2023/10/password-stupidity-is-no-longer-viable/",
        "date": "October 7, 2023",
        "title": "Password stupidity is no longer viable",
        "text": "[Of course, it\u2019s not stupidity. It\u2019s fear and superstition, which often go together. First, the rant.]\n\nIt\u2019s 2023. Major corporations should not be posting rules like this:\n\nThis is not just security theatre. It\u2019s a waste of time, the math makes no sense and it leads people to create worse passwords, not better ones.\n\nIf the person who maintains your office sprayed water on the front walk just before the temperature dropped to freezing, you\u2019d never stand for that. If the folks who filed your taxes simply made up numbers that felt like they made sense, you\u2019d switch accountants.\n\nIf a company can\u2019t get this simple system right, how can we trust them to make a refrigerator?\n\nThere is plenty of insightful, effective thinking about online security. Your organization embarrasses itself when it hassles customers to engage in silliness like this. Stupidity is easier to spot and fix than ever before.\n\nPS if this is broken but looks fine to the boss, what else in your organization is similarly grounded in superstition or the status quo?\n\n[The challenge with tech is that the person doing the work often has a boss who doesn\u2019t understand the work and isn\u2019t willing to put in the time to do so.\n\nTwenty years ago, I ranted about the forms that have a pull-down for US citizens challenging them to choose which of fifty states they live in, and country pull-downs that begin with Andorra and put two of the biggest webshop countries in the world at the end of a list of more than a hundred. There\u2019s no good technical reason for this. It\u2019s simply the way someone created a template at the end of the last century, and it\u2019s easier to simply go along.\n\nNow that AI is about to rewrite just about every rule of our culture, perhaps it\u2019s a good time for the boss to commit to understanding it.]"
    },
    {
        "url": "https://seths.blog/2023/10/how-big-is-the-vessel/",
        "date": "October 6, 2023",
        "title": "Getting better at bucket management",
        "text": "If you throw a bucket of water on a small campfire, you\u2019ll succeed in putting it out.\n\nPour a bucketful of sake into one of those little glasses and you\u2019ll waste most of it and ruin the table setting.\n\nAnd try to use a bucket to refill a dried-out lake and not much will happen.\n\nRelativity is everywhere we look. If you put in eight hours on a ten-hour project, you\u2019ll fail. Put that much effort into a smaller, six-hour project and the client will be delighted.\n\nThe Grateful Dead remain one of the greatest bands in memory, partly because they relentlessly overfilled what was expected from a band. Those that seek to be the next Grateful Dead inevitably fail, because the standard has been reset.\n\nOn the other hand, a tech company that raises a lot of money to \u2018change the world\u2019 but merely delivers a really useful tool is seen as a failure.\n\nThe promise we make defines the quality that is expected. Market pressure and our own insecurity drive us to make ever bigger promises, but when the promise doesn\u2019t match the deliverable, everyone forgets the effort and workmanship that was delivered.\n\nThe two challenges are:\n\nPick the right size bucket for the problem you\u2019re trying to solve.\n\nMake sure you have the resources to fill it all the way to the top.\n\nChoose your bucket, choose your future."
    },
    {
        "url": "https://seths.blog/2023/10/nothing-to-ad/",
        "date": "October 5, 2023",
        "title": "Nothing to ad",
        "text": "A recent discussion about the challenges of direct-to-consumer marketing of a skincare product ended with one participant describing the hard part with, \u201cnothing to ad.\u201d\n\nShe was referring to how much the thread had covered, but the pun wasn\u2019t lost on us.\n\nSocial media offered an irresistible promise to many folks who are looking to do \u201cmarketing\u201d:\n\nA business begins with the assertion that if they can get a committed new customer to start buying a high-margin product it would be worth at least $50 to them.\n\nIf it\u2019s worth $50 to get someone to click over to your site, a social media site or search engine offers to sell that click for $40!\n\nBuy as many clicks as you can, and you can grow your business.\n\nOf course, this is a really good deal for the social media sites. They do very little and keep almost all the profit.\n\nBut competitive pressures make the really good deal into one that it\u2019s hard for a company to live with. Now, instead of $40 to get a click, it costs $50 or $60 or $80. DTC companies end up raising baskets of money and spending just about all of it on social media and online ads, payments to influencers, etc, losing money on every customer.\n\nOnce committed, they\u2019re open to trying just about anything. They listen to wise (but actually making-stuff-up) sales reps and consultants about what time to post, whether to use photos, color photos, testimonials, paid influencers, free samples and more. \u201cOh, you tried to scale your buy too fast, the algorithm can tell\u2026\u201d and all sorts of black box thinking that, from a distance, surely gives away the con of separating a hardworking brand manager from the money they control.\n\nWe\u2019ve seen this before, many times, and it almost never ends well. There\u2019s not much to ad.\n\nThat\u2019s because the fundamental strategy cannot thrive in a competitive environment. Someone will always be willing to outbid you for attention. Someone will always be willing to lose just a bit more money than you.\n\nThe path forward is very different.\n\nYour (current) customers need to bring you your (new) customers.\n\nIt\u2019s not ironic but it is edifying to realize that this is EXACTLY how every one of the media companies you\u2019re paying ad money to grew. They grew with word of mouth, not the sorts of ads they\u2019re selling.\n\nFacebook or that influencer\u2013they didn\u2019t grow by running ads and selling subscriptions. They grew when their users felt that it was in their own selfish interests to bring them new users.\n\nAs long as your project is built around the misguided myth of \u201cgetting the word out\u201d and promoting itself to strangers, you will struggle. Someone always wins the spend-money-on-DTC-promo game, but it probably won\u2019t be you. It\u2019s simply a lottery where one of the spenders hits a magical level of critical mass and becomes buzzy. For the rest of us, there\u2019s only the glorious work of creating a product and a situation that people think is worth talking about. It\u2019s hard, it has dead ends, but it\u2019s the work.\n\nThe formulaic attraction of category + money + media consultant = home run is a problem precisely because it\u2019s a formula.\n\nPeople don\u2019t talk about your product or service because you have a gimmick or hype or because they care about you or even because a thoughtful analysis shows that it has the best features and price performance. They talk about it because they believe it\u2019s good for their status, their affiliation with people they care about or their frame of mind.\n\n[I wrote about this twenty years ago in\n\nPurple Cow\n\n, but people still look for the shortcut of ads, which is rarely a shortcut. And the conversation that inspired this post happened in the\n\nPurple Space\n\n.]"
    },
    {
        "url": "https://seths.blog/2023/10/evenly-distributed/",
        "date": "October 4, 2023",
        "title": "Evenly distributed",
        "text": "For the first time, the only time, everyone on Earth was in the same boat at the same time. We\u2019ve long been divided by privilege, by caste, by accidents of birth or by organized hierarchies.\n\nSure, there have been events that struck us all at once. Landing on the moon caused us all to gasp simultaneously. But this time was different. Regardless of class or age or nationality, the situation was right there, in front of our face. And it didn\u2019t go away in a few news cycles.\n\nBut the responses, of course, were not the same.\n\nSome profiteered and hoarded, cutting the line and seeking a profit, regardless of the cost to others. Some embraced panic while others sought to fan it. Some showed up asking for help while others decided to see who needed help.\n\nAnd that\u2019s the first lesson of our pandemic. While events might be evenly distributed, responses and reactions rarely are. We are able to choose to see possibility. We are able to lead. We\u2019re able to see beyond a day or a week into the future.\n\nNot simply a few of us.\n\nAny\n\nof us.\n\nThat choice wasn\u2019t dictated by class or station or race. It was a new decision, made each day, by people who chose to care. Volunteer firemen who showed up for the next alarm. Parents who sat with a kid instead of parking them in front of a device. Doctors who quieted their fears in order to save others.\n\nThis leads to the second lesson, which is the choice that is in front of each of us. Just as the pandemic created the opportunity to lead and to contribute, the future is knocking on our doors asking us to make a new decision.\n\nFor millennia, we\u2019ve been using our resources to insulate ourselves from the weather. Some are luckier than others in their ability to find a safe haven.\n\nWe learned the hard way that our fragile industrial ecosystem isn\u2019t quite as resilient as we hoped. We discovered that we aren\u2019t actually as insulated from nature (and each other) as we might have expected. And we learned (perhaps) that compared to the alternative, preparation is quite cheap.\n\nThere will be other flu pandemics, and each time, if history is a guide, we\u2019ll be better at fighting them. But fighting a virus is very different than fighting the weather. The weather, the inexorable rise of the sea, is going to get harder and harder to ignore. The effects are unevenly distributed now, often exposing the most vulnerable, but as we saw with a global pandemic, we won\u2019t be able to buy ourselves peace of mind for long.\n\nThe fork in the road is plain to see. Who will lead? Who will see possibility and opportunity and decide to show up now, when we can, to do something about tomorrow? And who will decide to push to go back to business as usual?\n\nJust as air travel and cruise ships spread the virus, our industrial might has planted the seeds of our destruction. At the same time, the modern world has created a system with enough leverage to save itself.\n\nWhile the system has leverage, the system is not resilient and the system doesn\u2019t lead itself.\n\nThe best time to begin is now. Start where you are. Don\u2019t wait for authority or a\n\nmanual\n\n.\n\nChange will come, as it always does, from us.\n\nEach of us. If we care enough to lead.\n\nThe opportunity to care is evenly distributed."
    },
    {
        "url": "https://seths.blog/2023/10/fooling-ourselves/",
        "date": "October 3, 2023",
        "title": "Fooling ourselves",
        "text": "It\u2019s tempting to believe that we\u2019re not easy to fool.\n\nNot by a magician, a politician or a banker. Other folks might be easily duped by a spammer or a hustler, but not us.\n\nAnd yet, no one fools you more than you.\n\nWhen you look in the mirror, do you see what others see, or is it possible you see someone far less (or far more) attractive than others do?\n\nDo we assume that our work is so good and so useful that anyone who doesn\u2019t see that is confused or misguided?\n\nPerhaps we feel like an impostor, a fraud or an unseen genius\u2026\n\nThese are all forms of self-deception.\n\nA useful way forward might be to ask, \u201cis it working?\u201d\n\nIf the marketplace of ideas, of commerce or of relationships sees something of value, perhaps they\u2019re right. And if they don\u2019t, perhaps we might develop the empathy to understand what\u2019s missing in our narrative about what we do or how we do it.\n\nMarketing to others begins with marketing to ourselves.\n\nIf it turns out that our self-deception is a reliable source of fuel for us to achieve our goals, it might be worth living with. But at some point, our ability to fool ourselves becomes toxic. It blocks our ability to create generous and useful work, and it eats away at our confidence and peace of mind.\n\nIt\u2019s not easy to see ourselves as others do. But perhaps they\u2019re onto something."
    },
    {
        "url": "https://seths.blog/2023/10/but-it-matters-a-lot-to-them/",
        "date": "October 2, 2023",
        "title": "But it matters a lot to them\u2026",
        "text": "To get to the\n\nKebab House Cafe\n\n, you\u2019ll need to drive past a dozen fast food restaurants, restaurants you can find off just about any interstate. It\u2019s certainly less convenient to go a few blocks off the beaten path, but the food and service and vibe might be worth it.\n\nThe thing is, it matters even more to\n\nthem\n\n. The folks that work there, the ones who are building something they\u2019re proud of. It matters to the unique ones, to the ones that are trying harder than the others, to the folks who create interesting and memorable experiences.\n\nAnd it\u2019s not just one cafe. When a musician, a playwright or an entrepreneur takes a risk, they\u2019re betting someone will care enough to hear them and engage with them. They do the work because they care, not because someone handed them a manual.\n\nThe best part is that when it matters to them, it might matter even more to us.\n\nIf we want to have the option of choosing something that isn\u2019t in the ordinary course of convenient and cheap, we need to show up for the people who bring it to us.\n\nWorking with people who want to work with us is a privilege and a delight.\n\nWe get what we support."
    }  
]

```