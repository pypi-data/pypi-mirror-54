# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from allink_core.core.loading import get_model


Testimonials = get_model('testimonials', 'Testimonials')


class TestimonialsSitemap(Sitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(TestimonialsSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return Testimonials.objects.active()

    def lastmod(self, obj):
        return obj.modified
