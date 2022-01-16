import time

from celery import shared_task
from django.core.mail import send_mail

from .models import Episode
from .serializers import EpisodeToNewSerializer


@shared_task
def send_mail_task(users):
    users.remove('admin@gmail.com')
    episodes = Episode.objects.all()
    serializer = EpisodeToNewSerializer(episodes, many=True)
    new_episodes = []
    for ordered_dict in serializer.data:
        if ordered_dict.get('was_published_recently'):
            ordered_dict.pop('was_published_recently')
            new_episodes.append(ordered_dict.get('__str__'))
    while True:
        time.sleep(10)
        send_mail('Новые серии', f'За прошлый день вышли серии: {new_episodes}', 'test@gmail.com', ['sainirgg@inbox.ru'])
