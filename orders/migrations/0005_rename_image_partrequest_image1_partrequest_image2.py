# Generated by Django 5.1.6 on 2025-02-19 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_partrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partrequest',
            old_name='image',
            new_name='image1',
        ),
        migrations.AddField(
            model_name='partrequest',
            name='image2',
            field=models.ImageField(default=1, upload_to='part_images/'),
            preserve_default=False,
        ),
    ]
