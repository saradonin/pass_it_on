# Generated by Django 4.2.6 on 2023-10-30 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0010_alter_donation_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.CharField(choices=[('2', 'organizacja pozarządowa'), ('1', 'fundacja'), ('3', 'zbiórka lokalna')], default=1, max_length=64),
        ),
    ]
