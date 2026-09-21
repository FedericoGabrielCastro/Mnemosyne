from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from vaults.models import MemoryDocument, Vault
from vaults.views import _index_document

SEED_TEXT = Path(__file__).resolve().parents[2] / "fixtures" / "mnemosyne.md"


class Command(BaseCommand):
    help = "Inscribe the first vault with the Mnemosyne mythos."

    def handle(self, *args, **options):
        vault, created = Vault.objects.get_or_create(
            slug="first-palace",
            defaults={
                "name": "The First Palace",
                "epithet": "Where the Muses still drink.",
            },
        )
        if vault.documents.exists():
            self.stdout.write("The First Palace already holds offerings.")
            return
        if not SEED_TEXT.exists():
            raise SystemExit(f"Seed manuscript missing: {SEED_TEXT}")
        document = MemoryDocument(
            vault=vault,
            title="Mnemosyne",
            original_filename="mnemosyne.md",
            mime_type="text/markdown",
        )
        document.file.save("mnemosyne.md", ContentFile(SEED_TEXT.read_bytes()), save=True)
        _index_document(document)
        verb = "inscribed" if created else "replenished"
        self.stdout.write(self.style.SUCCESS(f"{verb} {vault.name} ({document.status})"))
