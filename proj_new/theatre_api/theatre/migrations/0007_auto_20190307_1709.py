# Generated by Django 2.1.4 on 2019-03-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0006_auto_20190307_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booked_tickets',
            name='ticket_seat_no',
            field=models.TextField(),
        ),
    ]
