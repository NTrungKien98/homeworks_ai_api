# Generated by Django 4.1.3 on 2023-06-13 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_firebase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="language",
            field=models.IntegerField(
                choices=[(1, "English"), (2, "Tiếng Việt")], default=1
            ),
        ),
    ]
