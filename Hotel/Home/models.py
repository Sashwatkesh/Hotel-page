from random import choices
from secrets import choice
from django.contrib.auth.models import User
from django.db import models
import uuid
# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default = uuid.uuid4, editable = False, primary_key = True)
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length =100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length =100)
    hotel_price = models.IntegerField() 
    desc = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)

    
    def __str__(self) -> str:
        return self.hotel_name

class HotelImages(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'hotel_images')


class HotelBookimg(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_book", on_delete=models.CASCADE)
    user =  models.ForeignKey(User, related_name="hotel_image", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=100  ,choices =(('Pre Paid','Pre Paid'),('Post Paid','Post Paid')))
