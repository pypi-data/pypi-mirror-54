# Generated by Django 2.1.10 on 2019-10-02 19:51

from django.db import migrations
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcategorytranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='allink_categories.AllinkCategory'),
        ),
    ]
