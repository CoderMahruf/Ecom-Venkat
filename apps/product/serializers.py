from rest_framework import serializers
from .models import Banner,Category,Product

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','title','feature','image','button_text','button_url','is_active']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','slug','description','image','is_active']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    cat = serializers.CharField(write_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'cat', 'title', 'slug', 'description', 'price', 'stock', 'image', 'is_active']
        read_only_fields = ['id', 'category']

    def create(self, validated_data):
        cat_title = validated_data.pop('cat')
        if cat_title:
            category = Category.objects.get(title=cat_title)
            validated_data['category'] = category
        return super().create(validated_data)


