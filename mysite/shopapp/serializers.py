from django.contrib.auth.models import User
from rest_framework import serializers

from shopapp.models import Product, Order
from myauth.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'avatar']
        read_only_fields = ['user', 'avatar']

class ProductSerializer(serializers.ModelSerializer):
    crated_by = serializers.SerializerMethodField(source='crated_by')

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'crated_by']

    def get_crated_by(self, obj):
        return {
            'id': obj.crated_by.id,
            'username': obj.crated_by.user.username,
            'bio': obj.crated_by.bio,
            'avatar': obj.crated_by.avatar if obj.crated_by.avatar else None
        }

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(many=True,
                                                      queryset=Product.objects.all(),
                                                      source='products',
                                                      write_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['address', 'promocode', 'user', 'is_archived', 'products', 'product_ids']

