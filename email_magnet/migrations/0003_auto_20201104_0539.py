# Generated by Django 3.1.2 on 2020-11-04 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_magnet', '0002_auto_20201104_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsearch',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='middle_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='possible_emails',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='valid_emails',
            field=models.TextField(blank=True),
        ),
    ]
