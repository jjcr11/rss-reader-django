# Generated by Django 3.1.7 on 2021-03-19 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='page_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='feed.page'),
        ),
    ]
