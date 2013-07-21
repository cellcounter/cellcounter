import json
from django.db import models
from django.contrib.auth.models import User

from cellcounter.main.models import CellType


class KeyMap(models.Model):
    cellid = models.ForeignKey(CellType)
    key = models.CharField(max_length=1)


class CustomKeyboard(models.Model):
    """Represents a CustomKeyboard mapping between users and keys"""
    user = models.ForeignKey(User)
    label = models.CharField(max_length=25)
    is_primary = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    mappings = models.ManyToManyField(KeyMap)

    class Meta:
        unique_together = ('user', 'label')

    def __unicode__(self):
        return u"Keyboard %s for %s" %(self.label, self.user.username)

    def _sync_primary_flags(self):
        """Syncs all keyboard primary flags, setting the current to true,
        and all others to False"""
        for keyboard in self.user.customkeyboard_set.all():
            if keyboard == self:
                if not keyboard.is_primary:
                    keyboard.is_primary = True
                    keyboard.save()
            else:
                if keyboard.is_primary:
                    keyboard.is_primary = False
                    keyboard.save()

    def set_primary(self):
        self._sync_primary_flags()

    def get_mappings_json(self):
        """Returns JSON formatted dict of mappings"""
        return json.dumps(
            {mapping.key: {'cellid': mapping.cellid.id} for
             mapping in self.mappings.all()}
        )

    def delete(self):
        """Custom delete method, covering setting primary flags"""
        user = self.user
        primary = self.is_primary

        super(CustomKeyboard, self).delete()
        if primary:
            keyboards = user.customkeyboard_set.all()
            if keyboards:
                keyboards[0].set_primary()