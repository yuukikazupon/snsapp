# Generated by Django 3.1.2 on 2021-01-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0010_auto_20210117_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keijiban',
            name='goodman_list_field',
        ),
        migrations.AlterField(
            model_name='keijiban',
            name='goodtext',
            field=models.CharField(blank=True, default='👍', max_length=10000, null=True),
        ),
    ]
