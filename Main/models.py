from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):

    ROLE_CHOICES = [
        ('user', 'User'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name or ''}"

    def __str__(self):
        return self.user.username

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    

#MODELS FOR RESERVATION FORM
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who made the reservation
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    
    # Date and Time Fields
    pickup_date = models.DateField(null=True, blank=True)
    dropoff_date = models.DateField(null=True, blank=True)
    pickup_time = models.TimeField(null=True, blank=True)
    dropoff_time = models.TimeField(null=True, blank=True)

    PICKUP_LOCATION_CHOICES = [
        ('lucena_grand_terminal_pick', 'Lucena Grand Terminal'),
        ('groto_lucban_quezon_pick', 'Groto Lucban Quezon'),
        ('tayabas_city_quezon_pick', 'Tayabas City Quezon'),
    ]
    
    DROPOFF_LOCATION_CHOICES = [
        ('lucena_grand_terminal_drop', 'Lucena Grand Terminal'),
        ('groto_lucban_quezon_drop', 'Groto Lucban Quezon'),
        ('tayabas_city_quezon_drop', 'Tayabas City Quezon'),
    ]

    # Location Fields
    pickup_location = models.CharField(max_length=255, choices= PICKUP_LOCATION_CHOICES)
    dropoff_location = models.CharField(max_length=255, choices= DROPOFF_LOCATION_CHOICES)

    #     # Location Fields
    # pickup_location = models.CharField(max_length=255)
    # dropoff_location = models.CharField(max_length=255)
    
    # Vehicle and Payment
    vehicle = models.CharField(max_length=100, choices=[
        ('Toyota Corolla', 'Class A - Toyota Corolla - 6 Seats'),
        ('Modernized PUV V1', 'Class B - Modernized PUV V1 - 15 Seats'),
        ('Modernized PUV V2', 'Class B - Modernized PUV V2 - 15 Seats'),
    ])
    payment_method = models.CharField(max_length=20, choices=[
        ('gcash', 'GCash'),
        ('cash', 'On-hand Payment (CASH)')
    ])
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    roundtrip = models.BooleanField(default=False)

    # GCash Receipt Upload
    gcash_receipt = models.ImageField(upload_to='receipts/', blank=True, null=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.full_name} ({self.pickup_date})"
    
    def calculate_fare(self):
        # Define kilometers for each route
        distance_map = {
            ('lucban_terminal', 'lucena_grand_terminal'): 23.2,
            ('lucban_terminal', 'tayabas_city_public_market'): 12.9,
            ('tayabas_city_public_market', 'lucena_grand_terminal'): 9.2,
        }

        # Get distance for the selected route
        distance = distance_map.get(
            (self.pickup_location.split('_pick')[0], self.dropoff_location.split('_drop')[0]),
            0
        )
        
        # Compute fare per kilometer
        fare_per_km = 17 / 4  # 17 pesos per 4 kilometers
        base_fare = distance * fare_per_km
        
        # Get seat count based on the vehicle
        seat_map = {
            'Toyota Corolla': 6,
            'Modernized PUV V1': 15,
            'Modernized PUV V2': 15,
        }
        seat_count = seat_map.get(self.vehicle, 0)
        
        # Calculate total fare
        total_fare = base_fare * seat_count
        if self.roundtrip:
            total_fare *= 2  # Double the fare for roundtrip
        
        return round(total_fare, 2)

#ADMIN ANNOUNCEMENTS
class Announcement(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='announcements/')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Announcement {self.id}"