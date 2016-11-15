from __future__ import unicode_literals

from itertools import chain
from django.db import models

from modelcluster.fields import ParentalKey

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from blog.blocks.code_highlight import CodeBlock
from blog.blocks.markdown import MarkDownBlock
from blog.blocks.restructured_text import RSTBlock
from wagtail.wagtailsearch import index

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', related_name='tagged_items')

class FreeFormBlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.FreeFormBlogPage', related_name='tagged_freeform')

class BlogIndex(Page):
    subpage_types = ['BlogPage', 'FreeFormBlogPage']
    def get_context(self, request):
        context = super(BlogIndex, self).get_context(request)
        # Add extra variables and return the updated context
        freeformpage = FreeFormBlogPage.objects.child_of(self).live().filter(in_blog_index=True).order_by('-date')[:10]
        blogpage = BlogPage.objects.child_of(self).live().order_by('-date')[:10]
        all_posts = list(chain(freeformpage, blogpage))
        context['blog_entries'] = all_posts
        return context

class BlogPage(Page):
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('date'),
        index.SearchField('tags'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        ImageChooserPanel('main_image'),
        FieldPanel('body', classname="full"),
        # InlinePanel('related_links', label="Related links"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('main_image'),
        FieldPanel('tags'),
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

class FreeFormBlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    tags = ClusterTaggableManager(through=FreeFormBlogPageTag, blank=True)
    in_blog_index = models.BooleanField("Include in Blog Index", default=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('code_snippet', CodeBlock()),
        ('restructured_text', RSTBlock()),
        ('markdown', MarkDownBlock()),
        ('raw_html', blocks.RawHTMLBlock()),
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('tags'),
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('date'),
        index.RelatedFields('tags', [index.SearchField('name', partial_match=True, boost=10),
        ]),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('in_blog_index')
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
