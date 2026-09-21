from rest_framework import serializers

from vaults.models import MemoryDocument, Vault


class VaultSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField(source="documents.count", read_only=True)

    class Meta:
        model = Vault
        fields = ["id", "name", "slug", "epithet", "document_count", "created_at", "updated_at"]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class MemoryDocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = MemoryDocument
        fields = [
            "id",
            "title",
            "original_filename",
            "file",
            "mime_type",
            "status",
            "chunk_count",
            "character_count",
            "error_message",
            "created_at",
            "indexed_at",
        ]
        read_only_fields = [
            "id",
            "original_filename",
            "mime_type",
            "status",
            "chunk_count",
            "character_count",
            "error_message",
            "created_at",
            "indexed_at",
        ]
        extra_kwargs = {"title": {"required": False, "allow_blank": True}}

    def validate_file(self, value):
        name = value.name.lower()
        if not name.endswith((".txt", ".md", ".markdown", ".pdf")):
            raise serializers.ValidationError("Offer a .txt, .md, or .pdf manuscript.")
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Offerings must be 10MB or smaller.")
        return value


class SearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField()
    top_k = serializers.IntegerField(min_value=1, max_value=20, default=5)


class AskRequestSerializer(serializers.Serializer):
    question = serializers.CharField()
    top_k = serializers.IntegerField(min_value=1, max_value=20, default=5)
