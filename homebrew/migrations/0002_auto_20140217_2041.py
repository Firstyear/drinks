# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homebrew', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='name',
            field=models.CharField(default='Box', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sugar',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='yeast',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
