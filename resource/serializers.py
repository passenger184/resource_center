from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, UploadedFile, Folder, FileSharing, Tag

User = get_user_model()

class FolderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    subfolders = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    owner_first_name = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent', 'created_at', 'subfolders', 'files', 'is_starred', 'owner_email', 'owner_first_name']

    def get_subfolders(self, obj):
        return FolderSerializer(obj.subfolders.all(), many=True).data

    def get_files(self, obj):
        return UploadedFileSerializer(obj.files.all(), many=True).data

    def get_owner_email(self, obj):
        if obj.owner:
            return obj.owner.email
        return None    

    def get_owner_first_name(self, obj):
        if obj.owner:
            return obj.owner.first_name
        return None      

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]  # Include 'id' for API use


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class UploadedFileSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested representation
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )  # Accept category ID in requests
    
    owner_email = serializers.SerializerMethodField()
    owner_first_name = serializers.SerializerMethodField()

    meta_tags = TagSerializer(many=True, read_only=True)
    meta_tag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = UploadedFile
        fields = ["id", "name", "file", "file_type", "file_size", "category", "category_id", "uploaded_at", 'folder', 'is_starred', 'is_archived', 'is_public', 'owner_email',  'owner_first_name', 'meta_tags', 'meta_tag_names']

    def get_owner_email(self, obj):
        if obj.owner:
            return obj.owner.email
        return None

    def get_owner_first_name(self, obj):
        if obj.owner:
            return obj.owner.first_name
        return None      

    def create(self, validated_data):
        tag_names = validated_data.pop('meta_tag_names', [])
        instance = super().create(validated_data)
        self._handle_tags(instance, tag_names)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('meta_tag_names', [])
        instance = super().update(instance, validated_data)
        self._handle_tags(instance, tag_names)
        return instance

    def _handle_tags(self, instance, tag_names):
        instance.meta_tags.clear()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name.strip())
            instance.meta_tags.add(tag)


class FileSharingSerializer(serializers.ModelSerializer):
    shared_by = serializers.ReadOnlyField(source='shared_by.email')  # or username
    file = UploadedFileSerializer(read_only=True)
    shared_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FileSharing
        fields = ['id', 'file', 'shared_to', 'shared_by', 'shared_at', 'message', 'share_type']
        read_only_fields = ['shared_by', 'shared_at']

    def validate(self, data):
        if not data.get('file') and not data.get('folder'):
            raise serializers.ValidationError("Either a file or a folder must be provided.")
        if data.get('file') and data.get('folder'):
            raise serializers.ValidationError("Cannot share both file and folder at the same time.")
        return data
    

class EmailShareSerializer(serializers.Serializer):
    recipients = serializers.ListField(
        child=serializers.EmailField(),
        allow_empty=False
    )
    message = serializers.CharField()
    file_id = serializers.IntegerField()