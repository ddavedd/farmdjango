# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-07-01 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('color', models.CharField(default=b'grey', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_count', models.IntegerField()),
                ('discount', models.FloatField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('enabled', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.FloatField()),
                ('name', models.CharField(max_length=200)),
                ('tax_rate_nonedible', models.BooleanField()),
                ('enabled', models.BooleanField()),
                ('product_type', models.CharField(choices=[(b'SP', b'Set Price'), (b'WT', b'By Weight'), (b'PM', b'Premarked')], max_length=2)),
                ('color', models.CharField(default=b'grey', max_length=100)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.Product')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_product', models.BooleanField()),
                ('product_or_deal_id', models.IntegerField()),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('subtotal', models.FloatField()),
                ('edible_tax', models.FloatField()),
                ('nonedible_tax', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('cashier', models.CharField(max_length=100)),
                ('transaction_time', models.IntegerField()),
                ('location', models.CharField(default=b'stand', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='transactionitem',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.TransactionTotal'),
        ),
        migrations.AddField(
            model_name='deal',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm_register.Product'),
        ),
    ]
