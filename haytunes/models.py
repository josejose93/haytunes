import uuid

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.DecimalField(null=True, max_digits=8, decimal_places=2, validators=[MinValueValidator(0.001)])

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[a-zA-Z]*$', message='Name must be Alphabetic', code='invalid_name')])

    class Meta:
        permissions = (("can_admin_content", "Admin content in page"),)

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular product across')
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.001)])
    author = models.CharField(max_length=100)
    LOAN_TYPE = (
        ('i', 'Image'),
        ('a', 'Audio'),
        ('v', 'Video'),
    )
    type = models.CharField(max_length=1, choices=LOAN_TYPE, help_text="Types of contents")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    #owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ManyToManyField(User, help_text='Select an owner for this product.', blank=True)
    content = models.FileField(upload_to='product')

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.id} ({self.title})'

    def display_owner(self):
        return ', '.join(owner.first_name for owner in self.owner.all()[:3])

    display_owner.short_description = 'Owner'


