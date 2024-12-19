import os
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from backend.models import Machine, Slot
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate slots for all machines with specific product types, subtypes, and product images'

    def handle(self, *args, **kwargs):
        # Define the slot data with product types, subtypes, and their respective images
        slot_data = {
            'kits_oral': {
                'slot_numbers': [1, 3, 5],
                'product_type': 'Kits',
                'product_subtype': 'Oral Kits',
                'image_filename': 'oralkit.jpg',
                'price': 0,
                'quantity': 0
            },
            'kits_blood': {
                'slot_numbers': [11, 13, 15, 21, 23, 25],
                'product_type': 'Kits',
                'product_subtype': 'Blood Kits',
                'image_filename': 'bloodkit.jpg',
                'price': 0,
                'quantity': 0
            },
            'condoms_male': {
                'slot_numbers': [7, 17, 27] + list(range(41, 61)),
                'product_type': 'Condoms',
                'product_subtype': 'Male Condoms',
                'image_filename': 'male_condom.jpg',
                'price': 500,
                'quantity': 0
            },
            'condoms_female': {
                'slot_numbers': list(range(31, 41)),
                'product_type': 'Condoms',
                'product_subtype': 'Female Condoms',
                'image_filename': 'female_condom.jpg',
                'price': 500,
                'quantity': 0
            },
        }

        # Retrieve all machines
        machines = Machine.objects.all()
        if not machines.exists():
            self.stdout.write(self.style.WARNING(
                "No machines found in the database."))
            return

        # Create FileSystemStorage instance for checking file existence
        fs = FileSystemStorage()

        # Iterate through all machines
        for machine in machines:
            self.stdout.write(f"Processing machine: { machine.name} (ID: {machine.machine_id})")

            # Iterate through slot data to create slots
            for key, data in slot_data.items():
                for slot_number in data['slot_numbers']:
                    # Get the image path
                    image_path = os.path.join(
                        'product_images', data['image_filename'])

                    # Check if the file exists
                    if not fs.exists(image_path):
                        self.stdout.write(self.style.WARNING(
                            f"Image file {data['image_filename']} does not exist. Skipping."))
                        continue

                    image_url = image_path

                    # Create the slot with the image URL (relative path)
                    _, created = Slot.objects.get_or_create(
                        slot_number=slot_number,
                        machine=machine,
                        defaults={
                            'name': f"Slot {slot_number} - {data['product_type']}",
                            'product_type': data['product_type'],
                            'product_subtype': data['product_subtype'],
                            'capacity': 11,
                            'quantity_available': data['quantity'],
                            'price': data['price'],
                            'product_image': image_url  # Corrected to store the relative path
                        },
                    )

                    # Log the creation success
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created slot {slot_number} ({data['product_type']} - {data['product_subtype']}) with image for machine {machine.name}."))

        self.stdout.write(self.style.SUCCESS(
            "Slot generation completed for all machines."))
