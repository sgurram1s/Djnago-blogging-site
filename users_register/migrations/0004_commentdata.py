# Generated by Django 4.2 on 2023-12-21 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users_register', '0003_remove_postdata_content_type_delete_contenttype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_register.postdata')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]