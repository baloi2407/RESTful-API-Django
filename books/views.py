from rest_framework import viewsets
from .models import Author, Category, Publisher, Book, Borrowing
from .serializers import AuthorSerializer, CategorySerializer, PublisherSerializer, BookSerializer, BorrowingSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

# API Đăng ký người dùng mới
@api_view(['POST'])
@permission_classes([AllowAny])  # Cho phép truy cập không cần login
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Thiếu username hoặc password"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username đã tồn tại"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "Đăng ký thành công!"}, status=201)


# API Đăng xuất (Xoá refresh token)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Đảm bảo user đã đăng nhập mới được logout
def logout(request):
    try:
        refresh_token = request.data.get("refresh")  # Lấy refresh token từ request
        if not refresh_token:
            return Response({"error": "Thiếu refresh token!"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()  # Thêm token vào danh sách blacklist

        return Response({"message": "Đăng xuất thành công!"}, status=200)
    except Exception as e:
        return Response({"error": "Token không hợp lệ hoặc đã bị thu hồi"}, status=400)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]  # Chỉ Admin mới có quyền truy cập

class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
