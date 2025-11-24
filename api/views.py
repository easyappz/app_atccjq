from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User, Token
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from api.models import Member, Message
from api.serializers import (
    MessageSerializer,
    MemberSerializer,
    RegisterSerializer,
    LoginSerializer,
    AuthResponseSerializer
)
from api.authentication import MemberTokenAuthentication


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: MessageSerializer}, description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        serializer = MessageSerializer(data)
        return Response(serializer.data)


class RegisterView(APIView):
    """
    Register a new user and return token with user data.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: AuthResponseSerializer},
        description="Register a new user"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Create Member
            member = Member(username=username)
            member.set_password(password)
            member.save()
            
            # Create User for token authentication
            user = User.objects.create_user(
                username=f"member_{member.id}",
                password=password
            )
            user.id = member.id
            user.save()
            
            # Create token
            token, created = Token.objects.get_or_create(user=user)
            
            # Prepare response
            response_data = {
                'token': token.key,
                'user': MemberSerializer(member).data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Login user and return token with user data.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthResponseSerializer},
        description="Login user"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Find member
            try:
                member = Member.objects.get(username=username)
            except Member.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Check password
            if not member.check_password(password):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get or create token
            try:
                user = User.objects.get(id=member.id)
            except User.DoesNotExist:
                # Create user if doesn't exist
                user = User.objects.create_user(
                    username=f"member_{member.id}",
                    password=password
                )
                user.id = member.id
                user.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            # Prepare response
            response_data = {
                'token': token.key,
                'user': MemberSerializer(member).data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Get current user profile.
    """
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MemberSerializer},
        description="Get current user profile"
    )
    def get(self, request):
        member = request.user
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagesView(APIView):
    """
    Get all messages or create a new message.
    """
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MessageSerializer(many=True)},
        description="Get all messages with author information, sorted by creation date"
    )
    def get(self, request):
        messages = Message.objects.select_related('member').all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=MessageSerializer,
        responses={201: MessageSerializer},
        description="Create a new message from current user"
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(member=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
