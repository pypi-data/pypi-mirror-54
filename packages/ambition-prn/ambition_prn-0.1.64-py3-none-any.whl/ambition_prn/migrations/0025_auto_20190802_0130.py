# Generated by Django 2.2.2 on 2019-08-01 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0024_auto_20190628_2236")]

    operations = [
        migrations.RenameField(
            model_name="deathreport",
            old_name="cause_of_death",
            new_name="cause_of_death_old",
        ),
        migrations.RenameField(
            model_name="historicaldeathreport",
            old_name="cause_of_death",
            new_name="cause_of_death_old",
        ),
    ]
