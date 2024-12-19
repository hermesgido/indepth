import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

CUSTOMER_TYPES = (
    ('General Population', 'General Population'),
    ('Client Group', 'Client Group'),
)

CLIENT_GROUPS = (
    ('FSW', 'FSW'),
    ('MSM', 'MSM'),
    ('PWID,', 'PWID,'),
    ('MAT,', 'MAT,'),
    ('AGYW,', 'AGYW,'),
)
GENDERS = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

PRODUCT_TYPES = (
    ('Condoms', 'Condoms'),
    ('Kits', 'Kits'),
)
PRODUCT_SUBTYPES = (
    ('Male Condoms', 'Male Condoms'),
    ('Female Condoms', 'Female Condoms'),
    ('Blood Kits', 'Blood Kits'),
    ('Oral Kits', 'Oral Kits'),
)


PIN_TYPES = (
    ('PERMANENT', 'PERMANENT'),
)


TRANSCTION_STATUSES  = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
)
class Machine(models.Model):
    name = models.CharField(max_length=50)
    machine_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    last_online = models.DateTimeField(null=True, blank=True)
    
    # def get_online_status(self):
    #     ##if last_online is 10 seconds ago then the machine is online
    #     if self.last_online and datetime.datetime.now() - self.last_online < datetime.timedelta(seconds=10):
    #         return "Online"
    #     else:
    #         return "Offline"
    def remained_condoms(self):
        slots = Slot.objects.filter(machine=self, product_type= "Condoms")
        return sum(slot.quantity_available for slot in slots)
    def remained_kits(self):
        slots = Slot.objects.filter(machine=self,  product_type="Kits")
        return sum(slot.quantity_available for slot in slots if slot.product_type == "Kits")
    def condom_capacity(self):
        return sum(slot.capacity for slot in Slot.objects.filter(machine=self, product_type="Condoms"))
    def kit_capacity(self):
        return sum(slot.capacity for slot in Slot.objects.filter(machine=self, product_type="Kits"))
        
        
    
    def __str__(self):
        return self.name + self.machine_id
    
class Slot(models.Model):
    name = models.CharField(max_length=50)
    slot_number  = models.IntegerField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='slots/', null=True, blank=True)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    product_subtype = models.CharField(max_length=50, choices=PRODUCT_SUBTYPES, blank=True, null=True)
    capacity = models.IntegerField()
    quantity_available = models.IntegerField()
    price = models.IntegerField(null=True, blank=True)
    product_image = models.ImageField(upload_to="product_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def stock(self):
        return f"{self.quantity_available}/{self.capacity}"
    
    def get_product_id(self):
        if self.product_type == "Kits":
            return "222"
        else:
            return "111"
    
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    type = models.TextField(max_length=200, choices=CUSTOMER_TYPES)
    client_group = models.TextField(max_length=200, null=True, blank=True, choices=CLIENT_GROUPS)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=GENDERS)
    registered_machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    ##for KVP PINS
    pin = models.CharField(max_length=50, null=True, blank=True, unique=True)
    pin_type = models.CharField(
        max_length=50, null=True, blank=True, choices=PIN_TYPES)
    expire_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    hotspot = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.phone_number if self.phone_number else self.pin
    
    

    @property
    def condom_transaction_limit(self):
        return self.transaction_limit()["condom"]
    
    @property
    def kits_transaction_limit(self):
        return self.transaction_limit()["kits"]
    
    @property       
    def today_condom_transactions(self):
        today = datetime.date.today()
        transactions = Transaction.objects.filter(customer=self, product_type="Condoms", created_at__date=today)
        transaction_logs_count = TransactionLog.objects.filter(
            transaction__in=transactions).count()
        return transaction_logs_count

        return transactions.count()
    @property
    def today_kits_transaction_logs(self):
        today = datetime.date.today()
        transactions = Transaction.objects.filter(customer=self,product_type="Kits",created_at__date=today)
        transaction_logs_count = TransactionLog.objects.filter(transaction__in=transactions).count()
        return transaction_logs_count
    
    def transactions(self):
        return Transaction.objects.filter(customer=self)
    def transaction_limit(self):
        type = self.type
        if type == "General Population":
            limits = { "condom": 3, "kits": 3}
            return  limits
        elif type == "Client Group":
            if self.client_group == "FSW":
                limits = { "condom": 5, "kits": 3}
                return  limits
            elif self.client_group == "MSM":
                limits = { "condom": 5, "kits": 3}
                return  limits
            elif self.client_group == "PWID":
                limits = { "condom": 5, "kits": 3}
                return  limits
            elif self.client_group == "MAT":
                limits = { "condom": 5, "kits": 3}
                return  limits
            elif self.client_group == "AGYW":
                limits = { "condom": 5, "kits": 3}

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    dispensed_amount = models.IntegerField(default=0)
    dispensed_successful_amount = models.IntegerField(default=0)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.CharField(
        max_length=50, null=True, blank=True, choices=PRODUCT_TYPES, )
    status = models.CharField(max_length=50, null=True,
                              blank=True, choices=TRANSCTION_STATUSES, default="Pending")
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def dispensed_products_count(self):
        status = Q(feedback_status="0") | Q(feedback_status="2")
        return TransactionLog.objects.filter(transaction=self).filter(status).count()
    @property
    def get_status(self):
        if self.amount == self.dispensed_products_count:
            return "Succefully"
        elif self.amount > self.dispensed_products_count and self.dispensed_products_count !=0:
            return "Partially"
        else:
            return "Pending"
    
    def __str__(self):
        
        numbr = self.customer.phone_number if self.customer.phone_number else self.customer.pin
        return numbr  + self.product_type + str(self.amount)

class TransactionLog(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    product_type = models.CharField(
        max_length=50, null=True, blank=True, choices=PRODUCT_TYPES)
    status = models.CharField(max_length=50, null=True,  blank=True,
                              choices=TRANSCTION_STATUSES, default="Pending")
    status_description = models.CharField(max_length=200, null=True, blank=True)
    feedback_status = models.CharField(max_length=20, null=True, blank=True)
    trade_number = models.CharField(max_length=200, null=True, blank=True)
    index = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction.customer.phone_number if self.transaction.customer.phone_number else self.transaction.customer.pin + self.product_type + "Log" + " " + "Status " + self.status

class Facility(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE)
    district = models.CharField(
        max_length=100, verbose_name="District Supporting Ward",  null=True, blank=True)
    ward = models.CharField(
        max_length=100, verbose_name="Supporting Ward",  null=True, blank=True)
    hfrcode = models.CharField(
        max_length=15, verbose_name="HFR Code", null=True, blank=True)
    supporting_facility = models.CharField(
        max_length=100, verbose_name="Supporting Facility",  null=True, blank=True)
    responsible_cso = models.CharField(
        max_length=100, verbose_name="Responsible CSO",  null=True, blank=True)
    responsible_person = models.CharField(
        max_length=100, verbose_name="Responsible Person",  null=True, blank=True)
    mobile_no = models.CharField(max_length=15, verbose_name="Mobile Number", null=True, blank=True)
    app_password =  models.CharField(
        max_length=15, verbose_name="App Password", null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "District Support"
        verbose_name_plural = "District Supports"
        ordering = ['district', 'ward']

    def __str__(self):
        return f"{self.district} - {self.ward}"


class MachineLogs(models.Model):
    machine = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.CASCADE)
    response  =models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    function_code = models.CharField(max_length=23, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.machine.name} - {self.function_code}"