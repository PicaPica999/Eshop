# Generated by Django 3.2.9 on 2021-12-19 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydemo', '0009_auto_20211219_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='uid',
            field=models.CharField(max_length=128, null=True, verbose_name='订单编号'),
        ),
    ]
