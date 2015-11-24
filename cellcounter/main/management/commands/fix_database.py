import os
import sys

from django.core.management.base import BaseCommand
import psycopg2
from psycopg2.extras import DictCursor

from django.contrib.auth.models import User
from cellcounter.cc_kapi.models import Keyboard, KeyMap
from cellcounter.main.models import CellType


class Command(BaseCommand):
    help = 'Fixes broken database migration'

    def handle(self, *args, **options):
        dbname = os.environ.get('OLD_DB_NAME', None)
        dbuser = os.environ.get('OLD_DB_USER', None)
        dbpwd = os.environ.get('OLD_DB_PWD', None)

        if any(a is None for a in [dbname, dbuser, dbpwd]):
            sys.exit("You have not supplied sufficient data for old database connection")

        connect_string = "dbname=%s user=%s password=%s host=localhost port=5432" % (dbname, dbuser, dbpwd)
        conn = psycopg2.connect(connect_string)
        dict_cur = conn.cursor(cursor_factory=DictCursor)

        # Get old users
        dict_cur.execute('SELECT * FROM auth_user;')
        old_user_list = dict_cur.fetchall()

        for user_tuple in old_user_list:
            user_id = user_tuple['id']
            username = user_tuple['username']
            password = user_tuple['password']
            first_name = user_tuple['first_name']
            last_name = user_tuple['last_name']
            email = user_tuple['email']
            date_joined = user_tuple['date_joined']
            is_staff = user_tuple['is_staff']
            is_superuser = user_tuple['is_superuser']

            new_user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name, date_joined=date_joined,
                                                is_staff=is_staff, is_superuser=is_superuser)

            dict_cur.execute('SELECT * FROM cc_kapi_keyboard WHERE user_id=%s' % user_id)
            user_keyboards = dict_cur.fetchall()

            for keyboard_tuple in user_keyboards:
                old_keyboard_id = keyboard_tuple['id']
                old_label = keyboard_tuple['label']
                is_primary = keyboard_tuple['is_primary']
                created = keyboard_tuple['created']

                new_keyboard = Keyboard.objects.create(user=new_user, label=old_label, is_primary=is_primary,
                                                       created=created)

                # Add new maps to keyboards
                dict_cur.execute('SELECT * FROM cc_kapi_keymap_keyboards WHERE keyboard_id=%s' % old_keyboard_id)
                old_maps_list = dict_cur.fetchall()

                new_maps = []

                for old_map_tuple in old_maps_list:
                    keymap_id = old_map_tuple['keymap_id']
                    dict_cur.execute('SELECT * FROM cc_kapi_keymap WHERE id=%s' % keymap_id)
                    old_keymap_tuple = dict_cur.fetchone()
                    old_keymap_key = old_keymap_tuple['key']
                    cell = CellType.objects.get(id=old_keymap_tuple['cellid_id'])

                    new_keymap = KeyMap.objects.get_or_create(key=old_keymap_key, cellid=cell)
                    new_maps.append(new_keymap)

                new_keyboard.set_keymaps(new_maps)

        conn.close()
