import random
import string
from datetime import date

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.geos import Point
from djoser.signals import user_registered


def get_random_string(length):
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(options) for _ in range(length))

def get_random_file_name():
    return str(int(timezone.now().timestamp())) + "_" + get_random_string(5)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password, username, first_name, last_name):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

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


class MailNotificationFrequencies(models.TextChoices):
    INSTANTLY = 'I', _("Instantly")
    DAILY = 'D', _("Daily")
    WEEKLY = 'W', _("Weekly")
    NEVER = 'N', _("Never")


class MailNotificationFrequenciesConversations(models.TextChoices):
    INSTANTLY = 'I', _("Instantly")
    DAILY = 'D', _("Daily")
    NEVER = 'N', _("Never")


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(default=date.today, blank=True)
    sign_up_date = models.DateField(auto_now_add=True)
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    username = models.CharField(max_length=20, default="")
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="", max_length=300)
    homepage_url = models.URLField(blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    ref_location = models.PointField(blank=True, geography=True, null=True)
    use_ref_loc = models.BooleanField(default=False)
    mail_notif_freq_conversations = models.CharField(
        max_length=1,
        choices=MailNotificationFrequenciesConversations.choices,
        default=MailNotificationFrequenciesConversations.DAILY
    )
    mail_notif_freq_events = models.CharField(
        max_length=1,
        choices=MailNotificationFrequencies.choices,
        default=MailNotificationFrequencies.DAILY
    )
    mail_notif_freq_items = models.CharField(
        max_length=1,
        choices=MailNotificationFrequencies.choices,
        default=MailNotificationFrequencies.DAILY
    )
    dwithin_notifications = models.PositiveSmallIntegerField(
        null=True,
        default=10,
        help_text="Enter maximum distance for new item and event notifications"
    )
    save_item_viewing = models.BooleanField(default=True)

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
        ordering = ['-id']


class UserImage(models.Model):
    image = models.ImageField(upload_to='users_images')
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.image.name = get_random_file_name()
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        MAX_SIZE = 256
        if img.height > MAX_SIZE or img.width > MAX_SIZE:
            output_size = (MAX_SIZE, MAX_SIZE)
            img.thumbnail(output_size)
            img.save(self.image.path, format=img.format)

    def __str__(self) -> str:
        return self.url

    @property
    def path(self):
        return self.image.path

    @property
    def url(self):
        return "{}/api/v1/users/images/{}".format(settings.API_URL, self.pk)

    class Meta:
        ordering = ['user_id', '-id']


class UserMapExtraCategories(models.TextChoices):
    BOOKCASES = 'BKC', _("Public bookcases")
    DEFIBRILLATORS = 'DEF', _("Defibrillators")
    DRINKING_WATER_SPOTS = 'DWS', _("Drinking water spots")
    FOOD_BANKS = 'FDB', _("Food Banks")
    FOOD_SHARING = 'FDS', _("Food Sharing")
    FALLING_FRUITS = 'FLF', _("Falling fruits")
    FREE_SHOPS = 'FRS', _("Free shops")
    GIVE_BOXES = 'GVB', _("Give boxes")
    SOUP_KITCHENS = 'SPK', _("Soup Kitchens")


class UserMapExtraCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='map_ecats', on_delete=models.CASCADE)
    category = models.CharField(max_length=3, choices=UserMapExtraCategories.choices)
    selected = models.BooleanField(default=True)
    update_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user_id', 'category']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'],
                name='unique__mymap_usermapextracategory__user_category'
            )
        ]


class Item(models.Model):
    class ItemType(models.TextChoices):
        DONATION = 'DN', _("Donation")
        LOAN = 'LN', _("Loan")
        REQUEST = 'RQ', _("Request")
        EVENT = 'EV', _("Event")

    class Categories(models.TextChoices):
        FOOD = 'FD', _("Food and Supplies")
        ANIMALS = 'AN', _("Pets and Animals")
        ENTERTAINMENT = 'EN', _("Arts, Culture, and Entertainments")
        COLLECTORS = 'CL', _("Collectibles and Decoratives")
        HELPING = 'HL', _("Helping hand and Manual Labor")
        ADMINIT = 'AT', _("Administrative tasks")
        DIY = 'DY', _("Do-it-Yourself")
        BEAUTY = 'BT', _("Beauty and Well-being")
        HEALTH = 'HE', _("Health")  # and hygiene
        ENERGY = "EY", _("Energy and Heating")
        CHILDHOOD = 'CH', _("Childhood")
        CLOTHES = 'CO', _("Clothes and Shoes")
        IT = 'IT', _("Multimedia Hardware")
        CS = 'CS', _("Informatics Software")
        GARDEN = 'GD', _("Gardening and Nature")
        HOUSE = 'HS', _("Living spaces and Housing")
        TOOLS = 'EQ', _("Tools and Equipments and Ustensils")
        HOLIDAYS = 'HD', _("Holidays, Week-end, Leisures")
        BOOK = 'BK', _("Books and Magazines")
        MEDIA = 'MD', _("CDs, DVDs, Blu-rays, Discs")
        SPORT = 'SP', _("Sports")
        TRANSPORT = 'TS', _("Transportation, Delivery, Pick-up, Moving")
        VEHICLE = 'VE', _("Vehicles and Means of transport")
        OTHER = 'OT', _("Other")

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    location = models.PointField(blank=True, geography=True, null=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    startdate = models.DateTimeField(default=timezone.now)
    enddate = models.DateTimeField(null=True)
    is_recurrent = models.BooleanField(default=False)

    type = models.CharField(max_length=2, choices=ItemType.choices, default=ItemType.REQUEST)

    category1 = models.CharField(max_length=2, choices=Categories.choices, default='OT')
    category2 = models.CharField(max_length=2, choices=Categories.choices, default="", blank=True)
    category3 = models.CharField(max_length=2, choices=Categories.choices, default="", blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name + " : " + self.description + " (" + self.category1 + ")"

    class Meta:
        ordering = ['-id']


def user_created(sender, user, request, **kwargs):
    for category in UserMapExtraCategories:
        UserMapExtraCategory.objects.create(user=user, category=category)

user_registered.connect(user_created)


class ItemImage(models.Model):
    image = models.ImageField(upload_to='items_images')
    position = models.IntegerField()
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.image.name = get_random_file_name()
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        MAX_SIZE = 1024
        if img.height > MAX_SIZE or img.width > MAX_SIZE:
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
        return "{}/api/v1/items/images/{}".format(settings.API_URL, self.pk)

    class Meta:
        ordering = ['item_id', 'position']


class ItemComment(models.Model):
    content = models.TextField(blank=True, default="")
    creationdate = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-creationdate']


class ItemView(models.Model):
    item = models.ForeignKey(Item, related_name='item_views', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='item_views', on_delete=models.SET_NULL, null=True)
    view_date = models.DateTimeField(default=timezone.now)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['item', 'user'], name='unique__mymap_itemview__item_user')
        ]


class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.SET_NULL, null=True)
    is_closed = models.BooleanField(default=False)
    lastmessagedate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-lastmessagedate']


class ConversationUser(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_link', on_delete=models.CASCADE)
    joining_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.SET_NULL, null=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['conversation_id', '-date']
