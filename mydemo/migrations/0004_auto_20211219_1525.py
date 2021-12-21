# Generated by Django 3.2.9 on 2021-12-19 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mydemo', '0003_shoppingcart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='goods',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='good_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mydemo.goods'),
        ),
    ]
