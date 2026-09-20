# Running Multi-Step Workflow with Sciunit

Sciunit can be used to execute and containerize complex scientific workflows consisting of multiple steps. The whole workflow can be repeated at a later stage with the same fidelity. We share a real-life workflow of a lightweight retrieval-augmented generation (RAG) pipeline as an example to demonstrate this.


## RAG-Lite
This workflow consists of three steps. It ingests and chunks text data and creates a corpus, which is converted into a retrieval index, which is then queried to retrieve relevant chunks with the given context.

Move into the correct directory:
```bash
cd ~/tutorial/examples/sciunit/rag-lite
```
Install and activate the conda environment to run this example:
```
source ./sciunit-env.sh 
```

## Executing RAG-Lite with Sciunit

### Step 1: Ingest and Chunk Text Data
Read dataset of books in the text files, clean and chunk each one in parallel, and write the combined corpus to a json file.
```
sciunit exec python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
```
It gives the following output:
```
Found books:
 - alice.txt (151191 bytes)
 - frankenstein.txt (421633 bytes)
 - pg64317.txt (306553 bytes)
 - shakespeare_complete.txt (5638480 bytes)

Book IDs: ['alice', 'frankenstein', 'pg64317', 'shakespeare_complete']

Local workers: 8

Submitted 4 local chunking tasks
[1/4] ✓ book pg64317 -> 359 chunks
[2/4] ✓ book frankenstein -> 616 chunks
[3/4] ✓ book alice -> 189 chunks
[4/4] ✓ book shakespeare_complete -> 7198 chunks

All tasks done.
Total chunks collected: 8362

✓ Saved 8362 chunks to gutenberg_corpus.json

Chunks per book:
  alice: 189 chunks
  frankenstein: 616 chunks
  pg64317: 359 chunks
  shakespeare_complete: 7198 chunks

Chunk length stats:
  min: 35
  max: 999
  avg: 822.2
```

### Step 2: Build a BM25 Retrieval Index
Loads the combined corpus, converts chunks into LangChain Document format,
build a BM25Retriever index, and persist it to disk for later on-demand usage.
```
sciunit exec python 02_build_bm25_index.py --corpus gutenberg_corpus.json --index-out bm25_index.pkl
```
It gives an output like this:
```
Loaded 8362 chunks from gutenberg_corpus.json
Built 8362 Documents from corpus
✓ BM25 retriever ready (k=4)
✓ Saved BM25 index to bm25_index.pkl
```

### Step 3: Context-based Retrieval from Index
Load the persisted BM25Retriever index and run a query on the index to retrieve chunks with the given query context.
```
sciunit exec python 03_query_rag.py --index bm25_index.pkl "What happens when Alice falls down the rabbit hole?" --k 4
```
The first few lines of the output look like this:
```
Loaded BM25 retriever from bm25_index.pkl

======================================================================
RAG query: 'What happens when Alice falls down the rabbit hole?'
======================================================================
Retrieved 4 chunks:

[1] book_id=alice  chunk_id=2  pos=1.1%
    There was nothing so _very_ remarkable in that; nor did Alice think it so _very_ much out of the way to hear the Rabbit say to itself, “Oh dear! Oh dear! I shall be late!” (when she thought it over af...

[2] book_id=shakespeare_complete  chunk_id=5999  pos=83.4%
    QUINTUS. My sight is very dull, whate’er it bodes.  MARTIUS. And mine, I promise you. Were it not for shame, Well could I leave our sport to sleep awhile.  [_He falls into the pit._]  QUINTUS. What, a...

[3] book_id=alice  chunk_id=104  pos=55.3%
    “Well, I’d hardly finished the first verse,” said the Hatter, “when the Queen jumped up and bawled out, ‘He’s murdering the time! Off with his head!’”  “How dreadfully savage!” exclaimed Alice.  “And ...
...................................................
...................................................
```

Verify all executions captured in this workflow which show an output like this:
```
> sciunit list
   e1 Sep  8 23:42 python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
   e2 Sep  8 23:43 python 03_query_rag.py 'What happens when Alice falls down the rabbit hole?' --k 4
   e3 Sep  8 23:45 python 03_query_rag.py --index bm25_index.pkl 'What happens when Alice falls down the rabbit hole?' --k 4
```

These entire workflow could be reproduced by repeating the captured executions like this:
```
sciunit repeat e1
sciunit repeat e2
sciunit repeat e3
```