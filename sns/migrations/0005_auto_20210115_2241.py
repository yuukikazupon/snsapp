# Generated by Django 3.1.2 on 2021-01-15 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0004_auto_20210115_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keijiban',
            name='goodtext',
            field=models.TextField(blank=True, default='a', max_length=10000, null=True),
        ),
    ]