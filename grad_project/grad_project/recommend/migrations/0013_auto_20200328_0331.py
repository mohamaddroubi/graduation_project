# Generated by Django 2.2.11 on 2020-03-28 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0012_auto_20200321_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='brand',
            field=models.CharField(choices=[('Zara', 'Zara'), ('Gap', 'Gap'), ("Levi Strauss & Co. (Levi's)", "Levi Strauss & Co. (Levi's)"), ('Mango', 'Mango'), ('Monsoon', 'Monsoon'), ('Pull & Bear', 'Pull & Bear'), ('Bershka', 'Bershka'), ('American Eagle (AE)', 'American Eagle (AE)'), ('Forever 21', 'Forever 21'), ('Stradivarious', 'Stradivarious'), ('Parfois', 'Parfois'), ('British Home Stores (BHS)', 'British Home Stores (BHS)'), ('United States Polo Assn.', 'United States Polo Assn.'), ('Adidas', 'Adidas'), ('Tommy Hilfiger', 'Tommy Hilfiger'), ('BOGGI', 'BOGGI'), ('HACKETT', 'HACKETT'), ('Massimo Dutti', 'Massimo Dutti'), ('Punt Roma', 'Punt Roma'), ('H&M', 'H&M'), ('next', 'Next'), ('Nike', 'Nike')], max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Top', 'Top'), ('Bottom', 'Bottom'), ('FullBody', 'Full Body'), ('Shoes', 'Shoes')], max_length=100),
        ),
    ]
