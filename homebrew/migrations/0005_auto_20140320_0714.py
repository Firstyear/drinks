# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0004_sourceingredient_ean13'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourceingredient',
            name='source_ean',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='sourceingredient',
            name='ean13',
            field=models.CharField(default=None, max_length=14, null=True, blank=True),
        ),
    ]
