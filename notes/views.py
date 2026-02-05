from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save() 
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.pk,
            'message': 'Login successful'
        })



class NoteListApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notes = Note.objects.filter(owner=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # ربط النوت باليوزر اللي عمل الريكويست
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class NoteDetailApi(APIView):
    permission_classes = [IsAuthenticated]
    # Helper function to get the object or return None if it doesn't exist
    def get_object(self, pk, user):
        try:
            return Note.objects.get(pk=pk, owner=user)  # تأكد إن النوت بتاعت اليوزر اللي عامل الريكويست بس
        except Note.DoesNotExist:
            return None

    # 1. Retrieve a single note
    def get(self, request, pk):
        note = self.get_object(pk, request.user)
        if note is None:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    # 2. Update a note
    def put(self, request, pk):
        note = self.get_object(pk,request.user)
        if note is None:
            return Response({"error": "Cannot update, note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. Delete a note
    def delete(self, request, pk):
        note = self.get_object(pk,request.user)
        if note is None:
            return Response({"error": "Cannot delete, note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
