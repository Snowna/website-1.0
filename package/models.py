from django.db import models


class Package(models.Model):
    tracking_num = models.CharField(max_length= 50)
    package_type = models.CharField(max_length=100)
    package_company = models.CharField(max_length=100)
    company_logo = models.CharField(max_length=1000)

    def __str__(self):
        return self.tracking_num + '-' + self.package_type