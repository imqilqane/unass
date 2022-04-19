from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db.models.signals import post_save
from PIL import Image

class UserManager(UserManager):
    def create_user(self, username, email, password=None):
        print("model password ", password)
        if not username:
            raise ValueError('user has to have a username!')
        if not email:
            raise ValueError('user has to have an email')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=25, unique=True, verbose_name="username")
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="email address")
    first_name = models.CharField(
        max_length=25, verbose_name="first name", blank=False, null=False)
    last_name = models.CharField(
        max_length=25, verbose_name="last name", blank=False, null=False)
    is_director_national = models.BooleanField(default=False, verbose_name="directeur national")
    is_staff = models.BooleanField(default=False, verbose_name="directeur")
    is_active = models.BooleanField(default=True, verbose_name="formateur")
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def has_perm(self, perm):
        return True

    def __str__(self) :
        try:
            return f'{self.first_name} {self.last_name}'
        except:
            return f'{self.username}'
    

class user_profile (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default='images.png' , upload_to='profile_pics' , verbose_name='profile image')

    def save (self , *args , **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300 :
            output_size = (300 , 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) :
        return '{} profile.'.format(self.user.username)

        
def create_profile (sender , **kwarg) :
    if kwarg['created'] :
      user_profile.objects.create(user=kwarg['instance'])
post_save.connect(create_profile ,sender=User)