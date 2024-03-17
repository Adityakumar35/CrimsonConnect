# Generated by Django 5.0.3 on 2024-03-16 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_delete_request'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('requested_blood', models.CharField(blank=True, max_length=3, null=True)),
                ('recipient_fname', models.CharField(max_length=15)),
                ('recipient_pincode', models.CharField(max_length=6)),
                ('recipient_age', models.IntegerField()),
                ('relation_with', models.CharField(max_length=10)),
                ('recipient_address', models.CharField(max_length=50)),
                ('recipient_state', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
