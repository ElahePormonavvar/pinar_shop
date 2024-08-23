from django.shortcuts import render,redirect
import requests
import json
import requests
from django.views import View
from django.contrib import messages

from apps.orders.models import Order,OrderState
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from apps.payments.models import Payment
from apps.accounts.models import Customer
import utils    
from .zarinpal import ZarinPal
from django.http import HttpResponse



if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = "https://{sandbox}.api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://{sandbox}.api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://{sandbox}.zarinpal.com/pg/StartPay/{authority}"

pay = ZarinPal(merchant=settings.MERCHANT, call_back_url="http://127.0.0.1:8000//payment/verify/")
merchant=settings.MERCHANT

def send_request(request,order_id):
    # email and mobile is optimal
    
    if utils.has_internet_connection():
        
        user =  request.user
        order = Order.objects.get(id = order_id)
        
        payment = Payment.objects.create(
            order = order,
            customer = Customer.objects.get(user_id = request.user),
            amount = order.get_order_total_price(),
            description = 'پرداخت شما با زرین پال انجام شد'
        )
        
        payment.save()
        
        request.session['payment_session'] = {
            'order_id':order.id,
            'payment_id':payment.id,
            
        }
        
        response = pay.send_request(amount=order.get_order_total_price(), description='توضیحات مربوط به پرداخت', email="Example@test.com",
                                mobile=user.mobile_number)
        if response.get('error_code') is None:
            # redirect object
            return response
        else:
            return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
        
    else:
        
        messages.error(request,'اتصال اینرنت شما قابل تایید نیست','danger')
        return redirect('main:index')
        

def verify(request):
    response = pay.verify(request=request, amount='1000')

    if response.get("transaction"):
        if response.get("pay"):
            return HttpResponse('تراکنش با موفقیت انجام شد')
        else:
            return HttpResponse('این تراکنش با موفقیت انجام شده است و الان دوباره verify شده است')
    else:
        if response.get("status") == "ok":
            return HttpResponse(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}')
        elif response.get("status") == "cancel":
            return HttpResponse(f'تراکنش ناموفق بوده است یا توسط کاربر لغو شده است'
                                f'Error Message: {response.get("message")}')

from django.http import JsonResponse
class Zarin_pal_view_verfiy(LoginRequiredMixin, View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session['payment_session']['order_id']
        payment_id = request.session['payment_session']['payment_id']
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(id=payment_id)

        if t_status == 'OK':
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            req_data = {
                "merchant_id": merchant,
                "amount": order.get_order_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_finaly = True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()
                    payment.is_finaly = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect('payments:show_sucess', 'کد رهگیری شما : {}'.format(str(req.json()['data']['ref_id'])))
                elif t_status == 101:
                    order.is_finaly = True
                    order.save()
                    payment.is_finaly = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect('payments:show_sucess', 'کد رهگیری شما : {}'.format(str(req.json()['data']['ref_id'])))
                else:
                    payment.status_code = t_status
                    payment.save()
                    return redirect('payments:show_verfiy_unmessage', 'کد رهگیری شما : {}'.format(str(req.json()['data']['ref_id'])))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return JsonResponse({
                    "status": 'ok',
                    "message": e_message,
                    "error_code": e_code
                })
        else:
            # payment.status_code = t_status
            # payment.save()
            return redirect('payments:show_verfiy_unmessage','پرداخت توسط کاربر لغو شد')


def show_verfiy_message(request,message):
    return render(request,'payments_app/payment.html',{'message':message})

def show_verfiy_unmessage(request,message):
    return render(request,'payments_app/unpayment.html',{'message':message})








# from django.shortcuts import render,redirect
# from django.views import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from apps.orders.models import Order
# import requests
# import json
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Payment
# from apps.accounts.models import Customer
# from django.conf import settings
# from django.http import HttpResponse
# # ---------------------------------------------------------------------------------------------
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'

# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# amount = 1000
# description='پرداخت از طریق درگاه زرین پال انجام شد'
# CallbackURL = 'http://127.0.0.1:8080/payments/verify/'

# # ---------------------------------------------------------------------------------------------
# class ZarinpalPaymentView(LoginRequiredMixin,View):
#     def get(self,request,order_id):
#         try:
#             order=Order.objects.get(id=order_id)
#             # payment=Payment.objects.create(
#             #     order=order,
#             #     customer=Customer.objects.get(user=request.user),
#             #     amount=order.get_order_total_price(),
#             #     description=description,
#             #     )
#             # payment.save()
#             # request.session['payment_session']={
#             #     'order_id': order.id,
#             #     'payment_id':payment.id,
#             # }
#             user=request.user
#             data = {
#                 "MerchantID":settings.MERCHANT,
#                 "Amount": order.get_order_total_price(), 
#                 "Description": description,
#                 "Phone":user.mobile_number ,
#                 "CallbackURL": CallbackURL,
#                 }
#             data = json.dumps(data)
#             headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#             try:
#                 response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
#                 if response.status_code == 200:
#                     response = response.json()
#                     if response['Status'] == 100:
#                         return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
#                     else:
#                         return {'status': False, 'code': str(response['Status'])}
#                 return response       
#             except requests.exceptions.Timeout:
#                 return {'status': False, 'code': 'timeout'}
#             except requests.exceptions.ConnectionError:
#                 return {'status': False, 'code': 'connection error'}     
#         except ObjectDoesNotExist:
#             return redirect('orders:checkout_order',order_id)

# # --------------------------------------------------------------------------------------------------------------
# # class ZarinpalPaymentVerifyView(LoginRequiredMixin,View):
#     def get(self,request,authority):
#         order_id=request.session['payment_session']['order_id']
#         payment_id=request.session['payment_session']['payment_id']
#         order=Order.objects.get(id=order_id)
#         payment=Payment.objects.get(id=payment_id)

#         data = {
#             "MerchantID":settings.MERCHANT,
#             "Amount": order.get_order_total_price(),
#             "Authority": authority,
#         }
#         data = json.dumps(data)
#         # set content length by data
#         headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
#         response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 order.is_finaly=True
#                 order.save()
#                 payment.is_finaly=True
#                 payment.status_code=response['Status']
#                 payment.ref_id=str(response['RefID'])
#                 payment.save()
                
#             elif response['Status'] == 101:
#                 order.is_finaly=True
#                 order.save()
#                 payment.is_finaly=True
#                 payment.status_code=response['Status']
#                 payment.ref_id=str(response['RefID'])
#                 payment.save()    

#             else:
#                 payment.status_code=response['Status']  
#                 payment.save() 

#         return response