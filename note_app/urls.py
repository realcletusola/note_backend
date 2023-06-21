from django.urls import path 

from .views import NoteList, NoteDetail


urlpatterns = [
    path('', NoteList.as_view(), name="note_list"),
    path('<pk>/', NoteDetail.as_view(), name="note_detail"),
]