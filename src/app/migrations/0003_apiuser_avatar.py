# Generated by Django 3.1.7 on 2021-04-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200910_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]