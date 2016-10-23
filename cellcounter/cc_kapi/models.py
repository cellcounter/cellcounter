from django.db import models
from django.contrib.auth.models import User

from cellcounter.main.models import CellType

from django.utils import timezone

class Keyboard(models.Model):
    """Represents a Keyboard mapping between users and keys"""

    DESKTOP = 1
    MOBILE = 2
    
    DEVICE_TYPES = (
                    (DESKTOP, 'desktop'),
                    (MOBILE, 'mobile'),
                   )


    user = models.ForeignKey(User, null=True)
    label = models.CharField(max_length=25)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPES,
                                  default=DESKTOP)

    _is_default = False

    def _set_default(self):
        self._is_default = True

    @property
    def is_default(self):
        return self._is_default

    @is_default.setter
    def is_default(self, value):
        self._set_default()
        to_set = self
        if not self.user:
            to_set = None
        if self.device_type == self.DESKTOP:
            self.user.defaultkeyboards.desktop = to_set
        elif self.device_type == self.MOBILE:
            self.user.defaultkeyboards.mobile = to_set

    def __unicode__(self):
        if self.user is None:
            return u"Builtin Keyboard '%s'" %(self.label)
        else:
            return u"Keyboard '%s' for user '%s'" %(self.label, self.user.username)

    def _sync_keymaps(self, new_mapping_list):
        """Expects a list of KeyMap objects"""
        current_mappings = self.mappings.all()
        new_mappings = new_mapping_list

        [self.mappings.remove(x) for x in current_mappings if x not in new_mappings]
        [self.mappings.add(x) for x in new_mappings if x not in current_mappings]

    def set_keymaps(self, new_mapping_list):
        """new_mapping_list is a list of KeyMap objects"""
        self._sync_keymaps(new_mapping_list)

    def delete(self):
        """Custom delete method, covering setting default flags"""
        # FIXME: get the DefaultKeyboards to delete the default
        user = self.user

        super(Keyboard, self).delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # FIXME: get the DefaultKeyboards to set the default

        if self.user:
            self.last_modified = timezone.now()

        super(Keyboard, self).save(force_insert=False, force_update=False, using=None,
                                   update_fields=None)

class KeyMap(models.Model):
    cellid = models.ForeignKey(CellType, on_delete=models.CASCADE)
    key = models.CharField(max_length=1)
    keyboards = models.ManyToManyField(Keyboard, related_name='mappings')

class DefaultKeyboards(models.Model):
    """Maps the default keyboard settings (desktop and mobile) to the user"""

    user = models.OneToOneField(User, primary_key=True)
    desktop = models.ForeignKey(Keyboard, default=None, related_name="desktop_default", null=True)
    mobile = models.ForeignKey(Keyboard, default=None, related_name="mobile_default", null=True)

    def __str__(self):              # __unicode__ on Python 2
        return "%s default keyboard mappings" % self.user.username

