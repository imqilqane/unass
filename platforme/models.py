from django.db import models
from user.models import User
import datetime


class Deplomat(models.Model):
    formation = models.ForeignKey("Formation", related_name="deplomat" , on_delete=models.CASCADE)
    student_name = models.CharField(max_length=255)
    cin = models.CharField(max_length=25, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birthPlace = models.CharField(max_length=255, null=True, blank=True)
    birthPlace = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=14, null=True, blank=True)
    formationPlace = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    year_num = models.IntegerField(
        blank=True, null=True, verbose_name="order in this year")
    serial_num = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        ordering = ["date", "year_num"]

    def __str__(self) -> str:
        return self.student_name

    def save(self, *args, **kwargs):
        query = Deplomat.objects.all()
        last = None
        if query:
            index = query.count()
            last = query[index-1]
            if last.year_num > 0:
                self.year_num = last.year_num + 1
        else:
            self.year_num = 1
        self.serial_num = f"{datetime.datetime.now().year} - {self.year_num} - MA (CO) " if self.formation.convention else f"{datetime.datetime.now().year} - {self.year_num} - MA"
        return super(Deplomat, self).save(*args, **kwargs)


class Formation(models.Model):
    president = models.ForeignKey(
        User, verbose_name="présidente", related_name="présidente", on_delete=models.CASCADE, blank=True, null=True)
    fromDate = models.DateField(null=True, blank=True)
    toDate = models.DateField(null=True, blank=True)
    teacher = models.ForeignKey(
        User, verbose_name="formature", related_name="formature", on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    refused = models.BooleanField(default=False)
    cert_dir =  models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    antenne = models.ForeignKey("AnetmentUnass", blank=True, null=True, on_delete=models.SET_NULL)
    convention = models.BooleanField(default=False)

    

    def __str__(self) -> str:
        return f"{self.created_at}"

class Activite(models.Model):
    activite = models.CharField(max_length=200)

    def __str__(self):
        return self.activite[:50]

    class Meta:
        verbose_name_plural = "ACTIVITÉS UNASS"


class UnassActivite(models.Model):
    text = models.TextField()
    activites = models.ManyToManyField(Activite)
    image_n1 = models.ImageField(upload_to="Why_shoose_us", null = True, blank = True)
    image_n2 = models.ImageField(upload_to="Why_shoose_us", null = True, blank = True)
    image_n3 = models.ImageField(upload_to="Why_shoose_us", null = True, blank = True)
    

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name_plural = "ACTIVITÉ"

class CaralogueFormation(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name_plural = "Caralogue Des Formation"

class AnetmentUnass(models.Model):
    text = models.TextField()
    link = models.CharField(max_length = 300)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Anetment Unass"

class ChooseUsReasons(models.Model):
    reason = models.CharField(max_length=200)

    def __str__(self):
        return self.reason[:50]

    class Meta:
        verbose_name_plural = "ChooseUsReasons"


class WhyChoosingUs(models.Model):
    text = models.TextField()
    reasons = models.ManyToManyField(ChooseUsReasons)
    image_n1 = models.ImageField(upload_to="Why_shoose_us")
    

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name_plural = "WhyChoosingUs"


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)
    image = models.ImageField(upload_to="team")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "TeamMember"

class MessagesFromNewClients(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "MessagesFromNewClients"


class OurContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=40)

    def __str__(self):
        return self.phone
