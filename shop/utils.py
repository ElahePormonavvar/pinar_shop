# تولید عدد تصادفی 5 رقمی
# 10000   99999
def creat_random_code(count):
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)

# ----------------------------------------------------------------
from kavenegar import *
def send_sms(mobile_number,token):   
    pass
    # 1000689696
    try:
        api =KavenegarAPI('3135443531774145637938476F58584E355A47326F356F4F77386B35594739323543434A622F64763778383D')
        params = {
             'receptor': mobile_number,
             'template' :'verifyy',
             'token': token,
             'type':'sms',
        }
        response = api.verify_lookup(params)
        return response 
    except APIException as error:
        print(f'error1:{error}')
    except HTTPException as error:
        print(f'error2:{error}')

# -------------------------------------------------------------
import os
# رشته هش شده غیرتکراری تولید میکند
from uuid import uuid4

class FileUpload:
    def __init__(self,dir,prefix):
        self.dir=dir
        self.prefix=prefix
    
    def upload_to(self,instans,filename):
        filename,ext=os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"
        
# ----------------------------------------------------------------
def price_by_delivery_tax(price,discount=0):
    delivery=25
    if price >200:
        delivery=0

    tax=(price+delivery)*0.09
    sum=price+delivery+tax
    sum=sum-(sum*discount/100)
    
    return int(sum),delivery,int(tax)

# ----------------------------------------------
import socket

def has_internet_connection():
    """
    Check if the device has an active internet connection.
    
    Returns:
        bool: True if the device has an active internet connection, False otherwise.
    """
    try:
        # Try to connect to a well-known website
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# --------------------------------------------------------------------------------
import jdatetime
def gregorian_to_jalali(date):
    jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
    return jalali_date.strftime('%Y/%m/%d')


