1. Cài Đặt Môi Trường
Trước khi bắt đầu, bạn cần tạo môi trường ảo và cài đặt các thư viện cần thiết.

Bước 1: Tạo môi trường ảo
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows

Bước 2: Cài đặt Django và Django REST Framework
pip install django djangorestframework

Bước 3: Khởi tạo dự án Django
django-admin startproject book_management
cd book_management
python manage.py startapp books

Bước 4: Thêm ứng dụng vào settings.py
Mở settings.py và thêm books và rest_framework vào INSTALLED_APPS:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',  # Ứng dụng quản lý sách
]

Bước 5. Tạo Model
Mở books/models.py và thêm các model:
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title
        
Bước 6. Tạo Serializer
Mở books/serializers.py và thêm:
from rest_framework import serializers
from .models import Author, Category, Publisher, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Book
        fields = '__all__'
        
Bước 7. Tạo View
Mở books/views.py và thêm:
from rest_framework import viewsets
from .models import Author, Category, Publisher, Book
from .serializers import AuthorSerializer, CategorySerializer, PublisherSerializer, BookSerializer

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
    
Bước 8. Định Tuyến URL
Mở books/urls.py và thêm:
from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewSet, CategoryViewSet, PublisherViewSet, BookViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
Bước 9. Chạy Migration
Chạy lệnh sau để tạo bảng trong database:
python manage.py makemigrations
python manage.py migrate

Bước 10. Chạy Server
Chạy lệnh: python manage.py runserver

Dùng POSTMan để test:
Dữ liệu mẫu để tạo mới 1 author,category,publisher,book:
Author:
{
    "name": "Your name"
}
Category:
{
    "name": "Django REST Framework"
}
Publisher:
{
    "title": "Some one"
}
Book:
{
    "title": "Django REST Framework",
    "author": 1,
    "category": 1,
    "publisher": 1,
    "published_date": "2024-02-08",
    "isbn": "9781234567897",
    "available_copies": 5
}
