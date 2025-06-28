from rest_framework import serializers
from .models import Banner,Category,Product,ProductImage,ProductSize,ProductColor,ProductVariant
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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ['name']

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['name']

class ProductVariantSerializer(serializers.ModelSerializer):
    color = ProductColorSerializer()
    size = ProductSizeSerializer()
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'size', 'price']
    
    def get_price(self, obj):
        return format(obj.price, '.2f')
    

class ProductSerializer(serializers.ModelSerializer):
    cat = serializers.CharField(write_only=True)
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'category', 'cat', 'title', 'slug', 'description', 'price', 'stock', 'images','variants']
        read_only_fields = ['id', 'category']

    def create(self, validated_data):
        cat_title = validated_data.pop('cat')
        if cat_title:
            category = Category.objects.get(title=cat_title)
            validated_data['category'] = category
        return super().create(validated_data)