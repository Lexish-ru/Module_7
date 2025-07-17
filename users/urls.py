from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, PaymentListView,UserRegisterView, StripePaymentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "users"
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stripe/', StripePaymentView.as_view(), name='stripe-pay'),
]
urlpatterns += router.urls
