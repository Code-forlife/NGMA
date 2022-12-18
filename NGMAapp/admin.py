from django.contrib import admin
from .models import VisiterForm, ArtistForms, Employees,VisitorDetails, ArtistDetails,Transaction, ReviewSection

# Register your models here.

admin.site.register(VisiterForm)
admin.site.register(ArtistForms)
admin.site.register(Employees)
admin.site.register(VisitorDetails)
admin.site.register(ArtistDetails)
admin.site.register(Transaction)
admin.site.register(ReviewSection)