# Generated by Django 3.2.5 on 2021-08-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentsAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual_monthly_tax', models.IntegerField(default=0)),
                ('salaries', models.IntegerField(default=0)),
            ],
        ),
    ]
