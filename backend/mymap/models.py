from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
from PIL import Image

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name= last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email = email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(default=date.today, blank=True)
    sign_in_date = models.DateField(auto_now_add=True)
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    username = models.CharField(max_length = 20, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    description = models.TextField(blank = True, max_length = 300)
    image = models.ImageField(upload_to='tfe/uploads/', null=True, blank=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['image']
    """
    Use what's in this to have a better database later:
    https://stackoverflow.com/questions/310540/best-practices-for-storing-postal-addresses-in-a-database-rdbms
    """

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name + " (" + self.email + ")"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        ordering = ['sign_in_date']

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    location = models.PointField(blank=True, geography=True, null=True)
    in_progress = models.BooleanField(default=True)
    is_recurrent = models.BooleanField(default=False)
    
    class ItemType(models.TextChoices):
        DONATION = 'DN', _('Donation')
        LOAN = 'LN', _('Loan')
        BARTER = 'BR', _('Request')
    
    item_type = models.CharField(
        max_length=2,
        choices=ItemType.choices,
        default=ItemType.BARTER
    )

    class Categories(models.TextChoices):
        FOOD = 'FD', _('Food')
        ANIMALS = 'AN', _('Animals')
        ENTERTAINMENT = 'EN', _('Arts and Entertainments')
        COLLECTORS = 'CL', _('Collectors')
        HELPING = 'HL', _('Helping hand')
        DIY = 'DY', _('DIY')
        BEAUTY = 'BT', _('Beauty and Well-being')
        CHILDHOOD = 'CH', _('Childhood')
        IT = 'IT', _('IT and Multimedia')
        GARDEN = 'GD', _('Garden')
        HOUSE = 'HS', _('House')
        HOLIDAYS = 'HD', _('Holidays and Week-end')
        BOOK = 'BK', _('Books, CDs and DVDs')
        SPORT = 'SP', _('Sport and Leisure')
        TRANSPORT = 'TS', _('Transport and vehicle')
        OTHER = 'OT', _('Other')
    
    category1 = models.CharField(
        max_length=2,
        choices = Categories.choices,
        default='OT'
    )
    category2 = models.CharField(
        max_length=2,
        choices = Categories.choices,
        blank = True,
    )
    category3 = models.CharField(
        max_length=2,
        choices = Categories.choices,
        blank = True,
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="items", on_delete=models.CASCADE, null=True)

    image = models.ImageField(upload_to='tfe/uploads/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name + ' : ' + self.description + ' (' + self.category1 + ')'

    class Meta:
        ordering = ['name']

class ItemImage(models.Model):
    image = models.ImageField(upload_to='tfe/uploads/')
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 512 or img.width > 512:
            output_size = (512, 512)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) -> str:
        return 'Image related to ' + self.item.name + '.'

    class Meta:
        ordering = ['item']

class Conversation(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conversations_as_owner", on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conversations_as_buyer", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']

class Message(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="messages", on_delete=models.CASCADE, null=True)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
