from django.db import models
from django.contrib.auth.models import User

from cellcounter.main.models import CellType


class Keyboard(models.Model):
    """Represents a Keyboard mapping between users and keys"""
    user = models.ForeignKey(User)
    label = models.CharField(max_length=25)
    is_primary = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"Keyboard %s for %s" %(self.label, self.user.username)

    def _sync_primary_flags(self):
        """Syncs all keyboard primary flags, setting the current to true,
        and all others to False"""
        for keyboard in self.user.keyboard_set.all():
            if keyboard == self:
                if not keyboard.is_primary:
                    keyboard.is_primary = True
                    keyboard.save()
            else:
                if keyboard.is_primary:
                    keyboard.is_primary = False
                    keyboard.save()

    def _sync_keymaps(self, new_mapping_list):
        """Expects a list of KeyMap objects"""
        current_mappings = self.mappings.all()
        new_mappings = new_mapping_list

        [self.mappings.remove(x) for x in current_mappings if x not in new_mappings]
        [self.mappings.add(x) for x in new_mappings if x not in current_mappings]

    def set_keymaps(self, new_mapping_list):
        """new_mapping_list is a list of KeyMap objects"""
        self._sync_keymaps(new_mapping_list)

    def set_primary(self):
        self._sync_primary_flags()

    def delete(self):
        """Custom delete method, covering setting primary flags"""
        user = self.user
        primary = self.is_primary

        super(Keyboard, self).delete()
        if primary:
            keyboards = user.keyboard_set.all()
            if keyboards:
                keyboards[0].set_primary()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Keyboard, self).save(force_insert=False, force_update=False, using=None,
                                   update_fields=None)
        if self.is_primary:
            self.set_primary()


class KeyMap(models.Model):
    cellid = models.ForeignKey(CellType)
    key = models.CharField(max_length=1)
    keyboards = models.ManyToManyField(Keyboard, related_name='mappings')