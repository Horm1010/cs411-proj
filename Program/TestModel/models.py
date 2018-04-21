from django.db import models

# Create your models here.

class Test_date(models.Model):
    date = models.CharField(primary_key=True, max_length = 20)



class Test_tweet(models.Model):
    id = models.CharField(primary_key=True, max_length = 20)
    date = models.ForeignKey(Test_date, on_delete=models.CASCADE)
    tweet = models.CharField(max_length = 140)


