from rest_framework import serializers 


from . models import Note 


""" note serializer """
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Note
        fields = ['id','title','content','user','date','time']