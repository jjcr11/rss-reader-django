# Generated by Django 3.1.7 on 2021-03-19 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_post_page_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='page_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feed.page'),
        ),
    ]
