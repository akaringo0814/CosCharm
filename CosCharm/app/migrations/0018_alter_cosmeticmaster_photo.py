# Generated by Django 5.1.4 on 2025-01-18 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_cosmeticmaster_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cosmeticmaster',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='cosmetics/', verbose_name='画像'),
        ),
    ]
