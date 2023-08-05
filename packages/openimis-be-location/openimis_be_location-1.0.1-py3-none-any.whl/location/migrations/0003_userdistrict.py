# Generated by Django 2.1.11 on 2019-10-02 19:40

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDistrict',
            fields=[
                ('id', models.AutoField(db_column='UserDistrictID', primary_key=True, serialize=False)),
                ('legacy_id', models.IntegerField(blank=True, db_column='LegacyID', null=True)),
                ('validity_from', core.fields.DateTimeField(db_column='ValidityFrom')),
                ('validity_to', core.fields.DateTimeField(blank=True, db_column='ValidityTo', null=True)),
                ('audit_user_id', models.IntegerField(db_column='AuditUserID')),
            ],
            options={
                'db_table': 'tblUsersDistricts',
                'managed': False,
            },
        ),
    ]
