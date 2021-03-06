# Generated by Django 3.2.7 on 2021-10-04 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('surname', models.CharField(blank=True, max_length=122)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=3000)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(max_length=3000)),
                ('slug', models.SlugField(max_length=250)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('hash', models.CharField(default=None, max_length=32, null=True)),
                ('txId', models.CharField(default=None, max_length=66, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='crew.relatedpost')),
            ],
            options={
                'verbose_name': 'post received',
                'verbose_name_plural': 'posts received',
            },
        ),
    ]
