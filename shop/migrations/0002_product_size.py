# Generated by Django 5.1.2 on 2024-10-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.IntegerField(default=0, verbose_name='Product Size'),
        ),
    ]
