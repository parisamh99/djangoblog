# 📦 Import required modules
from django.core import exceptions  # Used to catch Django's validation errors
from rest_framework import serializers  # Base serializers from Django REST Framework
from accounts.models import User, Profile
from django.contrib.auth.password_validation import (
    validate_password,
)  # Django's built-in password strength validator
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


# 🔹 Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):
    # Extra field for confirming the password
    password1 = serializers.CharField(max_length=250, write_only=True)
    # Primary password field
    password = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = User  # The model this serializer is based on
        fields = [
            "email",
            "password",
            "password1",
        ]  # Fields that will be accepted in the API

    # 🧩 Custom validation logic
    def validate(self, attrs):
        # Check if both password fields match
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError("Passwords do not match")
        # Validate password strength using Django's built-in validators
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            # If validation fails, return a list of error messages
            raise serializers.ValidationError({"password": list(e.messages)})

        # Return the validated data if everything is fine
        return attrs

    # 🏗️ Create method — executed after successful validation
    def create(self, validated_data):
        # Remove password1 (confirmation field) before saving to the database
        validated_data.pop("password1", None)

        # Create a new user using Django's create_user method
        # (this automatically hashes the password)
        user = User.objects.create_user(**validated_data)

        # Return the created user instance
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    # Email field for user login
    # write_only=True means it won't be included in the response
    email = serializers.CharField(label=_("Email"), write_only=True)

    # Password field with masked input
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},  # makes it render as a password field
        trim_whitespace=False,  # don't strip spaces from input
        write_only=True,  # not returned in responses
    )

    # Token field that will be returned after successful authentication
    # read_only=True means the client can't send this value
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        # Extract email and password from incoming data
        username = attrs.get("email")
        password = attrs.get("password")

        # Ensure both email and password are provided
        if username and password:
            # Authenticate the user using Django's built-in authentication system
            # The `authenticate` function returns a user object if credentials are valid,
            # otherwise it returns None
            user = authenticate(
                request=self.context.get("request"),
                username=username,  # using email as username
                password=password,
            )

            # If authentication failed, raise a validation error
            # Note: for inactive users (is_active=False), `authenticate` also returns None
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_verified:
                raise serializers.ValidationError({"details": "user doesnt verified"})

        else:
            # If either email or password is missing
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        # Add the authenticated user to attrs for later use in the view
        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the parent class's validate method to perform
        # the normal authentication and token generation.
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user doesnt verified"})

        # Add the user's email to the response data.
        validated_data["email"] = self.user.email

        # Add the user's ID (from the custom 'id()' method to the response data.
        validated_data["user_id"] = self.user.id

        # Return the final response data including tokens and extra user info.
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
            raise serializers.ValidationError({"new_password": list(e.messages)})

        # Return the validated data if everything is fine
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "email", "first_name", "last_name", "image", "description"]
        read_only_fields = ["email"]


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = get_object_or_404(User, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "user doesnt exist"})
        if not user_obj.is_verified:
            raise serializers.ValidationError({"details": "user doesnt verified"})
        attrs["user"] = user_obj
        return super().validate(attrs)
