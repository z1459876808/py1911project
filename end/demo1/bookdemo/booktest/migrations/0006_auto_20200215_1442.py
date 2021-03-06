# Generated by Django 3.0.3 on 2020-02-15 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0005_auto_20200215_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
                ('regist_name', models.DateField(auto_now_add=True, verbose_name='注册日期')),
            ],
        ),
        migrations.AlterField(
            model_name='hero',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heros', to='booktest.Book'),
        ),
        migrations.CreateModel(
            name='Concat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(default='1459876808@qq.com', max_length=254)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='con', to='booktest.Account')),
            ],
        ),
    ]
