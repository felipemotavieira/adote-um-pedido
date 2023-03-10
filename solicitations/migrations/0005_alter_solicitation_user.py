# Generated by Django 4.1.5 on 2023-01-07 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("solicitations", "0004_alter_solicitation_donee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solicitation",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="solicitations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
