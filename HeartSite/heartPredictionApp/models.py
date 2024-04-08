from django.db import models

class HeartData(models.Model):
    Age = models.IntegerField()
    Sex = models.CharField(max_length=1)
    ChestPainType = models.CharField(max_length=3)
    RestingBP = models.IntegerField()
    Cholesterol = models.IntegerField()
    FastingBS = models.IntegerField()
    RestingECG = models.CharField(max_length=10)
    MaxHR = models.IntegerField()
    ExerciseAngina = models.CharField(max_length=1)
    Oldpeak = models.DecimalField(max_digits=3, decimal_places=2)
    ST_Slope = models.CharField(max_length=4)
    HeartDisease = models.IntegerField()

