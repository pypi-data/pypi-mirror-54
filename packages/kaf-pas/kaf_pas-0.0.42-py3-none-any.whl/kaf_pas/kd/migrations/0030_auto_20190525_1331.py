# Generated by Django 2.2.1 on 2019-05-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kd', '0029_auto_20190525_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document_attrs',
            name='value_str',
            field=models.TextField(db_index=True, default=None, verbose_name='Значение атрибута'),
        ),
    ]
