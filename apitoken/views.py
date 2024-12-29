from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def login(request):
    print(request.data)

    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user = user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    #print(request.user)

    serializer=UserSerializer(instance=request.user)

    #return Response(" you are login with {}".format(request.user.username),status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)



import logging
logger = logging.getLogger(__name__)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Elimina el token asociado al usuario autenticado
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
            return Response({"message": "Sesión cerrada exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Token no encontrado para este usuario."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Log del error
        logger.error(f"Error en el logout: {str(e)}")
        return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
