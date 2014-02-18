# encoding: utf8
from django.db import models, migrations
import datetime
from datetime import date


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0002_auto_20140217_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='predicted_ready',
            field=models.DateField(null=True, verbose_name='Predicted ready', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='predicted_brew_ready',
            field=models.DateField(default=date(2014, 2, 17), verbose_name='predicted brew ready'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='batch',
            name='notified_bottle_complete',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='batch',
            name='notified_brew_complete',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
