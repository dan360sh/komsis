# Generated by Django 4.0.5 on 2022-06-01 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0033_account_contract_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountstatus',
            name='previous_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.accountstatus', verbose_name='Предыдущий статус'),
        ),
    ]