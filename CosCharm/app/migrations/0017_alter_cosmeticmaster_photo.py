# Generated by Django 5.1.4 on 2025-01-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_mycosmetic_is_deleted_alter_mycosmetic_usage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cosmeticmaster',
            name='photo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
