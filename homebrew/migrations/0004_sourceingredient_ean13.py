# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0003_auto_20140217_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourceingredient',
            name='ean13',
            field=models.CharField(default='0', max_length=13),
            preserve_default=False,
        ),
    ]
