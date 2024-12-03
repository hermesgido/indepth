import datetime
from django.db import models

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
class Machine(models.Model):
    name = models.CharField(max_length=50)
    machine_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    
class Slot(models.Model):
    name = models.CharField(max_length=50)
    slot_number  = models.IntegerField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='slots/', null=True, blank=True)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    capacity = models.IntegerField()
    quantity_available = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    type = models.TextField(max_length=200, choices=CUSTOMER_TYPES)
    client_group = models.TextField(max_length=200, null=True, blank=True, choices=CLIENT_GROUPS)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    age = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True, choices=GENDERS)
    registered_machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

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
        return transactions.count()
    @property
    def today_kits_transactions(self):
        today = datetime.date.today()
        transactions = Transaction.objects.filter(customer=self, product_type="Kits", created_at__date=today)
        return transactions.count()
    
    def transactions(self):
        return Transaction.objects.filter(customer=self)
    def transaction_limit(self):
        type = self.type
        if type == "General Population":
            limits = { "condom": 3, "kits": 3}
            return  limits
        elif type == "Client Group":
            if self.client_group == "FSW":
                limits = { "condom": 3, "kits": 3}
                return  limits
            elif self.client_group == "MSM":
                limits = { "condom": 3, "kits": 3}
                return  limits
            elif self.client_group == "PWID":
                limits = { "condom": 3, "kits": 3}
                return  limits
            elif self.client_group == "MAT":
                limits = { "condom": 3, "kits": 3}
                return  limits
            elif self.client_group == "AGYW":
                limits = { "condom": 3, "kits": 3}
    
    
        
    


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    amount = models.IntegerField()
    product_type = models.CharField(max_length=50, null=True, blank=True, choices=PRODUCT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
