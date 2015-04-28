import bleach
import feedparser

from datetime import datetime
from django.db import transaction, IntegrityError
from lxml.html import fromstring
from time import mktime

from pagoeta.apps.core.functions import get_image_sources
from pagoeta.apps.core.models import XeroxImage


class ZuZarautzPostScraper():
    updated = None

    def get_source(self):
        return {'Zu Zarautz': 'http://zuzarautz.info/'}

    def get_data(self):
        return self.parse_rss_feed()

    def parse_rss_feed(self):
        allowed_tags = feedparser._HTMLSanitizer.acceptable_elements.union(set(['object', 'embed', 'iframe']))
        allowed_attrs = {
            'a': ['href', 'rel'],
            'img': ['src'],
        }
        feedparser._HTMLSanitizer.acceptable_elements = allowed_tags
        source = feedparser.parse('http://zuzarautz.info/feed/')
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
                'tags': [tag.term.lower() for tag in post.tags],
                'contentImages': content_images,
            })

        return posts

    def get_xerox_image_sources(self, image_source):
        try:
            with transaction.atomic():
                x = XeroxImage(url=image_source)
                x.save()
        except IntegrityError:
            pass

        return {
            'source': get_image_sources(XeroxImage.IMAGE_TYPE_IN_URL, x.hash)
        }
