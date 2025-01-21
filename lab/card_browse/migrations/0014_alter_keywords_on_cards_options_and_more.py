# Generated by Django 5.1.1 on 2025-01-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_browse', '0013_remove_user_cards'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keywords_on_cards',
            options={'verbose_name_plural': 'Keywords on Cards'},
        ),
        migrations.AlterField(
            model_name='card',
            name='oracle_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='oracle_text',
            field=models.TextField(),
        ),
    ]
