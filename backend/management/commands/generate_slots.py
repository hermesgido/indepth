from django.core.management.base import BaseCommand
from backend.models import Machine, Slot

class Command(BaseCommand):
    help = 'Generate slots for all machines'

    def handle(self, *args, **kwargs):
        # Define the slot numbers and product types
        kits_slots = [1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 27]
        condoms_slots = list(range(31, 61))

        # Iterate through all machines in the database
        machines = Machine.objects.all()
        if not machines.exists():
            self.stdout.write(self.style.WARNING("No machines found in the database."))
            return

        for machine in machines:
            self.stdout.write(f"Processing machine: {machine.name} (ID: {machine.machine_id})")

            # Generate slots for kits
            for slot_number in kits_slots:
                _, created = Slot.objects.get_or_create(
                    slot_number=slot_number,
                    machine=machine,
                    defaults={
                        'name': f"Slot {slot_number} - Kits",
                        'product_type': 'Kits',
                        'capacity': 199,  
                        'quantity_available': 10,
                        'price': 0,  
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created slot {slot_number} (Kits) for machine {machine.name}."))

            # Generate slots for condoms
            for slot_number in condoms_slots:
                _, created = Slot.objects.get_or_create(
                    slot_number=slot_number,
                    machine=machine,
                    defaults={
                        'name': f"Slot {slot_number} - Condoms",
                        'product_type': 'Condoms',
                        'capacity': 199,  
                        'quantity_available': 20,
                        'price': 500,  
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created slot {slot_number} (Condoms) for machine {machine.name}."))

        self.stdout.write(self.style.SUCCESS("Slot generation completed for all machines."))
