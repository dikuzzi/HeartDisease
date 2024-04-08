# Generated by Django 5.0.3 on 2024-04-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeartData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Age', models.IntegerField()),
                ('Sex', models.CharField(max_length=1)),
                ('ChestPainType', models.CharField(max_length=3)),
                ('RestingBP', models.IntegerField()),
                ('Cholesterol', models.IntegerField()),
                ('FastingBS', models.IntegerField()),
                ('RestingECG', models.CharField(max_length=10)),
                ('MaxHR', models.IntegerField()),
                ('ExerciseAngina', models.CharField(max_length=1)),
                ('Oldpeak', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ST_Slope', models.CharField(max_length=4)),
                ('HeartDisease', models.IntegerField()),
            ],
        ),
    ]