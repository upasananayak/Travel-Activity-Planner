# Generated by Django 5.1.4 on 2024-12-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_place_visited_delete_userplace"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]