# Generated by Django 5.2 on 2025-05-26 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_page_content_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='index',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='timestore',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
