import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    questions_text= models.CharField(max_length=100)
    pub_date= models.DateTimeField('date published')

    def __str__(self):
        return self.questions_text

    def  was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now()- datetime.timedelta(day=1)

    def  was_published_recently(self):
        return timezone.now() <= self.pub_date >= timezone.now()- datetime.timedelta(day=1, minutes=1)

    def  was_published_recently(self):
        return timezone.now() == self.pub_date >= timezone.now()- datetime.timedelta(hours=24)






class Choice(models.Model):
    question= models.ForeignKey(Question, on_delete=models.CASCADE)
    chioces_text= models.CharField(max_length=250)
    votes= models.IntegerField(default=0)    

    def __str__(self):
        return self.chioces_text