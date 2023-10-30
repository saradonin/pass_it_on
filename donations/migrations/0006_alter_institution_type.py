# Generated by Django 4.2.6 on 2023-10-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_alter_donation_pick_up_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[(3, 'zbiórka lokalna'), (1, 'fundacja'), (2, 'organizacja pozarządowa')], default=1, max_length=64),
        ),
    ]