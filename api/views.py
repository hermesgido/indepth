import datetime
import logging
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .vending import VendingMashineCallBackAPI
from backend.models import Customer, Facility, Machine, Slot, Transaction, TransactionLog
from django.db.models import Q

class HelloWorldView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, World!"})


def get_customer_data(customer):
    return {
        "id": customer.id,
        "type": customer.type,
        "client_group": customer.client_group,
        "phone_number": customer.phone_number,
        "location": customer.location,
        "condom_transaction_limit": customer.condom_transaction_limit,
        "kits_transaction_limit": customer.kits_transaction_limit,
        "today_condom_transactions": customer.today_condom_transactions,
        "today_kits_transactions": customer.today_kits_transactions,
        # special for kvp customers
        "pin": customer.pin,
        "pin_type": customer.pin_type,
        "expire_date": customer.expire_date,
        "description": customer.description,
        "status": customer.status,
        "hotspot": customer.hotspot,

        "created_at": customer.created_at,
        "updated_at": customer.updated_at,
    }


def get_transaction_data(transaction):
    return {
        "id": transaction.id,
        "customer": transaction.customer.phone_number,
        "machine": transaction.machine.machine_id,
        "amount": transaction.amount,
        "product_type": transaction.product_type,
        "created_at": transaction.created_at,
    }


class CustomerCreateAPIView(APIView):
    def post(self, request):
        machine = Machine.objects.filter(
            machine_id=request.data.get("machine_id")).first()
        if not machine:
            return Response({"status": "error", "message": "Machine not found"})
        custm = Customer.objects.filter(
            phone_number=request.data.get("phone_number")).first()
        if custm:
            return Response({"status": "error", "message": "Customer already exists"})
        type = "General Population"
        phone_number = request.data.get("phone_number")
        age = request.data.get("age")
        gender = request.data.get("gender")
        customer = Customer.objects.create(
            type=type,
            phone_number=phone_number,
            age=age,
            gender=gender,
            registered_machine=machine
        )
        customer.save()
        return Response({"status": "success", "data": get_customer_data(customer), "message": "Customer created successfully"})


class CustomerAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        type = request.query_params.get("type")
        print(type)
        if type == "pin":
            customer = Customer.objects.filter(pin=phone_number)
            if not customer.exists():
                return Response({"status": "error",             "type": type,
                                 "message": "Customer not found"})
            customer = customer.first()
        else:
            customer = Customer.objects.filter(phone_number=phone_number)
            if not customer.exists():
                return Response({"status": "error",             "type": type,
                                 "message": "Customer not found"})
            customer = customer.first()

        print(get_customer_data(customer))
        return Response({
            "status": "success",
            "type": type,
            "data": get_customer_data(customer)
        })


class TransactionCreateAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        product_type = request.data.get("product_type")
        pn = Q(phone_number=phone_number) | Q(pin=phone_number)
        customer = Customer.objects.filter(pn).first()
        if not customer:
            return Response({"status": "error", "message": "Customer not found"})
        if product_type == "Condoms":
            if customer.today_condom_transactions >= customer.condom_transaction_limit:
                return Response({"status": "error", "message": "Condom transaction limit reached"})
        if product_type == "Kits":
            if customer.today_kits_transactions >= customer.kits_transaction_limit:
                return Response({"status": "error", "message": "Kits transaction limit reached"})

        machine = Machine.objects.filter(
            machine_id=request.data.get("machine_id")).first()
        if not machine:
            return Response({"status": "error", "message": "Machine not found"})
        amount = request.data.get("amount")
        product_type = request.data.get("product_type")
        slot_number = request.data.get("slot_number")
        slot = Slot.objects.filter(
            machine=machine, slot_number=slot_number).first()
        transaction = Transaction.objects.create(
            customer=customer,
            machine=machine,
            amount=amount,
            product_type=product_type,
            slot=slot
        )
        transaction.save()
        # Save transaction logs
        # (TransactionLog.objects.create(transaction=transaction, machine=machine, slot=slot, product_type=product_type, index=i) for i in range(transaction.amount))
        print(transaction.amount)
        
        for i in range(transaction.amount):
            TransactionLog.objects.create(
                transaction=transaction,
                machine=machine,
                slot=slot,
                product_type=product_type,
                index=i,
            )
        return Response({"status": "success", "data": get_transaction_data(transaction), "message": "Transaction created successfully"})


class MachineSlotsAPIView(APIView):
    def get(self, request, machine_id=None):
        if machine_id is None:
            return Response({"status": "error", "message": "Machine ID is required"})
        if not machine_id:
            return Response({"status": "error", "message": "Invalid machine ID is requred"})
        machine = Machine.objects.filter(machine_id=machine_id).first()
        if not machine:
            return Response({"status": "error", "message": "Machine not found"})
        slots = Slot.objects.filter(machine=machine)
        data = []
        for slot in slots:
            data.append({
                "id": slot.id,
                "name": slot.name,
                "product_type": slot.product_type,
                "slot_number": slot.slot_number,
                "price": slot.price,
                "capacity": slot.capacity,
                "quantity": slot.quantity_available,
                # "created_at": slot.created_at,
                # "updated_at": slot.updated_at,
            })
        return Response({"status": "success", "data": data})


# Set up logging
logger = logging.getLogger(__name__)


class SetMachineIdAndPassword(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            machine_id = request.data.get("machine_id")
            password = request.data.get("password")
            phone_number = request.data.get("phone_number")

            # Validate required fields
            if not all([machine_id, password, phone_number]):
                return Response(
                    {"status": "error", "message": "All fields are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if machine exists
            machine = Machine.objects.filter(machine_id=machine_id).first()
            if not machine:
                return Response(
                    {"status": "error", "message": "Machine not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check if facility exists
            facility = Facility.objects.filter(
                mobile_no=phone_number, machine=machine).first()
            if not facility:
                return Response(
                    {"status": "error", "message": "Facility not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Update machine password
            machine.password = password # Hash the password
            machine.save()

            return Response(
                {"status": "success", "message": f"Machine password set successfully "},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Log the exception for debugging purposes
            logger.error(f"An error occurred: {e}")

            # Return a generic error response
            return Response(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred. Please try again later, {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
