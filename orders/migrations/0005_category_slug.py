# Generated by Django 2.0.3 on 2019-01-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_item_maxtoppings'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='slug', max_length=32),
            preserve_default=False,
        ),
    ]
