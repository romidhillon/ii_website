# Generated by Django 4.0 on 2022-11-27 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField()),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.client')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amey_position', models.CharField(max_length=100)),
                ('skillset', models.CharField(max_length=500)),
                ('cone_rate', models.FloatField()),
                ('image', models.ImageField(upload_to='')),
                ('cv', models.ImageField(upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('impact', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=50)),
                ('probability', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=50)),
                ('mitigation', models.CharField(max_length=500)),
                ('owner', models.CharField(choices=[('Romi Dhillon', 'Romi Dhillon'), ('Serena Haak', 'Serena Haak'), ('Tom Kinnear', 'Tom Kinnear'), ('Joe Collis', 'Joe Collis')], max_length=200)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], max_length=500)),
                ('date_opened', models.DateField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.project')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.resource')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('value', models.FloatField()),
                ('document', models.ImageField(upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('document', models.ImageField(upload_to='')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('hours', models.FloatField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.assignment')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.contract'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ii_app.position'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='resource', to='ii_app.resource'),
        ),
    ]
