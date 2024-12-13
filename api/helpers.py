import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.models import Machine, Transaction, TransactionLog


def handle_restock_1000(request):
    slot_no = request.data.get("SlotNo")
    quantity = request.data.get("Quantity")
    return Response({
        "Status": "0",
        "SlotNo": slot_no,
        "TradeNo": request.data.get("TradeNo"),
        "Err": "success"
    })


def verify_pickup_code_2000(request):
    slot_no = request.data.get("SlotNo")
    product_id = request.data.get("ProductID")
    return Response({
        "Status": "0",
        "SlotNo": slot_no,
        "ProductID": product_id,
        "TradeNo": request.data.get("TradeNo"),
        "Err": "success"
    })


def polling_interface_4000(request):
    machine_id = request.data.get("MachineID")
    machine = Machine.objects.filter(machine_id=machine_id).first()
    if not machine:
       return Response({"Status": "1", "Err": "Invalid Machine ID"}, status=400)
    
    pendings = TransactionLog.objects.filter(machine=machine, status="Pending").first()
    if not pendings:
        return Response({"Status": "1", "Err": "No pending transaction"}, status=400)
    else:
        print(request.data)
        print("Peninggg obtained machine")
        print(pendings)
        print("Peninggg obtained machine 22")
        pendings.status = "Processing"
        trade_number = f"{
            pendings.product_type}-{pendings.id}-{random.randint(100001, 1000001)}"
        pendings.trade_number = trade_number
        pendings.save()
        response = {
            "Status": "0",
            "MsgType": "0",
            "SlotNo": str(pendings.slot.slot_number),
            "ProductID": "222", 
            "TradeNo": trade_number,  
            "Err": "success"
        }
        print("TResponse top")
        print(response)
        print("TResponse bottom")
        return  Response(response)
    return Response({"Status": "1", "Err": "Invalid MsgType"}, status=400)


STATUS_DESCRIPTIONS = {
    0: "Dispensing successful",
    1: "Dispensing failed",
    2: "Dispensing successful, but order number is missing or incorrect",
    3: "Dispensing failed, but order number is missing or incorrect",
    4: "Dispensing result unknown",
}



def delivery_result_feedback_5000(request):
    data = request.data
    funcode = data.get('FunCode')           # Interface number
    machine_id = data.get('MachineID')      # Machine ID
    pay_type = data.get('PayType')          # Payment type
    trade_no = data.get('TradeNo')          # Serial number
    slot_no = data.get('SlotNo')            # Slot number
    status = data.get('Status')             # Dispensing status
    delivery_time = data.get('Time')        # Delivery time
    amount = data.get('Amount')             # Amount
    product_id = data.get('ProductID')      # Product ID
    name = data.get('Name')                 # Product name
    product_type = data.get('Type')         # Product type
    print("Logiing 5000")
    
    
    log = TransactionLog.objects.filter(trade_number=trade_no).first()
    if log:
        if (status == "0" or status == "2"):
            log.status = "Completed"
            log.status_description = STATUS_DESCRIPTIONS.get(
                int(status), "Unknown status")
            log.feedback_status = status
            log.save()
            return Response({
                "Status": "0",
                "SlotNo": request.data.get("SlotNo"),
                "TradeNo": request.data.get("TradeNo"),
                "Err": "success"
            })
        else:
            log.status = "Failed"
            log.status_description = STATUS_DESCRIPTIONS.get(
                int(status), "Unknown status")
            log.feedback_status = status
            log.save()
            return Response({
                "Status": "0",
                "SlotNo": request.data.get("SlotNo"),
                "TradeNo": request.data.get("TradeNo"),
                "Err": "success"
            })
    else:
        return Response({"Status": "1", "Err": "Invalid TradeNo"}, status=400)
            
        
        



def restock_result_feedback_5001(request):
    return Response({
        "Status": "0",
        "SlotNo": request.data.get("SlotNo"),
        "TradeNo": request.data.get("TradeNo"),
        "Err": "success"
    })
