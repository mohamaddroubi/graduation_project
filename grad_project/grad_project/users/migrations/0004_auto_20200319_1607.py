# Generated by Django 2.2.10 on 2020-03-19 14:07

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200319_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_brands',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Zara', 'Zara'), ('Gap', 'Gap'), ("Levi Strauss & Co. (Levi's)", "Levi Strauss & Co. (Levi's)"), ('Mango', 'Mango'), ('Monsoon', 'Monsoon'), ('Pull & Bear', 'Pull & Bear'), ('Bershka', 'Bershka'), ('American Eagle (AE)', 'American Eagle (AE)'), ('Forever 21', 'Forever 21'), ('Stradivarious', 'Stradivarious'), ('Parfois', 'Parfois'), ('British Home Stores (BHS)', 'British Home Stores (BHS)'), ('United States Polo Assn.', 'United States Polo Assn.'), ('Adidas', 'Adidas'), ('Tommy Hilfiger', 'Tommy Hilfiger'), ('BOGGI', 'BOGGI'), ('HACKETT', 'HACKETT'), ('Massimo Dutti', 'Massimo Dutti'), ('Punt Roma', 'Punt Roma'), ('H&M', 'H&M'), ('Next', 'Next'), ('Nike', 'Nike')], max_length=248, null=True),
        ),
    ]
