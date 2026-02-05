from rest_framework import serializers
from .models import Note, Profile  
from django.contrib.auth.models import User

class NoteSerializer(serializers.ModelSerializer):
    _id = serializers.ReadOnlyField(source='id')
    class Meta:
        model = Note
        fields = ['_id', 'id', 'title', 'content', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age', 'phone']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        user_age = validated_data.pop('age', None)
        user_phone = validated_data.pop('phone', None)
        
        user_email = validated_data['email']
        display_name = validated_data['username']

        user = User.objects.create_user(
            username=user_email,
            password=validated_data['password'],
            email=user_email,
            first_name=display_name 
        )

        if hasattr(user, 'profile'):
            profile = user.profile
            profile.age = user_age
            profile.phone = user_phone
            profile.save()

        return user