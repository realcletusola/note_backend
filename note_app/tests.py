
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework.test import APIClient
from rest_framework import status

from .models import Note 


""" urls for note and note detail """
note_url = reverse('note_list')

class NoteApiView(TestCase):

    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@email.com",
            password="t3$tuser"
            )
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.note = Note.objects.create(
            title="new title",
            content="new content",
            user=self.user
        )
        self.note.save()

    #create note 
    def test_create_note(self): 
        data = {
            "title":"new title",
            "content":"new content",
            "user":self.user
            
        }
        response = self.client.post(note_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # get all notes by user 
    def test_get_note(self):
        response = self.client.get(note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # # get note detail
    def test_get_note_detail(self):
        note_detail_url = reverse('note_detail', kwargs={'pk':self.note.id})
        response = self.client.get(note_detail_url, auth={"testuser@email.com","t3$tuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # edit note with put method
    def test_put_note(self):
        payload = {
            "title":"updated title",
            "content":"updated content"           
        }
        note_detail_url = reverse('note_detail', kwargs={'pk':self.note.id})

        response = self.client.put(note_detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # edit note with patch method
    def test_patch_note(self):
        payload = {
            "title":"updated title",
            "content":"updated content"           
        }
        note_detail_url = reverse('note_detail', kwargs={'pk':self.note.id})

        response = self.client.patch(note_detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # test delete note 
    def test_delete_note(self):
        note_detail_url = reverse('note_detail', kwargs={'pk':self.note.id})
        response = self.client.delete(note_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
