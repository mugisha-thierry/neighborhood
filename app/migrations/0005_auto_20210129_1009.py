# Generated by Django 3.1.5 on 2021-01-29 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210129_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighbourhood_infrastructure',
            name='email',
            field=models.EmailField(blank=True, default='No emai provided', max_length=254),
        ),
        migrations.AlterField(
            model_name='neighbourhood_infrastructure',
            name='department_name',
            field=models.CharField(choices=[('emergence', 'emergence'), ('businesses', 'businesses')], max_length=300),
        ),
        migrations.AlterField(
            model_name='profile',
            name='my_neighborhood_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.neighbourhood'),
        ),
    ]