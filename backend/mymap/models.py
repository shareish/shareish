import json
import random
import secrets
import string
from datetime import date

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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


class MailNotificationFrequenciesOSM(models.TextChoices):
    DAILY = 'D', _("Daily")
    WEEKLY = 'W', _("Weekly")
    MONTHLY = 'M', _("Monthly")
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
    mastodon_url  = models.URLField(blank=True, default="")
    ref_location = models.PointField(blank=True, geography=True, null=True)
    use_ref_loc = models.BooleanField(default=False)
    mail_notif_generalinfo = models.BooleanField(default=True)
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
    mail_notif_freq_osm = models.CharField(
        max_length=1,
        choices=MailNotificationFrequenciesOSM.choices,
        default=MailNotificationFrequenciesOSM.WEEKLY
    )
    dwithin_notifications = models.PositiveSmallIntegerField(
        null=True,
        default=10,
        help_text="Enter maximum distance for new item and event notifications"
    )
    save_item_viewing = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)

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


def user_created(sender, user, request, **kwargs):
    for category in UserMapExtraCategories:
        UserMapExtraCategory.objects.create(user=user, category=category)

user_registered.connect(user_created)


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
        PUBLICRESOURCE = 'PR', _("Public Resource")
        OTHER = 'OT', _("Other")

    class Visibility(models.TextChoices):
        PUBLIC = 'PB', _("Public")
        UNLISTED = 'UL', _("Unlisted")
        DRAFT = 'DR', _("Draft")

    class ClosedReason(models.TextChoices):
        ON = 'ON', _("On Shareish")
        OUTSIDE = 'OUT', _("Outside Shareish")
        NOT = 'NOT', _("Not resolved")
        OTHER = 'OTH', _("Other")

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    location = models.PointField(blank=True, geography=True, null=True)
    use_coordinates = models.BooleanField(default=False)
    creationdate = models.DateTimeField(auto_now_add=True)
    startdate = models.DateTimeField(default=timezone.now)
    enddate = models.DateTimeField(null=True)
    is_recurrent = models.BooleanField(default=False)

    type = models.CharField(max_length=2, choices=ItemType.choices, default=ItemType.REQUEST)

    category1 = models.CharField(max_length=2, choices=Categories.choices, default=Categories.OTHER)
    category2 = models.CharField(max_length=2, choices=Categories.choices, default="", blank=True)
    category3 = models.CharField(max_length=2, choices=Categories.choices, default="", blank=True)

    visibility = models.CharField(max_length=2, choices=Visibility.choices, default=Visibility.PUBLIC)

    closed_reason = models.CharField(max_length=3, choices=ClosedReason.choices, default="", blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE)

    @property
    def is_closed(self):
        return self.closed_reason != ""

    def __str__(self) -> str:
        return self.name + " : " + self.description + " (" + self.category1 + ")"

    class Meta:
        ordering = ['-id']


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
    item = models.ForeignKey(Item, related_name='views', on_delete=models.CASCADE)
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
    closed_by = models.ForeignKey(User, related_name='closed_conversations', on_delete=models.SET_NULL, null=True)
    max_users = models.PositiveIntegerField(default=2)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['conversation_id', '-date']


class Token(models.Model):
    class TokenActions(models.TextChoices):
        RECOVER_ACCOUNT = 'recover_account'
        DELETE_ACCOUNT = 'delete_account'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    action = models.CharField(max_length=50, choices=TokenActions.choices)
    used_at = models.DateTimeField(null=True)
    lifespan = models.DurationField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def check_token(token, action = None):
        """
        Check if the token is still valid (exists, not used, not expired) for the said action
        """
        if isinstance(token, str):
            if (isinstance(action, str) or action == None):
                if len(token) == 40:
                    try:
                        token = Token.objects.get(token=token)
                        if token.action != action:
                            return {'error': 'TOKEN_ACTION_DOESNT_MATCH'}
                        if not token.is_used():
                            if not token.is_expired():
                                return {'success': token}
                            return {'error': 'TOKEN_EXPIRED'}
                        return {'error': 'TOKEN_ALREADY_USED'}
                    except Token.DoesNotExist:
                        return {'error': 'TOKEN_DOESNT_EXIST'}
                return {'error': 'TOKEN_LENGTH_INVALID'}
            return {'error': 'TOKEN_ACTION_BAD_FORMAT'}
        return {'error': 'TOKEN_BAD_FORMAT'}

    @staticmethod
    def get_or_create(user, action):
        """
        Create a new token if no token is already pending for the passed action, otherwise retrieve it, and return it
        """
        if action in Token.TokenActions.values:
            # Generate a token 54 chars long and trim it to 40
            # Trim is used as a security here, token_urlsafe(30) should generate a token 40 chars long but \
            # I can't confirm that, so I decided to take some margin
            generated_token = secrets.token_urlsafe(40)[:40]

            # Create a new entry if no rows matches user, action and is not used
            token, created = Token.objects.get_or_create(user=user, action=action, used_at=None, defaults={
                'token': generated_token
            })
            return token
        return False

    def is_expired(self):
        """
        Returns True if the token has expired, False otherwise.
        """
        if self.lifespan is None:
            return False

        expiration_time = self.created_at + self.lifespan
        return expiration_time <= timezone.now()

    def is_used(self):
        """
        Returns True if the token has been used, False otherwise.
        """
        return self.used_at is not None

    def use(self):
        """
        Use the current token if it is not already
        """
        if not self.is_used():
            self.used_at = timezone.now()
            self.save()


class ScheduledAccountDeletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    interval = models.DurationField()

    def due_date(self):
        """
        Returns True if the scheduled account deletion is due, False otherwise.
        """
        return self.request_date + self.interval

    def is_due(self):
        """
        Returns True if the scheduled account deletion is due, False otherwise.
        """
        return self.due_date() < timezone.now()
