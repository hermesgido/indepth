from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.models import Customer, Machine, Slot, Transaction

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
        machine = Machine.objects.filter(machine_id=request.data.get("machine_id")).first()
        if not machine:
            return Response({"status": "error", "message": "Machine not found"})
        custm = Customer.objects.filter(phone_number=request.data.get("phone_number")).first()
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
            registered_machine = machine
        )
        customer.save()
        return Response({"status": "success", "data": get_customer_data(customer), "message": "Customer created successfully"})
    


class CustomerAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        customer = Customer.objects.filter(phone_number=phone_number)      
        if not customer.exists():
            return Response({"status": "error", "message": "Customer not found"})
        customer = customer.first()
        data = {
            "id": customer.id,
            "name": customer.name,
            "type": customer.type,
            "client_group": customer.client_group,
            "phone_number": customer.phone_number,
            "location": customer.location,
            "condom_transaction_limit": customer.condom_transaction_limit,
            "kits_transaction_limit": customer.kits_transaction_limit,
            "today_condom_transactions": customer.today_condom_transactions,
            "today_kits_transactions": customer.today_kits_transactions,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
        }
        return Response( {
            "status": "success",
            "data": data
        })
        
class TransactionCreateAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        product_type = request.data.get("product_type")
        customer = Customer.objects.filter(phone_number=phone_number).first()
        if not customer:
            return Response({"status": "error", "message": "Customer not found"})
        if product_type == "Condoms":
            if customer.today_condom_transactions >= customer.condom_transaction_limit:
                return Response({"status": "error", "message": "Condom transaction limit reached"})
        if product_type == "Kits":
            if customer.today_kits_transactions >= customer.kits_transaction_limit:
                return Response({"status": "error", "message": "Kits transaction limit reached"})
      
        machine = Machine.objects.filter(machine_id=request.data.get("machine_id")).first()
        if not machine:
            return Response({"status": "error", "message": "Machine not found"})
        amount = request.data.get("amount")
        product_type = request.data.get("product_type")
        transaction = Transaction.objects.create(
            customer=customer,
            machine=machine,
            amount=amount,
            product_type=product_type
        )
        transaction.save()
        return Response({"status": "success", "data": get_transaction_data(transaction), "message": "Transaction created successfully"})


class MachineSlotsAPIView(APIView):
    def get(self, request, machine_id):
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
                "price": slot.price,
                "capacity": slot.capacity,
                "quantity": slot.quantity_available,
                # "created_at": slot.created_at,
                # "updated_at": slot.updated_at,
            })
        return Response({"status": "success", "data": data})
       
    

# class VendingMashineCallBackAPI(APIView):
#     def get(self, request):
#         print(request.data)
#         print("Getting.....")


#         return Response({"status": "success", "message": "Machine status updated successfully"})
#     def post(self, request):
#         print(request.data)
#         print("Postingg")

#         return Response({"status": "success", "message": "Machine status updated successfully"})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VendingMashineCallBackAPI(APIView):
    def get(self, request):
        print(request.data)
        print("Getting.....")
        return Response({"status": "success", "message": "Machine status updated successfully"})

    def post(self, request):
        content_type = request.content_type
        print(request)
        
        # Parse data based on content type
        if content_type == 'application/json':
            data = request.data
        elif content_type == 'application/x-www-form-urlencoded':
            data = request.POST.dict()
        else:
            return Response({"status": "Unsupported content type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        print("Received Data:", data)
        
        funcode = data.get('FunCode')
        if funcode == '1000':
            print("Received Funcode 1000 Data:", data)
            response_data = {
                "Status": "0",
                "SlotNo": data.get("SlotNo", "Unknown"),
                "TradeNo": "20170802193446876",
                "ImageUrl": "http://xxx.com/201708029502889.png",
                "ImageDetailUrl": "http://xxx.com/20170801124323318.png",
                "Err": "success"
            }
            return Response(response_data)

        elif funcode == '2000':
            print("Received Funcode 2000 Data:", data)
            trade_no = data.get('TradeNo', "Unknown")
            session_code = data.get('SessionCode')
            if session_code == '123456789':
                response_data = {
                    "Status": "0",
                    "SlotNo": "23",
                    "ProductID": "1002356",
                    "TradeNo": trade_no,
                    "Err": "成功"
                }
                return Response(response_data)
            else:
                print("SessionCode does not match")
                return Response({"status": "failure", "message": "Invalid session code"}, status=status.HTTP_400_BAD_REQUEST)

        elif funcode == '4000':
            print("Received Funcode 4000 Data:", data)
            dt = { "Status": "0","MsgType":"0","TradeNo":"123456","SlotNo":"13","ProductID":"1005678692","Err":"NO Error"}
            return Response(dt)

        elif funcode == '5000':
            print("Received Funcode 5000 Data:", data)
            slot_no = data.get('SlotNo', "Unknown")  # Get SlotNo from request
            trade_no = data.get('TradeNo', "20170609123523569")  # Get TradeNo from request
            response_data = {
                "Status": "0",
                "SlotNo": slot_no,
                "TradeNo": trade_no,
                "Err": "success"
            }
            return Response(response_data)

        else:
            print("Unknown Funcode")
            return Response({"status": "failure", "message": "Unknown FunCode"}, status=status.HTTP_400_BAD_REQUEST)