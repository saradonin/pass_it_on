# Generated by Django 4.2.6 on 2023-10-19 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_alter_institution_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Instytucja', 'verbose_name_plural': 'Instytucje'},
        ),
    ]
