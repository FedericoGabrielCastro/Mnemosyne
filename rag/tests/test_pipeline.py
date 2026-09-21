from tests.conftest import FIXTURES


def test_ingest_and_semantic_search(palace) -> None:
    result = palace.ingest_path(FIXTURES / "mnemosyne.md", document_id="myth-1")

    assert result.chunks >= 1
    hits = palace.search("Who is the Titaness of memory?", top_k=3)
    assert hits
    assert any("Mnemosyne" in hit.text for hit in hits)
    assert hits[0].score > 0


def test_ask_is_extractive_without_ollama(palace) -> None:
    palace.ingest_path(FIXTURES / "mnemosyne.md", document_id="myth-1")
    answer = palace.ask("What is a memory palace?", prefer_generative=False)

    assert answer.mode == "extractive"
    assert answer.citations
    assert "memory" in answer.answer.lower()


def test_forget_removes_document(palace) -> None:
    palace.ingest_path(FIXTURES / "mnemosyne.md", document_id="myth-1")
    palace.forget("myth-1")
    assert palace.search("Mnemosyne") == []
    assert palace.stats().chunks == 0
