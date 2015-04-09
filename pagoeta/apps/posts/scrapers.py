import bleach
import feedparser
import hashlib

from datetime import date, datetime, timedelta
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils import timezone
from lxml.html import parse, fromstring
from time import mktime

from pagoeta.apps.core.functions import get_absolute_uri
from pagoeta.apps.core.models import XeroxImage


class ZuZarautzPostScraper():
    updated = None

    def get_source(self):
        return { 'Zu Zarautz': 'http://zuzarautz.info/' }

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
                hash = hashlib.sha1(image_source).hexdigest()
                content_images[image_source] = self.get_xerox_image_sources(image_source)

            posts.append({
                'title': post.title,
                'permalink': post.link,
                'author': post.author,
                'description': post.description,
                'content': content,
                'publishedAt': post.published,
                'tags': [tag.term.lower() for tag in post.tags],
                'contentImages': content_images
            })

        return posts

    def get_xerox_image_sources(self, image_source):
        hash = hashlib.sha1(image_source).hexdigest()

        try:
            x = XeroxImage(hash=hash, url=image_source)
            x.save()
        except:
            # https://docs.djangoproject.com/en/dev/ref/exceptions/#database-exceptions
            pass

        return {
            'source': {
                'square': get_absolute_uri(reverse('xerox', args=('square', hash))),
                'small': get_absolute_uri(reverse('xerox', args=('small', hash))),
                'medium': get_absolute_uri(reverse('xerox', args=('medium', hash))),
                'large': get_absolute_uri(reverse('xerox', args=('large', hash)))
            }
        }
