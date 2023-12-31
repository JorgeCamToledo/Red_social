# Generated by Django 4.2.6 on 2023-10-13 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('timestap', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(db_column='fk_post', on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(db_column='fk_user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Comments',
            },
        ),
    ]
