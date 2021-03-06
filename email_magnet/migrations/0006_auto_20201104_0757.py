# Generated by Django 3.1.2 on 2020-11-04 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_magnet', '0005_auto_20201104_0737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsearch',
            name='first_name',
            field=models.CharField(blank=True, help_text="The first name of employer at the company that you're targetting. It is recommended to fill in this field", max_length=30, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='last_name',
            field=models.CharField(blank=True, help_text="The last name of employer at the company that you're targetting. It is recommended to fill in this field", max_length=30, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='detailsearch',
            name='middle_name',
            field=models.CharField(blank=True, help_text="The middle name of employer at the company that you're targetting. You can leave it blank.", max_length=30, verbose_name='Middle name'),
        ),
    ]
