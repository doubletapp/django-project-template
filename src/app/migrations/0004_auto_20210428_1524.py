# Generated by Django 3.1.7 on 2021-04-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_apiuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]