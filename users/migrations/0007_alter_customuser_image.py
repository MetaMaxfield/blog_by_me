# Generated by Django 4.2.1 on 2023-12-12 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(default='static/img/comment_icon.png', upload_to='users/', verbose_name='Изображение пользователя'),
        ),
    ]
