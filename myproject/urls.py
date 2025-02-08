
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import AuthorViewSet, CategoryViewSet, PublisherViewSet, BookViewSet, BorrowingViewSet, register, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)
router.register(r'borrowings', BorrowingViewSet)

# Define the API endpoints and including the django admin interface
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout, name='logout'),
]
