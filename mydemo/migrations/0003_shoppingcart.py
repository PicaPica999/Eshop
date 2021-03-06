# Generated by Django 3.2.9 on 2021-12-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mydemo', '0002_delete_shoppingcart'),
    ]

    operations = [
        migrations.CreateModel(
            name='shoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.CharField(default=None, max_length=1024, null=True, verbose_name='商品')),
                ('buyer', models.CharField(default=None, max_length=1024, null=True, verbose_name='买家')),
                ('price', models.IntegerField(default=None, null=True, verbose_name='价格')),
            ],
        ),
    ]
