from django.core.management.base import BaseCommand
from backend.models import Facility


class Command(BaseCommand):
    help = 'Seed Facility data'

    def handle(self, *args, **kwargs):
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
            },
            {
                "district": "Mbarali DC",
                "ward": "Igurusi",
                "supporting_facility": "Igurusi HC",
                "hfrcode": "101595-7",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Wema Panga",
                "mobile_no": "0759636771",
                "app_password": "123456",

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

            },
            {
                "district": "Chunya DC",
                "ward": "Matundasi",
                "supporting_facility": "Itumbi Dispensary",
                "hfrcode": "114026-8",
                "responsible_cso": "SHDEPHA Mbarali",
                "responsible_person": "Michael Simkoko",
                "mobile_no": "0766245595",
                "app_password": "123456",

            },
            {
                "district": "Kyela DC",
                "ward": "Njisi",
                "supporting_facility": "Njisi Dispensary",
                "hfrcode": "106498-9",
                "responsible_cso": "SHYI ORG",
                "responsible_person": "Mediana Mswima",
                "mobile_no": "0752268925",
                "app_password": "123456",

            },
            
            {
                "district": "Tunduma TC",
                "ward": "Tunduma",
                "supporting_facility": "Tunduma HC",
                "hfrcode": "108850-9",
                "responsible_cso": "IRDO",
                "responsible_person": "TBD",
                "mobile_no": "TBD",
                "app_password": "123456",

            },
            {
                "district": "Tunduma TC",
                "ward": "Mpemba",
                "supporting_facility": "Tunduma Hospital",
                "hrfcode": "113990-6",
                "responsible_cso": "IRDO",
                "responsible_person": "TBD",
                "mobile_no": "TBD",
                "app_password": "123456",

            },
            {
                "district": "Sumbawanga MC",
                "ward": "Katandala",
                "supporting_facility": "Katandala HC",
                "hfrcode": "102460-3",
                "responsible_cso": "CEELS",
                "responsible_person": "Leah Sanga",
                "mobile_no": "0752109291",
                "app_password": "123456",

            },
            {
                "district": "Mpanda MC",
                "ward": "Makanyagio",
                "supporting_facility": "Town clinic HC ",
                "hfrcode": "111475-0",
                "responsible_cso": "CEELS",
                "responsible_person": "TBD",
                "mobile_no": "TBD",
                "app_password": "123456",

            },
        ]

        for facility in facilities:
            Facility.objects.create(**facility)

        self.stdout.write(self.style.SUCCESS(
            "Facility data seeded successfully."))
