from rest_framework import serializers
from api.models import Member, Message


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'member', 'username', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'username']


class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4, max_length=128)

    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create a new member with hashed password"""
        member = Member(
            username=validated_data['username']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member

    def update(self, instance, validated_data):
        """Update member data with password hashing"""
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class MemberRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=4, max_length=128)

    def validate_username(self, value):
        """Check if username already exists"""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        """Create a new member"""
        member = Member(
            username=validated_data['username']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, max_length=128)
