# Generated by Django 5.1.1 on 2025-01-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_browse', '0015_alter_card_oracle_text_alter_keyword_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
