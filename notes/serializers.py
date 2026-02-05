from rest_framework import serializers
from .models import Note, Profile  
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    age = serializers.IntegerField(required=False, allow_null=True) # أضفنا السماح بالقيمة الفارغة
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age', 'phone']

    def create(self, validated_data):
        user_age = validated_data.pop('age', None)
        user_phone = validated_data.pop('phone', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )

        if hasattr(user, 'profile'):
            profile = user.profile
            profile.age = user_age
            profile.phone = user_phone
            profile.save()

        return user