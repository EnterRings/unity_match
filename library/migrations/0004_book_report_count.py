# Generated by Django 5.0.1 on 2024-02-05 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_is_reported_book_report_level_book_reported_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='report_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
