from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.models import Machine, Transaction


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
    msg_type = "0"
    machine_id = request.data.get("mashineId")
    machine = Machine.objects.get(machine_id=machine_id)
    if msg_type == "0":
        pendings = Transaction.objects.filter(machine = machine, status="Pending")
        if pendings.exists():
            products_amout = 1
            slots = machine.slot
            slot_string = ""
        
        return Response({
            "Status": "0",
            "MsgType": "0",
            "SlotNo": request.data.get("SlotNo"),
            "ProductID": request.data.get("ProductID"),
            "TradeNo": request.data.get("TradeNo"),
            "Err": "success"
        })
    # elif msg_type == "1":
    #     return Response({
    #         "Status": "0",
    #         "MsgType": "1",
    #         "SlotNo": request.data.get("SlotNo"),
    #         "Capacity": request.data.get("Capacity"),
    #         "Quantity": request.data.get("Quantity"),
    #         "Err": "success"
    #     })
    return Response({"Status": "1", "Err": "Invalid MsgType"}, status=400)


def delivery_result_feedback_5000(request):
    return Response({
        "Status": "0",
        "SlotNo": request.data.get("SlotNo"),
        "TradeNo": request.data.get("TradeNo"),
        "Err": "success"
    })


def restock_result_feedback_5001(request):
    return Response({
        "Status": "0",
        "SlotNo": request.data.get("SlotNo"),
        "TradeNo": request.data.get("TradeNo"),
        "Err": "success"
    })
