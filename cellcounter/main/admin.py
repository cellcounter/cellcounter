from django.contrib import admin
from models import CellImage, CellType, SimilarLookingGroup

print "ADMIN"

class CellImageAdmin(admin.ModelAdmin):
    pass


class SimilarLookingGroupAdmin(admin.ModelAdmin):
    pass


class CellTypeAdmin(admin.ModelAdmin):
    pass 

admin.site.register(CellImage, CellImageAdmin)
admin.site.register(CellType, CellTypeAdmin)
admin.site.register(SimilarLookingGroup, SimilarLookingGroupAdmin)
