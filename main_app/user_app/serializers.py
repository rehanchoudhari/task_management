from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



def check_email_validity(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class ProfileSerializer(serializers.ModelSerializer):
    user_link = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    role = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Profile
        fields = ['url', 'id', 'image', 'role', 'user', 'user_link']


class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    profile = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request_method = self.context['request'].method
        if request_method == 'POST':
            self.fields['username'] = serializers.CharField(write_only=True)
            self.fields.pop('old_password')
        elif request_method in ['PUT', 'PATCH']:
            self.fields['username'] = serializers.CharField(read_only=True)
            self.fields.pop('confirm_password')

    def validate(self, data):
        request_method = self.context['request'].method
        password = data.get('password', None)
        if request_method == 'POST':
            confirm_password = data.get('confirm_password', None)
            email = data.get('email')
            if not check_email_validity(email):
                raise serializers.ValidationError({'Info': 'Passwords do not match'})
            if not password or not confirm_password or password != confirm_password:
                raise serializers.ValidationError({'Info': 'Passwords do not match'})
            
        elif request_method in ['PUT', 'PATCH']:
            old_password = data.get('old_password', None)
            if not password:
                raise serializers.ValidationError({'Info': 'password is not provided'})
            if not old_password:
                raise serializers.ValidationError({'Info': 'old_password is not provided'})
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        try:
            user = instance
            password = validated_data.pop('password')
            old_password = validated_data.pop('old_password')
            if user.check_password(old_password):
                user.set_password(password)
            else:
                raise serializers.ValidationError({'info': 'Old password is incorrect'})
        except Exception as e:
            raise serializers.ValidationError({"info": e})
        return super(UserSerializer, self).update(instance, validated_data)


    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'email'
                  , 'password', 'old_password', 'confirm_password', 'profile']