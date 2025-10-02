from django.conf import settings
from django.db import models




class NewsFotos(models.Model):
    title = models.CharField(max_length=500)
    image = models.URLField()


class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    count = models.IntegerField(default=0)
    images = models.ManyToManyField(NewsFotos, related_name="images")
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Serves(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title



class Region(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Organization(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


# Xodimlarning datalarini saqlash uchun yuqoridagi Course va Departments modellari Worker bog'langan
class ManagerOrganization(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username