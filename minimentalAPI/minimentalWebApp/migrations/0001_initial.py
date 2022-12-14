# Generated by Django 4.0.3 on 2022-04-14 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('givenName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('cellNumber', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('dateOfBirth', models.DateField()),
            ],
        ),
    ]
