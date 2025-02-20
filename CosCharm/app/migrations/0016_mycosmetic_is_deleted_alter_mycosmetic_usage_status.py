# Generated by Django 5.1.4 on 2025-01-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycosmetic',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='削除済み'),
        ),
        migrations.AlterField(
            model_name='mycosmetic',
            name='usage_status',
            field=models.CharField(choices=[('not_used', '未使用'), ('in_use', '使用中'), ('used', '使用済み')], default='not_used', max_length=20, verbose_name='使用ステータス'),
        ),
    ]
