# Generated by Django 4.1.4 on 2023-09-25 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0010_alter_associationmembershippayment_have_fine_and_more'),
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advocate',
            name='age',
        ),
        migrations.AddField(
            model_name='advocate',
            name='date_of_birth',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='advocate',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdata',
            name='otp',
            field=models.IntegerField(default='725892'),
        ),
        migrations.AlterField(
            model_name='advocate',
            name='document_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='advocate',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='advocate',
            name='type_of_user',
            field=models.CharField(choices=[('normal_advocate', 'Normal Advocate'), ('normal_admin', 'Normal Admin'), ('super_admin', 'Super Admin')], default='normal_advocate', max_length=255),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Registrar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(default='2000-01-01')),
                ('phone', models.CharField(max_length=200)),
                ('address', models.CharField(default='not given', max_length=200)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.court')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]