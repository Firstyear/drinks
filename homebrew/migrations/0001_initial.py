# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sugar',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                u'verbose_name_plural': 'sugar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Yeast',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                u'verbose_name': 'yeast',
                u'verbose_name_plural': 'yeast',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='labels')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceIngredient',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('comment', models.TextField(null=True, blank=True)),
                ('bottle_time', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('label', models.ForeignKey(to='homebrew.Label', to_field=u'id')),
                ('source_ean', models.CharField(max_length=13)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('sourceingredient', models.ForeignKey(to='homebrew.SourceIngredient', to_field=u'id')),
                ('yeast', models.ForeignKey(to='homebrew.Yeast', to_field=u'id')),
                ('yeast_volume', models.IntegerField()),
                ('sugar', models.ForeignKey(to='homebrew.Sugar', to_field=u'id')),
                ('sugar_volume', models.IntegerField()),
                ('pot_start_date', models.DateField(verbose_name='pot start')),
                ('bottling_date', models.DateField(null=True, verbose_name='Bottling date', blank=True)),
                ('start_specific_gravity', models.FloatField()),
                ('end_specific_gravity', models.FloatField(default=0, null=True, blank=True)),
                ('start_temperature', models.IntegerField()),
                ('avg_predicted_temperature', models.IntegerField(default=0)),
                ('label', models.ForeignKey(to_field=u'id', blank=True, to='homebrew.Label', null=True)),
                ('maker_comment', models.TextField(null=True, blank=True)),
            ],
            options={
                u'verbose_name_plural': 'batches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('batch', models.ForeignKey(to_field=u'id', blank=True, to='homebrew.Batch', null=True)),
                ('bottle_capacity', models.IntegerField(default=750)),
                ('max_bottles', models.IntegerField()),
                ('number_bottles', models.IntegerField()),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                u'verbose_name_plural': 'boxes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('batch', models.ForeignKey(to='homebrew.Batch', to_field=u'id')),
                ('viewpoint', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
