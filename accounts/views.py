from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serailizer = RegisterUserSerializer(data=request.data)
        if reg_serailizer.is_valid():
            newuser = reg_serailizer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serailizer.errors, status=status.HTTP_400_BAD_REQUEST)

        return "User Created"


class BlackListTokenView(APIView):
    permssion_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            print('refresh_token', refresh_token)
            token = RefreshToken(refresh_token)
            print('token', token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)