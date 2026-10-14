from rest_framework import serializers
from .models import Category, Destination

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class DestinationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='categories'
    )

    class Meta:
        model = Destination
        fields = "__all__"

