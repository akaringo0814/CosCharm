# Generated by Django 5.1.4 on 2024-12-30 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_mymakecosmetic'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'following')},
        ),
    ]