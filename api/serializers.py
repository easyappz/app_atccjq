from rest_framework import serializers
from api.models import Member, Message


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'username', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'username']


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, min_length=4, max_length=128, required=True)

    def validate_username(self, value):
        """Check if username already exists"""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, max_length=128, required=True)


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = MemberSerializer()
