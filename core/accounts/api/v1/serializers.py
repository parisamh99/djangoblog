# 📦 Import required modules
from django.core import exceptions  # Used to catch Django's validation errors
from rest_framework import (
    serializers,
)  # Base serializers from Django REST Framework
from accounts.models import User, Profile
from django.contrib.auth.password_validation import (
    validate_password,
)  # Django's built-in password strength validator
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404




class RegistrationSerializer(serializers.ModelSerializer):
  
    password = serializers.CharField(max_length=250, write_only=True)
    password1 = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User 
        fields = [
            "email",
            "password",
            "password1",
        ] 

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Passwords do not match")
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        user = User.objects.create_user(**validated_data)
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={
            "input_type": "password"
        }, 
        trim_whitespace=False,
        write_only=True,  
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        if username and password:
           
            user = authenticate(
                request=self.context.get("request"),
                username=username, 
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_verified:
                raise serializers.ValidationError(
                    {"details": "user doesnt verified"}
                )

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"details": "user doesnt verified"}
            )
        
        validated_data["email"] = self.user.email

        validated_data["user_id"] = self.user.id

        return validated_data


class CustomChangePassworSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        # Check if both password fields match
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError("Passwords do not match")
        # Validate password strength using Django's built-in validators
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            # If validation fails, return a list of error messages
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )

        # Return the validated data if everything is fine
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "description",
        ]
        read_only_fields = ["email"]


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = get_object_or_404(User, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"details": "user doesnt exist"}
            )
        if not user_obj.is_verified:
            raise serializers.ValidationError(
                {"details": "user doesnt verified"}
            )
        attrs["user"] = user_obj
        return super().validate(attrs)
