from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class event(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)
 
class event(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)
           
class food(models.Model):
    name = models.CharField(max_length=250)
    price= models.FloatField()
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name= models.CharField(max_length=250)
    price= models.FloatField()
    image= models.ImageField(upload_to='product/')
    image1 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image2 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image3 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    image4 = models.ImageField(upload_to='path/to/upload/', null=True, blank=True)
    description= models.TextField()
    location=models.TextField()
    event= models.ForeignKey(event, on_delete=models.CASCADE,null=True)
    capacity=models.TextField()

    def __str__(self):
        return str(self.name)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=225)
    address=models.TextField()
    phone=models.CharField(max_length=12)


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    date = models.DateField()
    duration = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.name} - {self.product.name}"

    class Meta:
        ordering = ['-created_at']


class BookingFood(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='food_items')
    food = models.ForeignKey(food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.booking.name} - {self.food.name} (x{self.quantity})"

    @property
    def total_price(self):
        return self.food.price * self.quantity