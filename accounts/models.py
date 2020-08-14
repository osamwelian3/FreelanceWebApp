from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import os
from writershub import settings
from .file_rename import cert_rename, cv_rename, id_rename, essay1_rename, essay2_rename


# Create your models here.
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        """
        Creates and saves a staff user with the given username, email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given username, email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # admin but not super user
    admin = models.BooleanField(default=False)  # super user
    user_type = models.CharField(max_length=255)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    # notice the absence of a "Password_field", that is built in.

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]  # email and password are required by default

    objects = UserManager()

    def get_full_name(self):
        # the user is identified by their username
        return self.username

    def get_short_name(self):
        # the user is identified by their username
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have specific permissions?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permission to view the app 'app_label'?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


def file_rename(instance, filename):
    file_id = ''
    file = ''
    if len(file) > 0:
        if file == 'essay_1':
            file = 'essay'
            file_id = '1'
        if file == 'essay_2':
            file = 'essay'
            file_id = '2'
        file = '/' + file + ''
    ext = filename.split('.')[-1]
    pid = WriterProfile.objects.all().count() + 1
    try:
        id = WriterProfile.objects.latest('created_at').id + 1
    except Exception:
        id = 1
    if WriterProfile.objects.filter(id=instance.id):
        p = WriterProfile.objects.get(id=instance.id)
        pimage = p.image.url
        pid = pimage.rsplit('_', 1)[1].rsplit('.', 1)[0]
        id = instance.id
    print(instance)
    filename = "%s_%s_%s %s.%s" % (instance.id, id, pid, file_id, ext)
    fullname = os.path.join(settings.MEDIA_ROOT + 'Accounts/Registration' + file + '', filename)
    print(fullname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return os.path.join('Accounts/Registration' + file + '', filename)


class WriterProfile(models.Model):
    # Personal Details
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name='Country')
    city = models.CharField(verbose_name='City', max_length=255, blank=True, null=True)
    zip = models.CharField(verbose_name='Zip/Postal code', max_length=6, blank=True, null=True)
    phone = models.CharField(verbose_name='Phone', max_length=13, blank=False, null=False)
    worked = models.BooleanField(verbose_name='Worked for other academic writing companies', blank=False, null=False)

    # Citations and Disciplines
    styles = models.CharField(max_length=255, blank=False, null=False)
    academic_disciplines = models.CharField(max_length=255, blank=False, null=False)

    # CV Details
    native_language = models.CharField(max_length=255, blank=False, null=False)
    ACADEMIC_LEVEL = (
        ('Associate in Arts', 'Associate in Arts'),
        ('Bachelor', 'bachelor'),
        ('Undergraduate', 'Undergraduate'),
        ('Master', 'Master'),
        ('Ph.D', 'Ph.D'),
    )
    academic_level = models.CharField(max_length=255, blank=False, null=False, choices=ACADEMIC_LEVEL)
    brief_cv = models.TextField(verbose_name='Your Brief CV', blank=False, null=False)
    detailed_cv = models.FileField(verbose_name='Upload your detailed CV', upload_to=cv_rename)

    # Certification & Government I.D/Passport
    government_id = models.FileField(verbose_name='Upload government ID/Passport', blank=False, null=False, upload_to=id_rename)
    certificate_title = models.CharField(verbose_name='Give your Certificate a Title', max_length=255, blank=False, null=False)
    certificate = models.ImageField(verbose_name='Upload your certificate in image format', blank=False, null=False, upload_to=cert_rename)

    # Sample Essays
    essay1_title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Title for sample essay one')
    essay_one = models.FileField(verbose_name='Upload Sample Essay one', blank=False, null=False, upload_to=essay1_rename)
    essay2_title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Title for sample essay two')
    essay_two = models.FileField(verbose_name='Upload Sample Essay two', blank=False, null=False, upload_to=essay2_rename)

    # Payment and Terms
    PAYMENT_METHODS = (
        ('Paypal', 'Paypal'),
        ('MPESA', 'MPESA')
    )
    payment_method = models.CharField(max_length=255, verbose_name='Preferred Payment Method', blank=False, null=True, choices=PAYMENT_METHODS)
    terms = models.BooleanField(verbose_name='Terms and Conditions', default=True)

    def __str__(self):
        try:
            return "Writer profile for " + self.user.username
        except ObjectDoesNotExist:
            return "Not yet created"

    def delete(self, using=None, keep_parents=False):
        self.detailed_cv.storage.delete(self.detailed_cv.name)
        self.certificate.storage.delete(self.certificate.name)
        self.essay_one.storage.delete(self.essay_one.name)
        self.essay_two.storage.delete(self.essay_two.name)
        super().delete()
