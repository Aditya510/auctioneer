import csv
from django.core.management.base import BaseCommand
from auction.models import Player

class Command(BaseCommand):
    help = 'Import players from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            
            for row in csv_reader:
                team = row[0]
                player_name = row[1].strip('"')
                
                Player.objects.create(
                    name=player_name,
                    team=team
                )
                
        self.stdout.write(self.style.SUCCESS(f'Successfully imported players from {csv_file}')) 