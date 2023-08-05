# Generated by Django 2.1.8 on 2019-07-03 10:34

import aldryn_common.admin_fields.sortedm2m
import aldryn_translation_tools.models
import allink_core.core.models.mixins
import cms.models.fields
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djangocms_text_ckeditor.fields
import filer.fields.image
import model_utils.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('cms', '0022_auto_20180620_1551'),
        ('locations', '0001_initial'),
        ('allink_categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(blank=True, null=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='end')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(1, 'active'), (2, 'inactive')], default=1, verbose_name='status')),
                ('template', models.CharField(blank=True, help_text='Choose a template.', max_length=50, null=True, verbose_name='Template')),
                ('sort_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('form_enabled', models.BooleanField(default=True, verbose_name='Event Form enabled')),
                ('event_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Event Date/ Time')),
                ('categories', models.ManyToManyField(blank=True, to='allink_categories.AllinkCategory')),
                ('content_placeholder', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_events_content_placeholder', slotname='events_content', to='cms.Placeholder')),
                ('header_placeholder', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_events_header_placeholder', slotname='events_header', to='cms.Placeholder')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='locations.Locations')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, help_text='og: image is used when shared on Facebook/ Twitter etc. (Min. 1200 x 630 px)<br>Page: 1. fallback is teaser_image, 2. fallback is field allink_config.default_og_image.<br>App: 1. fallback = preview_image 2. fallback is teaser_image, 3. fallback is defined in allink_config.default_og_image.<br>', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events_events_og_image', to=settings.FILER_IMAGE_MODEL, verbose_name='og:Image')),
                ('preview_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events_events_preview_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Preview Image')),
                ('teaser_image', filer.fields.image.FilerImageField(blank=True, help_text='Optional field for teaser image. og: properties are used when shared on Facebook/ Twitter etc. (Min. 1200 x 630 px)<br>Also used as "meta" property="og:image"<br>Page: 1. fallback is allink_config.default_og_image.<br>App: 1. fallback = preview_image 2. fallback is defined in allink_config.default_og_image.<br>', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='events_events_teaser_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Teaser image')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'abstract': False,
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, allink_core.core.models.mixins.AllinkTranslatedAutoSlugifyMixin, allink_core.core.models.mixins.AllinkInvalidatePlaceholderCacheMixin, allink_core.core.models.mixins.AllinkMetaTagMixin, allink_core.core.models.mixins.AllinkTeaserMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EventsAppContentPlugin',
            fields=[
                ('manual_filtering', models.CharField(blank=True, max_length=50, null=True)),
                ('manual_ordering', models.CharField(blank=True, max_length=50, null=True)),
                ('filter_fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=None, null=True, size=None)),
                ('template', models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template')),
                ('category_navigation_enabled', models.BooleanField(default=False, help_text='If checked, a filter navigation with all selected categories is displayed.<br>Please note: A category is only displayed if it contains items.', verbose_name='Show category navigation')),
                ('category_navigation_all', models.BooleanField(default=False, help_text='If checked, a category "all" in filter navigation is displayed.', verbose_name='Show category "all"')),
                ('softpage_enabled', models.BooleanField(default=True, help_text='If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded.', verbose_name='Show detailed information in Softpage')),
                ('detail_link_enabled', models.BooleanField(default=True, help_text='If checked, a link/button to the detail view will be displayed.', verbose_name='Show detail link')),
                ('items_per_row', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=3, help_text='Only applied if a "Grid" template has been selected.', verbose_name='Grid items per row')),
                ('paginated_by', models.IntegerField(default=0, help_text='Limit the number of entries (in case of the "load more" pagination type: entries per page). Default is "0" (show all entries)', verbose_name='Max. entries per page')),
                ('pagination_type', models.CharField(choices=[('no', 'None'), ('load', 'Add "Load more"-Button'), ('load_rest', 'Add "Load all"-Button')], default=('no', 'None'), max_length=50, verbose_name='Pagination Type')),
                ('load_more_button_text', models.CharField(blank=True, help_text='If left blank, a default text will be used. <br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)', max_length=255, null=True, verbose_name='Text for "Load .."-Button')),
                ('detail_link_text', models.CharField(blank=True, help_text='If left blank, a default text will be used.<br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)', max_length=255, null=True, verbose_name='Text for "Detail"-Link')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='events_eventsappcontentplugin', serialize=False, to='cms.CMSPlugin')),
                ('apphook_page', cms.models.fields.PageField(blank=True, help_text='If provided, this Apphook-Page will be used to generate the detail link.', null=True, on_delete=django.db.models.deletion.PROTECT, to='cms.Page', verbose_name='Apphook Page')),
                ('categories', models.ManyToManyField(blank=True, to='allink_categories.AllinkCategory')),
                ('categories_and', models.ManyToManyField(blank=True, related_name='events_eventsappcontentplugin_categories_and', to='allink_categories.AllinkCategory')),
                ('category_navigation', models.ManyToManyField(blank=True, help_text='You can explicitly define the categories for the category navigation here. This will override the automatically set of categories (either the one generated from "Filter & Ordering" or "Manual entries")', related_name='events_eventsappcontentplugin_category_navigation', to='allink_categories.AllinkCategory', verbose_name='Categories for Navigation')),
                ('manual_entries', aldryn_common.admin_fields.sortedm2m.SortedM2MModelField(blank=True, help_text='Select and arrange specific entries, or, leave blank to select all. (If manual entries are selected the category filtering will be ignored.)', to='events.Events')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='EventsRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('salutation', models.IntegerField(choices=[(1, 'Mr.'), (2, 'Mrs.')], null=True, verbose_name='Salutation')),
                ('first_name', models.CharField(max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=255, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Company')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Phone')),
                ('message', models.TextField(blank=True, max_length=255, null=True, verbose_name='Message')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Events')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventsTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('og_title', models.CharField(blank=True, default='', help_text='title-tag is used when shared on Facebook/ Twitter etc.<br>Also used to overwrite "meta property="og:image.."" and title-tag<br>Page: fallback is field "title" of the page.<br>App: fallback is field "title".', max_length=255, verbose_name='og:title | <title> Tag')),
                ('og_description', models.TextField(blank=True, default='', help_text='Description is used when shared on Facebook/ Twitter etc.<br>Also used to overwrite  "meta" property="og:description" .. and "meta name="description"<br>Page: fallback is field "teaser_description" of the page, if set. Otherwise empty.<br>App: fallback is field "lead", if set. Otherwise empty.', max_length=255, verbose_name='og:description | meta description')),
                ('teaser_title', models.CharField(blank=True, default='', help_text='Page: fallback is field "title" of the page.<br>App: fallback is field "title".', max_length=255, verbose_name='Teaser title')),
                ('teaser_technical_title', models.CharField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is hardcoded per app in the teaser_dict.', max_length=255, verbose_name='Teaser technical title')),
                ('teaser_description', models.TextField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is field "lead".', verbose_name='Teaser description')),
                ('teaser_link_text', models.CharField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is hardcoded per app in the teaser_dict.', max_length=255, verbose_name='Teaser link text')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, default='', help_text='Leave blank to auto-generate a unique slug.', max_length=255, verbose_name='Slug')),
                ('lead', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Teaser text that in some cases is used in the list view and/or in the detail view.', null=True, verbose_name='Lead Text')),
                ('costs', models.CharField(blank=True, help_text='Costs', max_length=255, null=True)),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='events.Events')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
