# Generated by Django 5.0.3 on 2024-03-15 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_request_requested_blood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='requested_blood',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]