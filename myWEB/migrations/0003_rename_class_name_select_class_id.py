# Generated by Django 3.2.3 on 2021-06-07 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myWEB', '0002_alter_class_class_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='select',
            old_name='class_name',
            new_name='class_id',
        ),
    ]
