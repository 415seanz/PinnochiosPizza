# Generated by Django 2.0.3 on 2018-12-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20181215_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='maxToppings',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]