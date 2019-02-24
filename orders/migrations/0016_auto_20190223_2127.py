# Generated by Django 2.0.13 on 2019-02-23 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20190223_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]