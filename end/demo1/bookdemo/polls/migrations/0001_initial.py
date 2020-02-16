# Generated by Django 3.0.3 on 2020-02-16 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20, verbose_name='投票内容')),
                ('count', models.FloatField(default=6, verbose_name='投票数量')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='polls.Article')),
            ],
        ),
    ]
