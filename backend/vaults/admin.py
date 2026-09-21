from django.contrib import admin

from vaults.models import MemoryDocument, OracleQuery, Vault


@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")


@admin.register(MemoryDocument)
class MemoryDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "vault", "status", "chunk_count", "created_at")


@admin.register(OracleQuery)
class OracleQueryAdmin(admin.ModelAdmin):
    list_display = ("question", "vault", "mode", "created_at")
