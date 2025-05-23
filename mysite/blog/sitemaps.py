from django.contrib.sitemaps import Sitemap
from .models import Post

"""
A sitemap is an XML file that tells search engines the pages of your website, their relevance, and
how frequently they are updated. Using a sitemap will make your site more visible in search engine
rankings because it helps crawlers to index your website’s content.

Below is an implementation of a sitemap of the blog that includes the links to all published posts
"""

class PostSitemap(Sitemap):
    changefreq = 'weekly' #? changes frequency of yor post pages
    priority = 0.9 #? blog priority
    def items(self):
        return Post.published.all()
    def lastmod(self, obj):
        return obj.updated