from django.db import models
from django.core.exceptions import ValidationError

class CommonAbstract(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True)
    updated_by = models.CharField(max_length=50, default=None, blank=True, null=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.updated_at < self.created_at:
            raise ValidationError("Updated date cannot be earlier than created date.")

class Vehicle_category(CommonAbstract):
    no_of_seats = models.IntegerField()

    # def save(self, *args, **kwargs):
    #     if not self.created_by:
    #         # If created_by is not set, set it to the current user
    #         self.created_by = self._request.user
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Vehicle(CommonAbstract):
    type_of_vehicle = models.ForeignKey(Vehicle_category, on_delete=models.PROTECT)
    vehicle_num = models.CharField(max_length=10)

    # def save(self, *args, **kwargs):
    #     if not self.created_by:
    #         # If created_by is not set, set it to the current user
    #         self.created_by = self._request.user
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Trip(CommonAbstract):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    num_of_people = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.created_by:
            # If created_by is not set, set it to the current user
            self.created_by = self._request.user
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("End date cannot be earlier than start date.")
        if self.num_of_people <= 0:
            raise ValidationError("Number of people must be greater than zero.")




# payments/models.py


# class Payment(models.Model):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=3, default='INR')
#     razorpay_payment_id = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product