# Generated by Django 5.0.6 on 2024-06-11 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_products_table_alter_users_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='telegram_id',
            field=models.PositiveBigIntegerField(unique=True, verbose_name='Telegram ID'),
        ),
    ]
