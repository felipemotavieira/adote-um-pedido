# Generated by Django 4.1.5 on 2023-01-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="cpf",
            field=models.CharField(default=None, max_length=11, unique=True),
            preserve_default=False,
        ),
    ]
