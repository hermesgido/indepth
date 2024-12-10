import logging
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from backend.models import Customer, Facility, Machine, Slot, Transaction
from django.db.models import Q

from .helpers import *



class VendingMashineCallBackAPI(APIView):
    def get(self, request):
        print(request.data)
        print("Getting.....")
        return Response({"status": "success", "message": "Machine status updated successfully"})

    def post(self, request):
        content_type = request.content_type
        if content_type == 'application/json':
            data = request.data
        elif content_type == 'application/x-www-form-urlencoded':
            data = request.POST.dict()
        else:
            return Response({"status": "Unsupported content type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        print("Received Data Is: {0}".format(request.data))

        fun_code = request.data.get("FunCode")
        if fun_code == "1000":
            print("Code 1000")
            # return handle_restock_1000(request)
        elif fun_code == "2000":
            print("Code 2000")
            # return verify_pickup_code_2000(request)
        elif fun_code == "4000":
            print("Code 4000 Received")
            return Response({
                "Status": "0",
                "MsgType": "0",
                "SlotNo": 2,
                "ProductID": "222",
                "TradeNo": "2222",
                "Err": "success"
            })
            return polling_interface_4000(request)
        # elif fun_code == "5000":
        #     return delivery_result_feedback_5000(request)
        # elif fun_code == "5001":
        #     return restock_result_feedback_5001(request)
        return Response({"Status": "1", "Err": "Invalid FunCode"}, status=400)