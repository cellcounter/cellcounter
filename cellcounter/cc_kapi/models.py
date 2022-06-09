from django.db import models
from django.contrib.auth.models import User

from cellcounter.main.models import CellType


class Keyboard(models.Model):
    """Represents a Keyboard mapping between users and keys"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=25)
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    mapping_type = models.CharField(max_length=25, default='desktop')

    def __unicode__(self):
        return "Keyboard %s for %s" %(self.label, self.user.username)

    def _sync_primary_flags(self):
        """Syncs all keyboard primary flags, setting the current to true,
        and all others to False"""
        for keyboard in self.user.keyboard_set.all():
            if keyboard == self:
                if not keyboard.default:
                    keyboard.default = True
                    keyboard.save()
            else:
                if keyboard.default:
                    keyboard.default = False
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
        primary = self.default

        super(Keyboard, self).delete()
        if primary:
            keyboards = user.keyboard_set.all()
            if keyboards:
                keyboards[0].set_primary()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Keyboard, self).save(force_insert=False, force_update=False, using=None,
                                   update_fields=None)
        if self.default:
            self.set_primary()


class KeyMap(models.Model):
    cellid = models.ForeignKey(CellType, on_delete=models.CASCADE)
    key = models.CharField(max_length=1)
    keyboards = models.ManyToManyField(Keyboard, related_name='mappings')
