# Generated by Django 4.1.4 on 2023-06-02 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookings",
            name="service_type",
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
