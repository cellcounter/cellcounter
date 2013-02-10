from django.contrib import admin
from models import CellImage, CellType, SimilarLookingGroup, License, CopyrightHolder

class CellImageAdmin(admin.ModelAdmin):
    pass


class SimilarLookingGroupAdmin(admin.ModelAdmin):
    pass


class CellTypeAdmin(admin.ModelAdmin):
    pass 

class LicenseAdmin(admin.ModelAdmin):
    pass 

class CopyrightHolderAdmin(admin.ModelAdmin):
    pass 

admin.site.register(CellImage, CellImageAdmin)
admin.site.register(CellType, CellTypeAdmin)
admin.site.register(SimilarLookingGroup, SimilarLookingGroupAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(CopyrightHolder, CopyrightHolderAdmin)
