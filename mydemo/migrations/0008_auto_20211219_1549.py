# Generated by Django 3.2.9 on 2021-12-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydemo', '0007_alter_shoppingcart_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='seller',
            field=models.CharField(default=None, max_length=1024, null=True, verbose_name='卖家'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='buyer',
            field=models.CharField(default=None, max_length=1024, null=True, verbose_name='买家'),
        ),
    ]
