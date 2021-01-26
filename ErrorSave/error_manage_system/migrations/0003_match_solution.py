# Generated by Django 3.1.5 on 2021-01-22 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error_manage_system', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_code', models.TextField()),
                ('solution_description', models.TextField()),
                ('user_id', models.IntegerField()),
                ('error_id', models.IntegerField()),
            ],
        ),
    ]