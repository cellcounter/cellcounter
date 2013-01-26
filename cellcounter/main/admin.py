from django.contrib import admin
from models import CellImage, SimilarLookingGroup

print "ADMIN"

class CellImageAdmin(admin.ModelAdmin):
    pass


class SimilarLookingGroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(CellImage, CellImageAdmin)
admin.site.register(SimilarLookingGroup, SimilarLookingGroupAdmin)
