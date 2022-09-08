from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import date
from PIL import Image

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, username, first_name, last_name):
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

    def create_superuser(self, email, password, username, first_name, last_name):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name= last_name,
            email = email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(default=date.today, blank=True)
    sign_in_date = models.DateField(auto_now_add=True)
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    username = models.CharField(max_length = 20, default='')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    description = models.TextField(blank = True, max_length = 300)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
    """
    Use what's in this to have a better database later:
    https://stackoverflow.com/questions/310540/best-practices-for-storing-postal-addresses-in-a-database-rdbms
    """

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        ordering = ['sign_in_date']

class UserImage(models.Model):
    image = models.ImageField(upload_to='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='image', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 256 or img.width > 256:
            output_size = (256, 256)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) -> str:
        return 'Image related to ' + self.user.email + '.'

    @property
    def path(self):
        return self.image.path

    @property
    def url(self):
        return "{}/api/v1/user_image/{}/image".format(settings.API_URL, self.pk)

    class Meta:
        ordering = ['user']

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    location = models.PointField(blank=True, geography=True, null=True)
    startdate = models.DateField(default=timezone.now)
    enddate = models.DateField(null=True)
    in_progress = models.BooleanField(default=True, db_index=True)
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

    def __str__(self) -> str:
        return self.name + ' : ' + self.description + ' (' + self.category1 + ')'

    class Meta:
        ordering = ['name']

class ItemImage(models.Model):
    image = models.ImageField(upload_to='')
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 256 or img.width > 256:
            output_size = (256, 256)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) -> str:
        return 'Image related to ' + self.item.name + '.'

    @property
    def path(self):
        return self.image.path

    @property
    def url(self):
        return "{}/api/v1/item_image/{}/image".format(settings.API_URL, self.pk)

    class Meta:
        ordering = ['item']

class Conversation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conversations_as_owner", on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conversations_as_buyer", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, related_name="conversations", on_delete=models.CASCADE, null=True)

    up2date_owner = models.BooleanField(default=True)
    up2date_buyer = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

class Message(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="messages", on_delete=models.CASCADE, null=True)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
