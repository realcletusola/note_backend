from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from .serializers import SignUpSerializer, UpdateEmailSerializer, PasswordChangeSerializer

import re 


""" register view """
class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if  serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            password = serializer.data['password']
            password_again = serializer.data['password_again']

            chk_email = User.objects.filter(email=email)

            """ we are performing our validations to the serialized data here bacause
            we want to errors to be returned as a response """
            if password == password_again:
                if len(password) < 8:
                    return Response({
                        "error": "Pasword must be atleast 8 characters"
                    })
                elif not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", password):
                    return Response({
                        "error": "Password must contain at least one special character"
                    })
                elif not any(p.isupper() for p in password):
                    return Response({
                        "error": "Password must have at least one uppercase letter"
                    })
                elif not any(p.islower() for p in password):
                    return Response({
                        "error":"Password must have at least one lowercase letter"
                    })
                elif not any(p.isdigit() for p in password):
                    return Response({
                        "error":"Password must have at least a digit"
                    })
                elif email is None:
                    return Response({
                        "error": "Email is required"
                    })
                elif chk_email.count():
                    return Response({
                        "error":"user with this email already exists"
                    })
                elif len(email) < 6 or len(email) > 60:
                    return Response({
                        "error": "Email must be between 6 to 60 characters"
                    })
                else:
                    user = User.objects.create_user(
                        email=email,
                        password=password
                    )
                    user.save()
                    return Response({
                        "success": "User account created successfully"
                    })
            else:
                return Response({
                    "error": "Passwords must match"
                })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" logout view """
class LogoutView(APIView):
    permissions_classes = (permissions.IsAuthenticated, )

    """ we make this a post request to blacklist the tokens after logout"""
    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



""" logout from all device """
class LogoutAllViews(APIView):
    permissions_classes = (permissions.IsAuthenticated, )

    """ we make this a post request to blacklist the tokens after logout"""
    def post(self, request, format=None):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)


""" Update Email View """
class UpdateEmailView(APIView):    
    permissions_classes = (permissions.IsAuthenticated, )
    """ we use post because we are not returning any instance with the email field,
    the field will be empty for the user to enter a new email """
    def post(self, request, format=None):
        serializer = UpdateEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            current_email = request.user.email
            chk_email = User.objects.filter(email=email)

            if chk_email.count() and email != current_email:
                return Response({
                    "error":"email not available, use a different email"
                })
            elif len(email) < 6 or len(email) > 60:
                return Response({
                    "error":"email must be between 6 to 60 characters"
                })
            else:
                user = request.user
                user.email = email
                user.save()
                serializer.save()

                return Response({
                    "success":"Email changed successfully"
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

""" Password Change Serializer """
class PasswordChangeView(APIView):
    permissions_classes = (permissions.IsAuthenticated, )


    def post(self, request, format=None):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.data["old_password"]
            new_password = serializer.data["new_password"]
            new_password_again = serializer.data["new_password_again"]
            
            user = request.user

            if old_password == user.password:
                if len(new_password) < 8:
                    return Response({
                        "error": "Password must be atleast 8 characters"
                    })
                elif not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", new_password):
                    return Response({
                        "error": "Password must contain at least one special character"
                    })
                elif not any(p.isupper() for p in new_password):
                    return Response({
                        "error": "Password must have at least one uppercase letter"
                    })
                elif not any(p.islower() for p in new_password):
                    return Response({
                        "error":"Password must have at least one lowercase letter"
                    })
                elif not any(p.isdigit() for p in new_password):
                    return Response({
                        "error":"Password must have at least a digit"
                    })
                elif new_password != new_password_again:
                    return Response({
                        "error":"New passwords must match"
                    })
                else:
                    user.set_password(new_password_again)
                    user.save()
                    return Response({
                        "success":"password changed successfully"
                    })
            else:
                return Response({
                    "error":"Old password is incorrect"
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








