# Generated by Django 5.1.7 on 2025-04-21 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_alter_jobvacancy_last_date_to_apply_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='addrs',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='highest_qualification',
            field=models.CharField(max_length=50),
        ),
    ]
