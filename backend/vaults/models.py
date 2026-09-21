from __future__ import annotations

import uuid

from django.db import models
from django.utils.text import slugify


class Vault(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    epithet = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base = slugify(self.name) or "vault"
            slug = base
            index = 2
            while Vault.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)


class MemoryDocument(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        INDEXED = "indexed", "Indexed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vault = models.ForeignKey(Vault, related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    original_filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="offerings/%Y/%m/")
    mime_type = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    chunk_count = models.PositiveIntegerField(default=0)
    character_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    indexed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class OracleQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vault = models.ForeignKey(Vault, related_name="queries", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    mode = models.CharField(max_length=20)
    citation_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
