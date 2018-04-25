from django.contrib.auth.models import Permission, User
from django.db import models


class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tracking_num = models.CharField(max_length=50)
    package_type = models.CharField(max_length=100)
    staff_company = models.CharField(max_length=50, default='')
    staff_price = models.CharField(max_length=100, default='')
    package_company = models.CharField(max_length=100)

    def __str__(self):
        return self.tracking_num + '-' + self.package_type
