# Generated by Django 3.2.13 on 2022-06-04 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pollster', '0003_auto_20220604_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pollster.choice'),
        ),
    ]
