# Generated by Django 3.2.3 on 2021-06-09 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myWEB', '0005_auto_20210609_0933'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teach',
            old_name='teacher',
            new_name='teacher_id',
        ),
    ]
