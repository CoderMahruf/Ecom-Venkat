from django.contrib import admin
from django.utils.html import format_html
from .models import Banner,Category,Product,ProductImage,ProductColor,ProductSize,ProductVariant
# Register your models here.
admin.site.register(Banner)
admin.site.register(Category)

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"

# Inline for Product Variants
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'size', 'price')
    show_change_link = True

# Product Admin Configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('price', 'stock', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('created_at', 'updated_at', 'main_image_preview')
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'description')
        }),
        ('Pricing/Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Media', {
            'fields': ('image', 'main_image_preview'),
        }),
        ('Status/Dates', {
            'fields': ('is_active', ('created_at', 'updated_at'))
        }),
    )

    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" />', obj.image.url)
        return "No image"
    main_image_preview.short_description = "Main Image Preview"

# Product Variant Admin
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'price')
    list_filter = ('product__category', 'color', 'size')
    search_fields = ('product__title',)
    autocomplete_fields = ('product', 'color', 'size')

# Product Color Admin
@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'color_preview')
    search_fields = ('name',)
    readonly_fields = ('color_preview',)

    def color_preview(self, obj):
        if obj.hex_code:
            return format_html(
                '<div style="background-color:{}; width:30px; height:30px; border:1px solid #000"></div>',
                obj.hex_code
            )
        return "-"
    color_preview.short_description = "Preview"

# Product Size Admin
@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    search_fields = ('product__title',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"     