from django.core.management.base import BaseCommand
from app.models import Product
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Displays number of active users'

    def handle(self, *args, **kwargs):

        active_users_count = Product.objects.filter(name__istartswith='C')

        self.stdout.write(self.style.SUCCESS(f'Active users count: {active_users_count}'))
        logger.info(f'Active users counted: {active_users_count}')