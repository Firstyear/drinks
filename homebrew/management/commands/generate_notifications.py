from django.core.management.base import BaseCommand, CommandError
from homebrew.models import Batch, Box
from django.contrib.auth.models import User
from datetime import date
from django.core.mail import send_mass_mail
from django.db import transaction

class Command(BaseCommand):
    args = ''
    help = 'Generates notifications for events with batches'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ### Select 
        today = date.today()
        messages = ()
        for user in User.objects.all():
            ### Check batches ready to bottle
            bottle_batch_list = Batch.objects.filter(predicted_ready__lte=today,user=user)
            brewed_batch_list = Batch.objects.filter(predicted_brew_ready__lte=today,user=user)
            ### Check batches ready to drink.
            if len(brewed_batch_list) > 0 or len(bottle_batch_list) > 0:
                message_body = 'Hi {user}, the following is ready:\n\n'.format(user=user)
                for batch in brewed_batch_list:
                    message_body += '- Batch #{id}, {name}, is ready to bottle.\n'.format(id=batch.id, name=batch)
                    batch.notified_brew_complete = True
                    batch.save()
                for batch in bottle_batch_list:
                    message_body += '- Batch #{id}, {name}, is ready to drink!\n'.format(id=batch.id, name=batch)
                    batch.notified_bottle_complete = True
                    batch.save()
                message_body += '\nSincerely,\n\nThe homebrew fairy'

                #Prepare the email.
                message = ('Homebrew notification {date}'.format(date=today),
                            message_body,
                            'noreply@blackhats.net.au',
                            [user.email])
                messages += (message,)
        send_mass_mail(messages, fail_silently=False)
