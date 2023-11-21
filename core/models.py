from django.db import models


class Cliente(models.Model):

    username = models.CharField("Username", max_length=50)
    password = models.CharField("Password", max_length=100)
    email = models.EmailField("E-mail")
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

