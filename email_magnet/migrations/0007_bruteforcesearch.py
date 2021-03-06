# Generated by Django 3.1.2 on 2020-11-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_magnet', '0006_auto_20201104_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='BruteForceSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(help_text="The domain name of the company that you're targetting. *This is a required field.", max_length=40, verbose_name='Domain name')),
                ('possible_emails', models.TextField(null=True)),
                ('employers_names', models.TextField(null=True)),
            ],
        ),
    ]
