# Generated by Django 2.0.3 on 2018-04-20 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_date',
            fields=[
                ('date', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Test_tweet',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tweet', models.CharField(max_length=140)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestModel.Test_date')),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]