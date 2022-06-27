import os
import sys

import psycopg2
from psycopg2.extras import DictCursor

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from cellcounter.cc_kapi.models import Keyboard, KeyMap
from cellcounter.main.models import CellType, CellImage, License, CopyrightHolder


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
                                                first_name=first_name, last_name=last_name)
            new_user.date_joined = date_joined
            new_user.is_staff = is_staff
            new_user.is_superuser = is_superuser
            new_user.save()

            dict_cur.execute('SELECT * FROM cc_kapi_keyboard WHERE user_id=%s' % user_id)
            user_keyboards = dict_cur.fetchall()

            for keyboard_tuple in user_keyboards:
                old_keyboard_id = keyboard_tuple['id']
                old_label = keyboard_tuple['label']
                is_default = keyboard_tuple['is_default']
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

                    new_keymap = KeyMap.objects.get_or_create(key=old_keymap_key, cellid=cell)[0]
                    new_maps.append(new_keymap)

                new_keyboard.set_keymaps(new_maps)

        # Save across all the CellImage related stuff
        dict_cur.execute('SELECT * FROM main_license')
        old_license_list = dict_cur.fetchall()

        for old_license_tuple in old_license_list:
            new_license = License.objects.create(title=old_license_tuple['title'], details=old_license_tuple['details'])

        dict_cur.execute('SELECT * FROM main_copyrightholder')
        old_copyrightholder_list = dict_cur.fetchall()

        for old_copyrightholder_tuple in old_copyrightholder_list:
            old_id = old_copyrightholder_tuple['id']
            dict_cur.execute('SELECT * FROM main_copyrightholder_user where copyrightholder_id=%s' % old_id)
            old_copyrightholder_user = dict_cur.fetchone()
            old_user_id = old_copyrightholder_user['user_id']
            dict_cur.execute('SELECT * FROM auth_user WHERE id=%s' % old_user_id)
            old_user = dict_cur.fetchone()
            old_username = old_user['username']
            new_user = User.objects.get(username=old_username)
            new_copyrightholder = CopyrightHolder.objects.create(name=old_copyrightholder_tuple['name'],
                                                                 link_title=old_copyrightholder_tuple['link_title'],
                                                                 link_url=old_copyrightholder_tuple['link_url'])
            new_copyrightholder.user.add(new_user)

        # Migrate over CellImages

        dict_cur.execute('SELECT * FROM main_cellimage')
        old_cellimage_list = dict_cur.fetchall()

        for old_cellimage_tuple in old_cellimage_list:
            old_title = old_cellimage_tuple['title']
            old_description = old_cellimage_tuple['description']
            old_file = old_cellimage_tuple['file']
            old_thumbnail = old_cellimage_tuple['thumbnail']
            old_celltype = old_cellimage_tuple['celltype_id']
            old_thumbnail_left = old_cellimage_tuple['thumbnail_left']
            old_thumbnail_top = old_cellimage_tuple['thumbnail_top']
            old_thumbnail_width = old_cellimage_tuple['thumbnail_width']
            old_uploader = old_cellimage_tuple['uploader_id']

            dict_cur.execute('SELECT * FROM auth_user WHERE id=%s' % old_uploader)
            old_uploader_username = dict_cur.fetchone()['username']

            old_copyright = old_cellimage_tuple['copyright_id']
            dict_cur.execute('SELECT * FROM main_copyrightholder WHERE id=%s' % old_copyright)
            old_copyrightholder_name = dict_cur.fetchone()['name']

            old_license = old_cellimage_tuple['license_id']
            dict_cur.execute('SELECT * FROM main_license WHERE id=%s' % old_license)
            old_license_title = dict_cur.fetchone()['title']

            # Get modern equivalents
            cell = CellType.objects.get(id=old_celltype)
            uploader = User.objects.get(username=old_uploader_username)
            copyright = CopyrightHolder.objects.get(name=old_copyrightholder_name)
            license = License.objects.get(title=old_license_title)

            # Generate new CellImage instance
            new_image = CellImage(title=old_title, description=old_description, celltype=cell,
                                  thumbnail_left=old_thumbnail_left, thumbnail_top=old_thumbnail_top,
                                  thumbnail_width=old_thumbnail_width, uploader=uploader,
                                  copyright=copyright, license=license)
            new_image.file.name = old_file
            new_image.thumbnail.name = old_thumbnail

            new_image.save()

        conn.close()
