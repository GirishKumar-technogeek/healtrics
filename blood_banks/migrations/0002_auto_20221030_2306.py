# Generated by Django 3.2 on 2022-10-30 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_banks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodcampenrollment',
            name='blood_group_collected',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bloodcampenrollment',
            name='camp_enrollment_status',
            field=models.CharField(choices=[('Enrolled', 'Enrolled'), ('Donated', 'Donated')], default='Enrolled', max_length=100),
        ),
        migrations.AlterField(
            model_name='bloodcampenrollment',
            name='collected_quantity_in_cc',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bloodcampenrollment',
            name='donation_date_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='bloodcampenrollment',
            name='transaction_id',
            field=models.TextField(null=True),
        ),
    ]
