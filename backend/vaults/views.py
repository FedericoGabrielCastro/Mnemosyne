from __future__ import annotations

from pathlib import Path

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from django.conf import settings

from vaults.models import MemoryDocument, OracleQuery, Vault
from vaults.serializers import (
    AskRequestSerializer,
    MemoryDocumentSerializer,
    SearchRequestSerializer,
    VaultSerializer,
)
from vaults.services import palace_for


@api_view(["GET"])
def health(_request):
    return Response(
        {
            "name": "mnemosyne",
            "status": "awake",
            "embedder": "lexical" if settings.MNEMOSYNE_LEXICAL else "fastembed",
        }
    )


class VaultViewSet(viewsets.ModelViewSet):
    queryset = Vault.objects.all()
    serializer_class = VaultSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def destroy(self, request, *args, **kwargs):
        vault = self.get_object()
        palace = palace_for(str(vault.id))
        for document in vault.documents.all():
            palace.forget(str(document.id))
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get", "post"], parser_classes=[MultiPartParser, FormParser, JSONParser])
    def documents(self, request, pk=None):
        vault = self.get_object()
        if request.method == "GET":
            serializer = MemoryDocumentSerializer(vault.documents.all(), many=True)
            return Response(serializer.data)

        serializer = MemoryDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offering = serializer.validated_data["file"]
        title = serializer.validated_data.get("title") or Path(offering.name).stem
        document = MemoryDocument.objects.create(
            vault=vault,
            title=title,
            original_filename=offering.name,
            file=offering,
            mime_type=getattr(offering, "content_type", "") or "",
        )
        _index_document(document)
        return Response(MemoryDocumentSerializer(document).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="documents/(?P<document_id>[^/.]+)")
    def destroy_document(self, request, pk=None, document_id=None):
        vault = self.get_object()
        document = vault.documents.filter(pk=document_id).first()
        if document is None:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        palace_for(str(vault.id)).forget(str(document.id))
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def search(self, request, pk=None):
        vault = self.get_object()
        serializer = SearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hits = palace_for(str(vault.id)).search(
            serializer.validated_data["query"],
            top_k=serializer.validated_data["top_k"],
        )
        return Response(
            {
                "query": serializer.validated_data["query"],
                "hits": [_hit_payload(hit) for hit in hits],
            }
        )

    @action(detail=True, methods=["post"])
    def ask(self, request, pk=None):
        vault = self.get_object()
        serializer = AskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = palace_for(str(vault.id)).ask(
            serializer.validated_data["question"],
            top_k=serializer.validated_data["top_k"],
        )
        OracleQuery.objects.create(
            vault=vault,
            question=result.question,
            answer=result.answer,
            mode=result.mode,
            citation_count=len(result.citations),
        )
        return Response(
            {
                "question": result.question,
                "answer": result.answer,
                "mode": result.mode,
                "citations": [_hit_payload(hit) for hit in result.citations],
            }
        )


def _index_document(document: MemoryDocument) -> None:
    palace = palace_for(str(document.vault_id))
    try:
        result = palace.ingest_path(
            Path(document.file.path),
            document_id=str(document.id),
            title=document.title,
        )
        document.status = MemoryDocument.Status.INDEXED
        document.chunk_count = result.chunks
        document.character_count = result.characters
        document.indexed_at = timezone.now()
        document.error_message = ""
    except Exception as exc:  # noqa: BLE001 - persist failure for the oracle UI
        document.status = MemoryDocument.Status.FAILED
        document.error_message = str(exc)
    document.save()


def _hit_payload(hit) -> dict:
    return {
        "document_id": hit.document_id,
        "chunk_id": hit.chunk_id,
        "title": hit.title,
        "text": hit.text,
        "score": hit.score,
        "metadata": hit.metadata,
    }
