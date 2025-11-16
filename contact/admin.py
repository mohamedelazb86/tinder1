from django.contrib import admin

from .models import Competitor,Company_by,Category

admin.site.register(Company_by)
admin.site.register(Competitor)
admin.site.register(Category)

