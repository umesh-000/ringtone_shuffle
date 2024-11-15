from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
from shuffle import models

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    user_phone = serializers.CharField(
        required=True,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    # New fields for ringtone_language, state, city, is_all, and DOB
    ringtone_language = serializers.PrimaryKeyRelatedField(
        queryset=models.Ringtone_Language.objects.all(), 
        required=False, 
        allow_null=True
    )
    state = serializers.PrimaryKeyRelatedField(
        queryset=models.State.objects.all(), 
        required=False, 
        allow_null=True
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=models.City.objects.all(), 
        required=False, 
        allow_null=True
    )
    is_all = serializers.BooleanField(default=False)
    
    # Adding Date of Birth field
    user_dob = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'user_name', 'user_phone', 'user_gender', 'password', 'password2', 'ringtone_language', 'state', 'city', 'is_all', 'user_dob')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if not attrs['user_phone'].isdigit():
            raise serializers.ValidationError({"user_phone": "Phone number must contain only digits."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        
        user = User.objects.create(
            email=validated_data['email'],
            user_name=validated_data['user_name'],
            user_phone=validated_data['user_phone'],
            user_gender=validated_data['user_gender'],
            ringtone_language=validated_data.get('ringtone_language', None),
            state=validated_data.get('state', None),
            city=validated_data.get('city', None),
            is_all=validated_data.get('is_all', False),
            user_dob=validated_data.get('user_dob', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'user_name', 'user_phone','user_gender','profile_img')


class RingtoneSerializer(serializers.ModelSerializer):
    ringtone_url = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Ringtone
        fields = (
            'id', 'ringtone_title', 'ringtone_language', 'ringtone_year_start', 'ringtone_year_end',
            'ringtone_url', 'audio_type', 'is_hyped', 'state', 'city', 'created_at', 'updated_at'
        )

    def get_ringtone_url(self, obj):
        if obj.ringtone_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.ringtone_file.url)
            return obj.ringtone_file.url
        return None


class RingtoneLanguageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.Ringtone_Language
        fields = ['id', 'language_name', 'status', 'image_url']
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                full_url = request.build_absolute_uri(obj.image.url)
                return full_url
            return obj.image.url
        return None


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ['id', 'name', 'state']