# Generated by Django 5.0.6 on 2024-11-12 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='exit', unique=True),
            preserve_default=False,
        ),
    ]
