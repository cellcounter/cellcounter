#from django.apps import apps
from django.test import TransactionTestCase
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

from django.utils import timezone

from django.contrib.auth.models import User
from .factories import UserFactory, KeyboardFactory
from .serializers import KeyboardListItemSerializer
from .models import Keyboard

from django.db import models


class TestMigrations(TransactionTestCase):

    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)
        #self.migrate_from = [(self.app, self.migrate_from)]
        #self.migrate_to = [(self.app, self.migrate_to)]
        connection.prepare_database()
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor.loader.build_graph()
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class DefaultsTestCase(TestMigrations):

    migrate_from = [('cc_kapi', u'0001_initial')]
    migrate_to = [('cc_kapi', u'0002_v2api')]

    def setUpBeforeMigration(self, japps):
        # create users and keyboards under the old schema
        User = japps.get_model('auth', 'User')

        class KeyboardFactory2(KeyboardFactory):
            class Meta:
                model = japps.get_model('cc_kapi', 'Keyboard')

        user = User(username="test")
        user.save()
        self.user_id = user.id

        keyboard1 = KeyboardFactory2(user=user)
        keyboard1.is_primary = True
        keyboard1.save()
        self.keyboard1_id = keyboard1.id

        keyboard2 = KeyboardFactory2(user=user)
        keyboard2.save()
        self.keyboard2_id = keyboard2.id

        user1 = User(username="test2")
        user1.save()
        self.user1_id = user1.id

        keyboard3 = KeyboardFactory2(user=user1)
        keyboard3.save()
        self.keyboard3_id = keyboard3.id


    def test_defaults_migrated(self):
        # check that there are two users
        users = User.objects.all()
        self.assertEqual(len(users), 2)

        user = User.objects.get(id=self.user_id)
        user1 = User.objects.get(id=self.user1_id)

        # check that the three keyboards in the database exist
        kb1 = Keyboard.objects.get(id=self.keyboard1_id)
        kb2 = Keyboard.objects.get(id=self.keyboard2_id)
        kb3 = Keyboard.objects.get(id=self.keyboard3_id)

        # check that there are two keyboards for user and that the ids match
        keyboards = user.keyboard_set.all()
        self.assertEqual(len(keyboards), 2)
        kids = [k.id for k in keyboards]
        kids.sort()
        self.assertEqual(kids, [self.keyboard1_id, self.keyboard2_id])

        # check that there is one keyboard for user1 and that the id matches
        keyboards1 = user1.keyboard_set.all()
        self.assertEqual(len(keyboards1), 1)
        self.assertEqual(keyboards1[0].id, self.keyboard3_id)

        # check that there are five keyboards in total
        keyboards_all = Keyboard.objects.all()
        self.assertEqual(len(keyboards_all), 5)

        # check that kb is user's default desktop keyboard and there is no mobile default
        self.assertEqual(user.defaultkeyboards.desktop.id, kb1.id)
        self.assertEqual(user.defaultkeyboards.mobile, None)

        # check that user1 has no default desktop or mobile keyboard
        self.assertFalse(hasattr(user1, 'defaultkeyboards'))

