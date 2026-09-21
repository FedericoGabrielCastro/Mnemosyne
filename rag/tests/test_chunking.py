from mnemosyne_rag.chunking import split_text


def test_split_text_keeps_short_documents_whole() -> None:
    chunks = split_text("The vault remembers.", chunk_size=900, chunk_overlap=140)
    assert len(chunks) == 1
    assert chunks[0].text == "The vault remembers."


def test_split_text_overlaps_long_documents() -> None:
    body = "\n\n".join(f"Room {index}: a gold tablet of memory " * 8 for index in range(12))
    chunks = split_text(body, chunk_size=400, chunk_overlap=60)
    assert len(chunks) > 1
    assert chunks[0].index == 0
    assert all(chunk.text for chunk in chunks)
    assert all(not chunk.text[0].islower() or chunk.text.startswith("a gold") for chunk in chunks)
