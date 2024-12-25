from django.core.management.base import BaseCommand
from backend.models import Facility, KvpGroup
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed Facility data'

    def handle(self, *args, **kwargs):
        pvs = [
            {
                "name": "AGYW",
                "gender": "Female",
                "age_start": 15,
                "age_end": 24,
                "pin_code_start": 10,
                "pin_code_end": 30,
            },
            {
                "name": "FSW",
                "gender": "Female",
                "age_start": 18,
                "age_end": 99,
                "pin_code_start": 31,
                "pin_code_end": 50,

            }, {
                "name": "MSM",
                "gender": "Male",
                "age_start": 15,
                "age_end": 99,
                "pin_code_start": 51,
                "pin_code_end": 70,

            }, {
                "name": "PWID",
                "gender": "Male/Female",
                "age_start": 15,
                "age_end": 99,
                "pin_code_start": 71,
                "pin_code_end": 90,
            },
            {
                "name": "PWUD",
                "gender": "Male/Female",
                "age_start": 15,
                "age_end": 99,
                "pin_code_start": 91,
                "pin_code_end": 99,
            }
        ]
        for i in pvs:
            KvpGroup.objects.get_or_create(
                name=i['name'],
                defaults={
                    "gender": i['gender'],
                    "age_start": i['age_start'],
                    "age_end": i['age_end'],
                    "pin_code_start": i['pin_code_start'],
                    "pin_code_end": i['pin_code_end'],
                }
            )
        facilities = [
            {
                "district": "Mbeya CC",
                "ward": "Igawilo",
                "supporting_facility": "Igawilo Hospital",
                "hfrcode": "101535-3",
                "responsible_cso": "SHYI ORGANIZATION",
                "responsible_person": "Mediana Mswima",
                "mobile_no": "0752268925",
                "app_password": "123456",
                "pin_range_start": 10,
                "pin_range_end": 20,
            },
            {
                "district": "Mbarali DC",
                "ward": "Igurusi",
                "supporting_facility": "Igurusi HC",
                "hfrcode": "101595-7",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Wema Panga",
                "mobile_no": "0759636772",
                "app_password": "123456",
                "pin_range": "21-30",
                "pin_range_start": 21,
                "pin_range_end": 30,
            },
            {
                "district": "Mbarali DC",
                "ward": "Rugelele",
                "supporting_facility": "Igawa Dispensary",
                "hfrcode": "101533-8",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Wema Panga",
                "mobile_no": "0759636771",
                "app_password": "123456",
                "pin_range_start": 31,
                "pin_range_end": 40,
            },
            {
                "district": "Chunya DC",
                "ward": "Chokaa",
                "supporting_facility": "Chunya DH, HfrCode",
                "hfrcode": "100890-3",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Michael Simkoko",
                "mobile_no": "0766245595",
                "app_password": "123456",
                "pin_range_start": 41,
                "pin_range_end": 50,
            },
            {
                "district": "Chunya DC",
                "ward": "Matundasi",
                "supporting_facility": "Itumbi Dispensary",
                "hfrcode": "114026-8",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Michael Simkoko",
                "mobile_no": "0766245585",
                "app_password": "123456",
                "pin_range_start": 51,
                "pin_range_end": 60,
            },
            {
                "district": "Kyela DC",
                "ward": "Njisi",
                "supporting_facility": "Njisi Dispensary",
                "hfrcode": "106498-9",
                "responsible_cso": "SHYI ORG",
                "responsible_person": "Mediana Mswima",
                "mobile_no": "0752268125",
                "app_password": "123456",
                "pin_range_start": 61,
                "pin_range_end": 70

            },

            {
                "district": "Tunduma TC",
                "ward": "Tunduma",
                "supporting_facility": "Tunduma HC",
                "hfrcode": "108850-9",
                "responsible_cso": "IRDO",
                "responsible_person": "TBD",
                "mobile_no": "TBD5",
                "app_password": "123456",
                "pin_range_start": 71,
                "pin_range_end": 80
            },
            {
                "district": "Tunduma TC",
                "ward": "Mpemba",
                "supporting_facility": "Tunduma Hospital",
                "hfrcode": "113990-6",
                "responsible_cso": "IRDO",
                "responsible_person": "TBD2",
                "mobile_no": "TBD",
                "app_password": "123456",
                "pin_range_start": 81,
                "pin_range_end": 87

            },
            {
                "district": "Sumbawanga MC",
                "ward": "Katandala",
                "supporting_facility": "Katandala HC",
                "hfrcode": "102460-3",
                "responsible_cso": "CEELS",
                "responsible_person": "Leah Sanga",
                "mobile_no": "0754109291",
                "app_password": "123456",
                "pin_range_start": 88,
                "pin_range_end": 93


            },
            {
                "district": "Mpanda MC",
                "ward": "Makanyagio",
                "supporting_facility": "Town clinic HC ",
                "hfrcode": "111475-0",
                "responsible_cso": "CEELS",
                "responsible_person": "TBD",
                "mobile_no": "TBD3",
                "app_password": "123456",
                "pin_range_start": 94,
                "pin_range_end": 99

            },
        ]

        for facility in facilities:
            user, user_created = User.objects.get_or_create(
                username=facility["mobile_no"],
            )
            if user_created:
                user.set_password(facility["app_password"])
                user.save()


            if not user_created:
                self.stdout.write(self.style.WARNING(
                    f"User with mobile number {
                        facility['mobile_no']} already exists. Skipping user creation..."
                ))

            # Update or create the facility
            facility_obj, created = Facility.objects.update_or_create(
                user=user,
                defaults={
                    "district": facility["district"],
                    "ward": facility["ward"],
                    "supporting_facility": facility["supporting_facility"],
                    "hfrcode": facility["hfrcode"],
                    "responsible_cso": facility["responsible_cso"],
                    "responsible_person": facility["responsible_person"],
                    "mobile_no": facility["mobile_no"],
                    "app_password": facility["app_password"],
                    "pin_range_start": facility["pin_range_start"],
                    "pin_range_end": facility["pin_range_end"]
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created facility: {facility_obj}"))
            else:
                self.stdout.write(self.style.NOTICE(
                    f"Updated facility: {facility_obj}"))

            facility_obj.save()  # Save the updated data back to the database

        self.stdout.write(self.style.SUCCESS(
            "Facility data seeded successfully."))
