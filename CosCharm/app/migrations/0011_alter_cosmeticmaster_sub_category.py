# Generated by Django 5.1.4 on 2024-12-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_mycosmetic_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cosmeticmaster',
            name='sub_category',
            field=models.IntegerField(choices=[(0, '化粧水'), (1, '乳液'), (2, '美容液'), (3, 'アイブロウ'), (4, 'アイライナー'), (5, 'アイシャドウ'), (6, 'マスカラ'), (7, 'チーク'), (8, 'リップ'), (9, '下地'), (10, 'ファンデーション'), (11, 'フェイスパウダー')], default=0, verbose_name='サブカテゴリ'),
        ),
    ]
