from django.core.management.base import BaseCommand
from delire.dataBDD import createData

class Command(BaseCommand):
    def handle(self, **options):
        createData()