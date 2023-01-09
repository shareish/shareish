from datetime import date

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point
from django.contrib.contenttypes.fields import GenericRelation

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
            last_name=last_name,
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
            last_name=last_name,
            email=email,
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
    username = models.CharField(max_length=20, default='')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    description = models.TextField(blank=True, max_length=300)
    homepage_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    ref_location = models.PointField(blank=True, geography=True, null=True, default=Point(0.0, 0.0))
    use_ref_loc = models.BooleanField(default=False)
    dwithin_notifications = models.PositiveSmallIntegerField(null=True,default=10, help_text='Enter maximum distance for new item notifications')
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='image', on_delete=models.CASCADE
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 256 or img.width > 256:
            output_size = (256, 256)
            img.thumbnail(output_size)
            img.save(self.image.path, format=img.format)

    def __str__(self) -> str:
        return self.url

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
    startdate = models.DateTimeField(default=timezone.now)
    enddate = models.DateTimeField(null=True)
    in_progress = models.BooleanField(default=True, db_index=True)
    is_recurrent = models.BooleanField(default=False)
    hitcount = models.IntegerField(verbose_name='Hit Count',default=0)

    
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
        FOOD = 'FD', _('Food and Supplies')
        ANIMALS = 'AN', _('Pets and Animals')
        ENTERTAINMENT = 'EN', _('Arts, Culture, and Entertainments')
        COLLECTORS = 'CL', _('Collectors')
        HELPING = 'HL', _('Helping hand and Manual Labor')
        ADMINIT = 'AT',  _('Administrative tasks')
        DIY = 'DY', _('Do-it-Yourself')
        BEAUTY = 'BT', _('Beauty and Well-being')
        HEALTH = 'HE', _('Health')
        ENERGY = "EY", _('Energy and Heating')
        CHILDHOOD = 'CH', _('Childhood')
        CLOTHES = 'CO', _('Clothes')
        IT = 'IT', _('Multimedia Hardware')
        CS = 'CS', _('Informatics Software')
        GARDEN = 'GD', _('Gardening and Nature')
        HOUSE = 'HS', _('Living spaces and Housing')
        TOOLS = 'EQ', _('Tools and Ustensils')
        HOLIDAYS = 'HD', _('Holidays, Week-end, Leisures')
        BOOK = 'BK', _('Books, CDs and DVDs')
        SPORT = 'SP', _('Sports')
        TRANSPORT = 'TS', _('Transportation, Delivery, Pick-up, Moving')
        VEHICLE = 'VE', _('Vehicles and Means of transport')
        OTHER = 'OT', _('Other')

    category1 = models.CharField(
        max_length=2,
        choices=Categories.choices,
        default='OT'
    )
    category2 = models.CharField(
        max_length=2,
        choices=Categories.choices,
        blank=True,
    )
    category3 = models.CharField(
        max_length=2,
        choices=Categories.choices,
        blank=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="items", on_delete=models.CASCADE, null=True
        )

    def current_hit_count(self):
        return self.hit_count.hits
    
    def __str__(self) -> str:
        return self.name + ' : ' + self.description + ' (' + self.category1 + ')'

    class Meta:
        #ordering = ['name']
        ordering = ['startdate']


class ItemImage(models.Model):
    image = models.ImageField(upload_to='')
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        print(img.filename)
        print(img.size)

        MAX_SIZE = 1024
        if img.height > MAX_SIZE or img.width > MAX_SIZE:
            print("resize")
            output_size = (MAX_SIZE, MAX_SIZE)
            img.thumbnail(output_size, resample=Image.LANCZOS)
            img.save(self.image.path, format=img.format)

    def __str__(self) -> str:
        return self.url

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
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="conversations_as_owner", on_delete=models.CASCADE,
        null=True
        )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="conversations_as_buyer", on_delete=models.CASCADE,
        null=True
        )
    item = models.ForeignKey(
        Item, related_name="conversations", on_delete=models.CASCADE, null=True
        )

    class Meta:
        ordering = ['name']


class Message(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="messages", on_delete=models.CASCADE, null=True
        )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE, null=True
        )
    date = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']
