from django.http import Http404

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status, permissions

from .serializers import NoteSerializer
from .models import Note 


""" list and post note view"""
class NoteList(APIView):
    permissions_classes = (permissions.IsAuthenticated, )
    serializer_class = NoteSerializer

    # get objects by user 
    def get_object(self):
        return Note.objects.filter(user=self.request.user)
    
    # get notes 
    def get(self, request, format=None):
        note = self.get_object()
        serializer = self.serializer_class(note, many=True)
        return Response({
            "data":serializer.data 
        },status=status.HTTP_200_OK)
    
    # create notes 
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            return Response({
                "data":serializer.data,
                "message": "Note created"
            },status=status.HTTP_201_CREATED)
        
        return Response({
            "message":serializer.errors,
            "status":status.HTTP_400_BAD_REQUEST
        })

""" retrieve, update and delete note view"""
class NoteDetail(APIView):
    permissions_classes = (permissions.IsAuthenticated, )
    serializer_class = NoteSerializer

    # get object by primary key and user 
    def get_object(self, pk):
        try:
            return Note.objects.get(id=pk, user=self.request.user)
        except:
            raise Http404
        
    # get notes by primary key 
    def get(self, request, pk, format=None):
        """ we use .filter because we want the note to return an object
            and not a single instance """
        note = Note.objects.filter(pk=pk, user=self.request.user)
        serializer = self.serializer_class(note, many=True)
        return Response({
            "data":serializer.data
        }, status=status.HTTP_200_OK)
    

    # edit notes with put 
    def put(self, request, pk, format=None):
        notes = self.get_object(pk)
        serializer = self.serializer_class(notes, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({
                "data":serializer.data,
                "message":"Note saved"
            },status=status.HTTP_201_CREATED)

        return Response({
            "meassage":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)


    # update note by patch 
    def patch(self, request, pk, format=None):
        notes = self.get_object(pk)
        serializer = self.serializer_class(notes, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({
                "data":serializer.data,
                "message":"Note saved"
            },status=status.HTTP_201_CREATED)
        
        return Response({
            "message":serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    
    
    # delete note 
    def delete(self, request, pk, format=None):
        notes = self.get_object(pk)
        notes.delete()
        return Response({
            "message":"Note deleted"
        },status=status.HTTP_204_NO_CONTENT)


