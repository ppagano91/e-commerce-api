from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('id','username','email','name','last_name','image','is_active','is_staff')
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()

        return updated_user


class UserListSerializer(serializers.Serializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance["id"],
            'username': instance["username"],
            'email': instance["email"],
            'password': instance["password"],
        }