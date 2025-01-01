import random
from backend.models import Customer, Facility, KvpGroup, KvpPin
from django.contrib import messages


# def generate_kvp_pins(facility_id, amount, groups):
#     try:
#         # Fetch the facility
#         facility = Facility.objects.get(id=facility_id)
#         pin_range_start = facility.pin_range_start
#         pin_range_end = facility.pin_range_end

#         print(f"Generating {amount} pins for facility: {facility}")

#         if pin_range_start >= pin_range_end:
#             raise ValueError(
#                 "Facility PIN range start must be less than the range end.")

#         # Loop to generate the required number of pins
#         for _ in range(int(amount)):
#             groups = KvpGroup.objects.filter(id__in=groups)
#             for group in groups:
#                 pin_code_start = group.pin_code_start
#                 pin_code_end = group.pin_code_end

#                 if pin_code_start >= pin_code_end:
#                     print(f"Skipping group {
#                           group.name} due to invalid pin code range.")
#                     continue

#                 # Generate unique PINs
#                 max_attempts = 1000  # Limit to prevent infinite loop
#                 attempts = 0

#                 while attempts < max_attempts:
#                     pin_code = random.randint(pin_code_start, pin_code_end)
#                     pin = random.randint(pin_range_start, pin_range_end)
#                     pin_generated = int(
#                         f"{pin_code}{pin}{random.randint(10, 99)}")

#                     # Check uniqueness
#                     if not KvpPin.objects.filter(pin=pin_generated).exists():
#                         KvpPin.objects.create(
#                             pin=pin_generated,
#                             facility=facility,
#                             group=group
#                         )
#                         print(f"Generated and saved PIN: {pin_generated}")
#                         break

#                     attempts += 1

#                 if attempts >= max_attempts:
#                     print("Failed to generate a unique PIN after maximum attempts.")

#     except Facility.DoesNotExist:
#         print(f"Facility with id {facility_id} does not exist.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


import random
from django.db import transaction
from backend.models import Facility, KvpGroup, KvpPin


def generate_kvp_pins(facility_id, amount, group_ids):
    try:
        # Fetch the facility
        facility = Facility.objects.get(id=facility_id)
        pin_range_start = facility.pin_range_start
        pin_range_end = facility.pin_range_end

        print(f"Generating {amount} pins for facility: {facility}")

        if pin_range_start >= pin_range_end:
            raise ValueError(
                "Facility PIN range start must be less than the range end.")

        # Fetch groups once
        groups = KvpGroup.objects.filter(id__in=group_ids)
        if not groups.exists():
            raise ValueError("No valid groups found for the given IDs.")

        # Use a set to track generated PINs in memory for this session
        existing_pins = set(KvpPin.objects.values_list("pin", flat=True))

        for _ in range(int(amount)):
            for group in groups:
                pin_code_start = group.pin_code_start
                pin_code_end = group.pin_code_end

                if pin_code_start >= pin_code_end:
                    print(f"Skipping group {
                          group.name} due to invalid pin code range.")
                    continue

                max_attempts = 1000  # Limit attempts to generate unique pins
                attempts = 0

                while attempts < max_attempts:
                    pin_code = random.randint(pin_code_start, pin_code_end)
                    pin = random.randint(pin_range_start, pin_range_end)
                    pin_generated = int(
                        f"{pin_code}{pin}{random.randint(10, 99)}")

                    if pin_generated not in existing_pins:
                        # Save to database and update the in-memory set
                        with transaction.atomic():
                            KvpPin.objects.create(
                                pin=pin_generated,
                                facility=facility,
                                group=group
                            )
                        existing_pins.add(pin_generated)
                        print(f"Generated and saved PIN: {pin_generated}")
                        break

                    attempts += 1

                if attempts >= max_attempts:
                    print("Failed to generate a unique PIN after maximum attempts.")

    except Facility.DoesNotExist:
        print(f"Facility with id {facility_id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def assign_pin(request, pin_id):
    pin = KvpPin.objects.get(id=pin_id)
    gender = pin.group.gender

    if not pin.is_used:
        Customer.objects.create(
            type="Client Group",
            gender=gender if pin.group.gender == "Male" or pin.group.gender == "Female" else None,
            client_group=pin.group,
            registered_machine=pin.facility.machine,
            pin = pin.pin,
            pin_type= "PERMANENT"
        )
        pin.is_used = True
        pin.save()
        print(f"Assigned PIN {pin.pin} to customer.")
        messages.error(request, f"PIN {pin.pin} has  been assigned.")
    else:
        print(f"PIN {pin.pin} has already been used.")
        messages.error(request, f"PIN {pin.pin} has already been used.")
