# Generated by Django 5.1.7 on 2025-04-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=70)),
                ('lname', models.CharField(max_length=70)),
                ('addrs', models.CharField(max_length=190)),
                ('email', models.EmailField(max_length=254)),
                ('phno', models.CharField(max_length=12)),
                ('uname', models.CharField(max_length=90)),
                ('pswrd', models.CharField(max_length=29)),
            ],
        ),
    ]
