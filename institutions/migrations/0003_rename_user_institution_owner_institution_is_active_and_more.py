# Generated by Django 4.1.5 on 2023-01-04 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0001_initial"),
        ("institutions", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="institution",
            old_name="user",
            new_name="owner",
        ),
        migrations.AddField(
            model_name="institution",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="address",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="institution",
                to="addresses.address",
            ),
        ),
    ]