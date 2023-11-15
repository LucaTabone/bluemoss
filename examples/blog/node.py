from bluemoss import Node, scrape
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


if __name__ == '__main__':
    with open('./static/blog.html', 'r') as f:
        for article in scrape(BLOG_PAGE_NODE, f.read()):
            print(article)
