# Generated by Django 3.1.1 on 2020-09-19 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200919_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='openorclosed',
            field=models.IntegerField(default=0),
        ),
    ]
