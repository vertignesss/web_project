# Generated by Django 5.1.1 on 2025-01-19 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_browse', '0006_alter_historicaloffer_id_alter_offer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='cards',
        ),
        migrations.CreateModel(
            name='Keywords_On_Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card_browse.keyword')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card_browse.card')),
            ],
        ),
    ]
