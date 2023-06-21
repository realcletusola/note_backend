from django.contrib import admin

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title','user','date']
    list_display_links = ['title','user','date']


admin.site.register(Note,NoteAdmin)