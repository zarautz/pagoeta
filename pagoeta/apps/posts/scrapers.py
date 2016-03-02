import bleach
import feedparser

from datetime import datetime
from django.template.defaultfilters import slugify
from lxml.html import fromstring
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

            for img in fromstring(content).cssselect('img'):
                image_source = img.get('src')
                content_images[image_source] = self.get_xerox_image_sources(image_source)

            posts.append({
                'title': post.title,
                'permalink': post.link,
                'author': post.author,
                'description': post.description,
                'content': content,
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
