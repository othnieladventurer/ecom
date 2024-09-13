from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) 

        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)


    def __str__(self):
        return self.name




class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    description= models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='products_picture/' ,default='images/default.jpg' )
    thumbnail = models.ImageField(upload_to='products_picture/thumbnail/' ,default='images/default.jpg' )
    date_created= models.DateTimeField(auto_now_add=timezone.now, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 

        super().save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
            
    def make_thumbnail(self, image, size=(300, 300)):
        img= Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.title)

        return thumbnail
    


    class Meta:
        ordering = ('-date_created',)


    def get_rating(self):
        reviews_total = 0

        for review in self.reviews.all():
            reviews_total += review.rating
        
        if reviews_total > 0:
            return reviews_total / self.reviews.count()
        
        return 0

    





class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.content} - {self.created_by} - {self.date_created}"






