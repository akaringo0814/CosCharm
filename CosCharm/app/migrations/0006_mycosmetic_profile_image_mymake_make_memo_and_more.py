# Generated by Django 5.1.1 on 2024-12-08 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_user_following_user_age_user_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycosmetic',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/default.jpg', null=True, upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='mymake',
            name='make_memo',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='personal_color',
            field=models.CharField(blank=True, choices=[('イエベ春', 'イエベ春'), ('ブルベ夏', 'ブルベ夏'), ('イエベ秋', 'イエベ秋'), ('ブルベ冬', 'ブルベ冬'), ('不明', '不明')], max_length=10, null=True, verbose_name='パーソナルカラー'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='profiles/default.jpg', null=True, upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='skin_type',
            field=models.CharField(blank=True, choices=[('乾燥肌', '乾燥肌'), ('脂性肌', '脂性肌'), ('普通肌', '普通肌'), ('混合肌', '混合肌'), ('不明', '不明')], max_length=10, null=True, verbose_name='肌質'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
