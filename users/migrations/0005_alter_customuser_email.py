# Generated by Django 4.2.1 on 2023-11-02 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_description_en_customuser_description_ru'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
    ]
