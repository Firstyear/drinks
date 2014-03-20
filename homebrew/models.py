from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
import datetime
from datetime import date, timedelta
import math

class Label(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='labels')

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy('homebrew:label_detail', kwargs={'pk': self.pk})

class SourceIngredient(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField(blank=True, null=True)
    #### Time needed in bottles before ready
    bottle_time = models.IntegerField()
    volume = models.IntegerField()
    ### This should probably not be null .... 
    label = models.ForeignKey(Label)
    source_ean = models.CharField(max_length=14)
    ean13 = models.CharField(max_length=14, blank=True, null=True, default=None)
    ## Should this have an EAN13?

    def __unicode__(self):
        return self.name

    def clean(self):
        print(self.id)
        print(self.ean13)
        if self.id is not None:
            if self.ean13 is None or self.ean13 == '0':
                self.ean13 = '0200001{id:0>5}'.format(id=self.id)

    def get_absolute_url(self):
        return reverse_lazy('homebrew:sourceingredient_detail', kwargs={'pk': self.pk})


class Sugar(models.Model):
    class Meta:
        verbose_name_plural = "sugar"

    name = models.CharField(max_length=50, unique=True)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('homebrew:sugar_detail', kwargs={'pk': self.pk})

class Yeast(models.Model):
    class Meta:
        verbose_name = "yeast"
        verbose_name_plural = "yeast"

    name = models.CharField(max_length=50, unique=True)
    comment = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('homebrew:yeast_detail', kwargs={'pk': self.pk})

class Batch(models.Model):
    class Meta:
        verbose_name_plural = "batches"

    user = models.ForeignKey(User)
    sourceingredient = models.ForeignKey(SourceIngredient)
    yeast = models.ForeignKey(Yeast)
    yeast_volume = models.IntegerField()
    sugar = models.ForeignKey(Sugar)
    sugar_volume = models.IntegerField()
    pot_start_date = models.DateField('pot start')
    predicted_brew_ready = models.DateField('predicted brew ready')
    bottling_date = models.DateField('Bottling date', blank=True, null=True)
    predicted_ready = models.DateField('Predicted ready', blank=True, null=True)
    start_specific_gravity = models.FloatField()
    end_specific_gravity = models.FloatField(default=0, blank=True, null=True)
    start_temperature = models.IntegerField()
    ### The temperature over the next fortnight
    avg_predicted_temperature = models.IntegerField(default=0)
    label = models.ForeignKey(Label, blank=True, null=True)
    maker_comment = models.TextField(blank=True, null=True)
    notified_brew_complete = models.BooleanField(default=False)
    notified_bottle_complete = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % ( self.sourceingredient.name)

    def clean(self):
        days = math.ceil(((-7.0/8.0) * self.avg_predicted_temperature) + 29.25)
        self.predicted_brew_ready = self.pot_start_date + datetime.timedelta(days=days)
        if self.bottling_date is not None:
            self.predicted_ready = self.bottling_date + datetime.timedelta(days=self.sourceingredient.bottle_time)
        else:
            self.predicted_ready = None
    
    @property
    def label_text(self):
        return "#{batch:0>4}, {date}, abv {percent:.2f}%".format(batch=self.id, date=self.predicted_ready, percent=self.predicted_abv )


    ### Generate the alcohol content. + 0.5%
    @property
    def predicted_abv(self):
        if self.end_specific_gravity is not None and self.end_specific_gravity != 0:
            abv = ((((1.05) * (self.start_specific_gravity - self.end_specific_gravity)) /
                    self.end_specific_gravity) /0.79 ) * 100
            return abv + 0.5 # Due to sugar charging!!!!
        else:
            return 0

    def get_absolute_url(self):
        return reverse_lazy('homebrew:batch_detail', kwargs={'pk': self.pk})

class Box(models.Model):
    class Meta:
        verbose_name_plural = "boxes"
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    batch = models.ForeignKey(Batch, blank=True, null=True)
    bottle_capacity = models.IntegerField(default=750)
    max_bottles = models.IntegerField()
    number_bottles = models.IntegerField()
    comment = models.TextField(blank=True, null=True)

    @property
    def status(self):
        """
        Returns an int for status.
        0 : ready to drink
        1 : Not quite yet
        2 : All drunk, or no batch
        """
        if self.batch is None or self.batch.predicted_ready is None:
            return 2
        if self.batch.predicted_ready >= date.today():
            return 1
        return 0

    @property
    def ready(self):
        if self.batch is not None and self.batch.predicted_ready is not None:
            return self.batch.predicted_ready
        return None

    @property
    def consumed(self):
        if number_bottles == 0:
            return True
        return False

    def get_absolute_url(self):
        return reverse_lazy('homebrew:box_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        if self.batch is not None:
            return "{id} : batch #{batch:0>4}".format(id=self.id, batch=self.batch.id)
        return "{id} : Empty".format(id=self.id)

class Comment(models.Model):
    batch = models.ForeignKey(Batch)
    viewpoint = models.TextField()
    created = models.DateField(auto_now_add=True)

    @property
    def allowed(self):
        ## Look up the batch, and it's boxes, and count the bottles
        total_bottles = 0
        for box in self.batch.box_set.all():
            total_bottles += box.number_bottles
        if total_bottles <= 0:
            return False
        ## Also check if it's past the predicted ready date
        if datetime.now() < (batch.predicted_ready - timedelta(days=7)):
            return False
        ## Finally, if after 3 months from the predicted ready, close comments
        if datetime.now() > (batch.predicted_ready + timedelta(days=56)):
            return False
        return True

