# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


CELLTYPES_INITIAL = [
    {"readable_name": "Neutrophils",
     "machine_name": "neutrophils",
     "abbr_name": "neut",
     "visualisation_colour": "#4f6228"},
    {"readable_name": "Metamyelocytes",
     "machine_name": "meta",
     "abbr_name": "meta",
     "visualisation_colour": "#77933c"
    },
    {"readable_name": "Myelocytes",
     "machine_name": "myelocytes",
     "abbr_name": "myelo",
     "visualisation_colour": "#c3d69b"
    },
    {"readable_name": "Promyelocytes",
     "machine_name": "promyelocytes",
     "abbr_name": "promyelo",
     "visualisation_colour": "#d7e4bd"
    },
    {"readable_name": "Blasts",
     "machine_name": "blasts",
     "abbr_name": "blast",
     "visualisation_colour": "#ebf1de"
    },
    {"readable_name": "Basophils",
     "machine_name": "basophils",
     "abbr_name": "baso",
     "visualisation_colour": "#8064a2"
    },
    {"readable_name": "Eosinophils",
     "machine_name": "eosinophils",
     "abbr_name": "eo",
     "visualisation_colour": "#f79546"
    },
    {"readable_name": "Erythroid",
     "machine_name": "erythroid",
     "abbr_name": "erythro",
     "visualisation_colour": "#ff0000"
    },
    {"readable_name": "Lymphocytes",
     "machine_name": "lymphocytes",
     "abbr_name": "lympho",
     "visualisation_colour": "#ffffff"
    },
    {"readable_name": "Monocytes",
     "machine_name": "monocytes",
     "abbr_name": "mono",
     "visualisation_colour": "#bfbfbf"
    },
    {"readable_name": "Plasma cells",
     "machine_name": "plasma_cells",
     "abbr_name": "plasma",
     "visualisation_colour": "#0000ff"
    },
    {"readable_name": "Other",
     "machine_name": "other",
     "abbr_name": "other",
     "visualisation_colour": "#f9ff00"
    },
    {"readable_name": "Lymphoblasts",
     "machine_name": "lymphoblasts",
     "abbr_name": "ly_blasts",
     "visualisation_colour": "#606060"
    }]


def initial_celltypes(apps, schema_editor):
    CellType = apps.get_model("main", "CellType")

    for cell_type in CELLTYPES_INITIAL:
        ct = CellType(readable_name=cell_type['readable_name'],
                      machine_name=cell_type['machine_name'],
                      abbr_name=cell_type['abbr_name'],
                      visualisation_colour=cell_type['visualisation_colour']).save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_celltypes),
    ]
