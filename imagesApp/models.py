from django.db import models

class MyModel(models.Model):
    image = models.ImageField(upload_to='images/origin/')

class Stylized(models.Model):
    original = models.ForeignKey(MyModel,on_delete=models.CASCADE)
    styled_image = models.ImageField(upload_to='images/styled/')

