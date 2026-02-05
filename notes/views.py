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
            return Response({"msg": "done"}, status=status.HTTP_201_CREATED)
        
        return Response({"msg": "Registration failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginApi(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # التعديل هنا: التوكن رجع صافي زي ما كنتِ كاتباه، وضفنا بس msg: done
        return Response({
            'msg': 'done',
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
        # تغليف المصفوفة في كلمة notes عشان الرياكت يشوفها
        return Response({"msg": "done", "notes": serializer.data})

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"msg": "done", "note": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"msg": "Error adding note", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class NoteDetailApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return Note.objects.get(pk=pk, owner=user)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk, request.user)
        if note is None:
            return Response({"msg": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note)
        return Response({"msg": "done", "note": serializer.data})

    def put(self, request, pk):
        note = self.get_object(pk, request.user)
        if note is None:
            return Response({"msg": "Cannot update, note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "done", "note": serializer.data})
        return Response({"msg": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk, request.user)
        if note is None:
            return Response({"msg": "Cannot delete, note not found"}, status=status.HTTP_404_NOT_FOUND)
        
        note.delete()
        return Response({"msg": "done", "message": "Note deleted successfully"}, status=status.HTTP_200_OK)