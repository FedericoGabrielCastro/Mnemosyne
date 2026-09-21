# Mnemosyne

Mnemosyne is the Titaness of memory, mother of the nine Muses by Zeus. Before a poet
spoke, they drank from her spring so the song would not dissolve into Lethe, the river
of forgetting.

A memory palace is an art of loci: rooms, colonnades, and gold-leaf tablets where
images are stored so they can be walked later. The vault does not invent. It recalls.

The Muses are Calliope, Clio, Euterpe, Erato, Melpomene, Polyhymnia, Terpsichore,
Thalia, and Urania. Each Muse governs a craft of remembrance: epic, history, lyric,
love poetry, tragedy, hymns, dance, comedy, and astronomy.

Local retrieval-augmented generation works in three motions. First, documents are
split into overlapping shards. Second, each shard is turned into a vector by a local
embedding model. Third, a question is embedded the same way and the nearest shards
are gathered. An oracle may then compose an answer, but only from those shards.

Semantic search differs from keyword search. It matches intent. Asking for "the river
that erases" should surface Lethe even if the query never names her. Asking for
"who taught the poets to remember" should surface Mnemosyne.

Nothing in this palace is sent to a remote model unless you deliberately connect
Ollama. The index lives on disk. The embeddings live on disk. Memory stays local.
