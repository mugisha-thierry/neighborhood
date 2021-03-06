# Generated by Django 3.1.5 on 2021-01-28 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post',
            new_name='post_details',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='post_image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='post',
            name='neighbourhood',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='username',
        ),
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.profile'),
        ),
    ]
