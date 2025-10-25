from django.urls import path
from .. import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns =[
    #registration
    path('registration/',views.RegistrationApiView.as_view(),name='registration'),
    #login token
    #path('login/token/',ObtainAuthToken.as_view(),name='auth_token') #login with obtainauthtoken that wrriten
    path('login/token/',views.CustomAuthToken.as_view(),name='auth_token'), #login with obtainauthtoken that we customize it 
    #logout token
    path('logout/token/',views.CustomDiscardAuthToken.as_view(),name='auth_logout'),
    #email-test
    path('email-test/',views.EmailTestSend.as_view(),name='email-test'),
    #activation
    path('activation/confirm/<str:token>',views.ActivationApiView.as_view(),name='activation_confirm'),
    #resend activation
    path('activation/resend/',views.ResendActivationApiView.as_view(),name='resend_activation'),
    #change password
    path('change-password/',views.CustomChangePasswordView.as_view(),name='change_password'),
    #reset password
    #login jwt
    path('jwt/create/',views.CustomTokenObtainPairView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/',TokenVerifyView.as_view(),name='jwt_verify'),
] 

