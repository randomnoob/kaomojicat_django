# Generated by Django 5.0.3 on 2024-04-02 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_ui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kaomojicategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main_ui.kaomojicategory'),
        ),
    ]
