# Generated by Django 3.1 on 2023-02-20 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('pnid', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(blank=True, default='vascular', max_length=50)),
                ('latname', models.CharField(blank=True, max_length=150)),
                ('authors', models.CharField(blank=True, max_length=150)),
                ('colnames', models.CharField(blank=True, max_length=150)),
                ('longname', models.CharField(blank=True, max_length=250)),
                ('note', models.TextField(blank=True)),
                ('caption', models.TextField(blank=True, default='')),
                ('excluded', models.BooleanField(default=False)),
                ('disabled', models.BooleanField(default=False, verbose_name='legacy only')),
                ('rank', models.CharField(blank=True, max_length=50, verbose_name='actual rank')),
                ('level', models.CharField(blank=True, max_length=50)),
                ('sal_latname', models.CharField(blank=True, max_length=150)),
                ('sal_authors', models.CharField(blank=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(blank=True, default='', max_length=10)),
                ('legacy_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legacy_upper', to='names.name')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='names.name')),
                ('upper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Fid_Gid', to='names.name')),
            ],
            options={
                'verbose_name_plural': 'NameRecords',
            },
        ),
        migrations.CreateModel(
            name='SpeciesMeta',
            fields=[
                ('spid', models.IntegerField(primary_key=True, serialize=False)),
                ('evergreen', models.CharField(blank=True, max_length=150)),
                ('introduced', models.CharField(blank=True, max_length=150, verbose_name='NonNative')),
                ('invasive_mipag', models.CharField(blank=True, max_length=150)),
                ('invasive', models.CharField(blank=True, default='', max_length=150)),
                ('origin', models.CharField(blank=True, max_length=150)),
                ('rare', models.CharField(blank=True, max_length=150)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('counties', models.CharField(blank=True, default='* * * * * * * * * * * * * *', max_length=150)),
                ('counties_changed_from', models.CharField(blank=True, max_length=150)),
                ('status', models.CharField(blank=True, max_length=150)),
                ('initial_name', models.CharField(blank=True, max_length=150)),
                ('rank', models.CharField(blank=True, default='species', max_length=150)),
                ('notes', models.TextField(blank=True, default='', null=True)),
                ('species', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='names.name')),
            ],
            options={
                'verbose_name_plural': 'SpeciesMeta',
            },
        ),
        migrations.CreateModel(
            name='NameAnnotation',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, max_length=520, null=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('cached', models.CharField(blank=True, help_text='saved filename', max_length=255, null=True)),
                ('kind', models.CharField(choices=[('', ''), ('note', 'note without photo'), ('photo', 'photo'), ('sample', 'to sample'), ('check', 'relocate')], max_length=50)),
                ('by', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='names.name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommonName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colname', models.CharField(blank=True, max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ref_name', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='names.name')),
            ],
            options={
                'unique_together': {('ref_name', 'colname')},
            },
        ),
    ]
