import bleach
import feedparser

from datetime import datetime
from django.template.defaultfilters import slugify
from lxml.html import fromstring, tostring
from time import mktime

from pagoeta.apps.core.scrapers import BaseScraper


class BasePostScraper(BaseScraper):
    pass


class RssPostScraper(BasePostScraper):
    source = None
    feed_url = None
    language = None

    def get_data(self):
        return self.parse_rss_feed()

    def parse_rss_feed(self):
        allowed_tags = feedparser._HTMLSanitizer.acceptable_elements.union(set(['object', 'embed', 'iframe']))
        allowed_attrs = {
            'a': ['href', 'rel'],
            'img': ['src'],
            'iframe': ['src', 'frameborder', 'allowfullscreen']
        }
        feedparser._HTMLSanitizer.acceptable_elements = allowed_tags
        source = feedparser.parse(self.feed_url)
        self.updated = datetime.fromtimestamp(mktime(source.updated_parsed))
        posts = []

        for post in source.entries:
            content = bleach.clean(post.content[0].value, allowed_tags, allowed_attrs)
            content_images = {}
            tree = fromstring(content)

            # Some blogs return a standard "The post {{title}} appeared first on {{source}}". Remove it.
            last_paragraph = tree.xpath('//p')[-1]
            if 'appeared first on' in last_paragraph.text_content():
                tree.remove(last_paragraph)

            for img in tree.xpath('//img'):
                image_source = img.get('src')
                content_images[image_source] = self.get_xerox_image_sources(image_source)

            posts.append({
                'title': post.title,
                'permalink': post.link,
                'author': post.author,
                'content': tostring(tree),
                'publishedAt': post.published,
                'tags': [slugify(tag.term.lower()) for tag in post.tags],
                'contentImages': content_images,
                'files': [],
            })

        return posts


class HitzaPostScraper(RssPostScraper):
    source = {'Zarauzko Hitza': 'http://urolakosta.hitza.eus/author/zarautz/'}
    feed_url = 'http://urolakosta.hitza.eus/author/zarautz/feed/'
    language = 'eu'
