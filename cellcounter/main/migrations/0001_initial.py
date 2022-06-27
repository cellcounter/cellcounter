# -*- coding: utf-8 -*-

from django.db import models, migrations
from django.conf import settings
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CellImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("file", models.ImageField(upload_to=b"cell_images")),
                (
                    "thumbnail",
                    models.ImageField(
                        null=True, upload_to=b"cell_thumbnails", blank=True
                    ),
                ),
                ("thumbnail_left", models.IntegerField()),
                ("thumbnail_top", models.IntegerField()),
                ("thumbnail_width", models.IntegerField()),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="CellType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("readable_name", models.CharField(max_length=50)),
                ("machine_name", models.CharField(unique=True, max_length=50)),
                ("abbr_name", models.CharField(unique=True, max_length=10)),
                ("comment", models.TextField(blank=True)),
                ("visualisation_colour", colorful.fields.RGBColorField(blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="CopyrightHolder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("link_title", models.CharField(max_length=300, null=True, blank=True)),
                ("link_url", models.CharField(max_length=300, null=True, blank=True)),
                ("user", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("details", models.TextField()),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SimilarLookingGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("cell_image", models.ManyToManyField(to="main.CellImage")),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="cellimage",
            name="celltype",
            field=models.ForeignKey(to="main.CellType", on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="cellimage",
            name="copyright",
            field=models.ForeignKey(
                to="main.CopyrightHolder", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="cellimage",
            name="license",
            field=models.ForeignKey(to="main.License", on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="cellimage",
            name="uploader",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
    ]
