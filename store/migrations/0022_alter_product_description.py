# Generated by Django 4.1.7 on 2023-03-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
    ]