from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers 



# signup serializer 
class SignUpSerializer(serializers.Serializer): 
    email = serializers.EmailField(max_length=60, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_again = serializers.CharField(min_length=8, required=True)


# update email serializer
class UpdateEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=6, max_length=60, required=True)

    class Meta:
        model = User 
        fields = ['email']


# password change serializer
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=8, required=True)  
    new_password_again = serializers.CharField(min_length=8, required=True)   