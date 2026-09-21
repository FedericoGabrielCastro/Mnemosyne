from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "mnemosyne.md"


class VaultApiTests(TestCase):
    def setUp(self) -> None:
        from vaults.services import reset_palace_cache

        reset_palace_cache()
        self.tmp = TemporaryDirectory()
        index_dir = Path(self.tmp.name) / "palace"
        media_dir = Path(self.tmp.name) / "media"
        self.settings = override_settings(
            MNEMOSYNE_LEXICAL=True,
            MNEMOSYNE_INDEX_DIR=index_dir,
            MEDIA_ROOT=media_dir,
        )
        self.settings.enable()
        reset_palace_cache()
        self.client = APIClient()

    def tearDown(self) -> None:
        from vaults.services import reset_palace_cache

        reset_palace_cache()
        self.settings.disable()
        self.tmp.cleanup()

    def test_health(self) -> None:
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "mnemosyne")

    def test_create_vault_ingest_and_search(self) -> None:
        created = self.client.post("/api/vaults/", {"name": "Lethe Annex", "epithet": "A quieter wing"}, format="json")
        self.assertEqual(created.status_code, 201)
        vault_id = created.json()["id"]

        offering = SimpleUploadedFile(
            "mnemosyne.md",
            FIXTURE.read_bytes(),
            content_type="text/markdown",
        )
        uploaded = self.client.post(
            f"/api/vaults/{vault_id}/documents/",
            {"title": "Mythos", "file": offering},
            format="multipart",
        )
        self.assertEqual(uploaded.status_code, 201)
        self.assertEqual(uploaded.json()["status"], "indexed")
        self.assertGreater(uploaded.json()["chunk_count"], 0)

        search = self.client.post(
            f"/api/vaults/{vault_id}/search/",
            {"query": "Titaness of memory", "top_k": 3},
            format="json",
        )
        self.assertEqual(search.status_code, 200)
        self.assertTrue(search.json()["hits"])

        asked = self.client.post(
            f"/api/vaults/{vault_id}/ask/",
            {"question": "Who is Mnemosyne?", "top_k": 3},
            format="json",
        )
        self.assertEqual(asked.status_code, 200)
        self.assertIn("answer", asked.json())
        self.assertEqual(asked.json()["mode"], "extractive")
