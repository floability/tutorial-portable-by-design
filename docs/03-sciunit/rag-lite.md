# Running Multi-Step Workflow with Sciunit

Sciunit can be used to execute and containerize complex scientific workflows consisting of multiple steps. The whole workflow can be repeated at a later stage with the same fidelity. We share a real-life workflow of a lightweight retrieval-augmented generation (RAG) pipeline as an example to demonstrate this.


## RAG-Lite
This workflow consists of three steps. It (1) ingests and chunks text data and creates a corpus, (2) which is converted into a retrieval index, (3) which is then queried to retrieve relevant chunks with the given context.

## Before you begin

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

Activate the prepared, read-only RAG-Lite environment:

```bash
source /opt/tutorial/activate-raglite-sciunit.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

Create the RAG-Lite environment the first time you run this exercise:

```bash
conda create -y -n raglite-sciunit-env python=3.11 pip
conda activate raglite-sciunit-env
python -m pip install \
  langchain-community \
  langchain-text-splitters \
  rank-bm25 \
  sciunit2
```

If the environment already exists, activate it without recreating it:

```bash
conda activate raglite-sciunit-env
```

**Continue with either setup**

Move into the example directory:

```bash
cd ~/tutorial/examples/sciunit/rag-lite
```

## Create your Sciunit Project
Create another Sciunit project:
```bash
sciunit create project-raglite
```
This will show an output similar to this:
```
Opened empty sciunit at /home/user02/sciunit/project-raglite
```

## Executing RAG-Lite Workflow with Sciunit

### Step 1: Ingest and Chunk Text Data
Read dataset of books in the text files, clean and chunk each one in parallel, and write the combined corpus to a json file.
```bash
sciunit exec python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
```
It will give an output similar to this:
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

[project-raglite e1] python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
 Date: Mon, 21 Sep 2026 21:50:46 +0000
```

### Step 2: Build a BM25 Retrieval Index
Loads the combined corpus, converts chunks into LangChain Document format,
build a BM25Retriever index, and persist it to disk for later on-demand usage.
```bash
sciunit exec python 02_build_bm25_index.py --corpus gutenberg_corpus.json --index-out bm25_index.pkl
```
It will give an output similar to this:
```
Loaded 8362 chunks from gutenberg_corpus.json
Built 8362 Documents from corpus
✓ BM25 retriever ready (k=4)
✓ Saved BM25 index to bm25_index.pkl

[project-raglite e2] python 02_build_bm25_index.py --corpus gutenberg_corpus.json --index-out bm25_index.pkl
 Date: Mon, 21 Sep 2026 21:51:33 +0000
```
_You can ignore any warning messages in the output_.

### Step 3: Context-based Retrieval from Index
Load the persisted BM25Retriever index and run a query on the index to retrieve chunks with the given query context.
```bash
sciunit exec python 03_query_rag.py --index bm25_index.pkl "What happens when Alice falls down the rabbit hole?" --k 4
```
The first and the last few lines of the output will look like this:
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
    “Well, I’d hardly finished the first verse,” said the Hatter, “when the Queen jumped up and bawled out, ‘He’s murdering the time! Off with his head!’”  “How dreadfully savage!” exclaimed Alice. 
...................................................
...................................................
...................................................
...................................................

[project-raglite e3] python 03_query_rag.py --index bm25_index.pkl 'What happens when Alice falls down the rabbit hole?' --k 4
 Date: Mon, 21 Sep 2026 21:52:28 +0000
```
_You can ignore any warning messages in the output_.

## Verify the Captured Workflow
Verify all executions captured in this workflow:
```bash
sciunit list
```
This will show an output similar to this:
```
   e1 Sep  8 23:42 python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
   e2 Sep  8 23:43 python 03_query_rag.py 'What happens when Alice falls down the rabbit hole?' --k 4
   e3 Sep  8 23:45 python 03_query_rag.py --index bm25_index.pkl 'What happens when Alice falls down the rabbit hole?' --k 4
```

## Repeat RAG-Lite Workflow with Sciunit

This captured RAG-Lite workflow could be repeated in the same environment, or another environment which does not have the necessary dependenceis to execute it. 

Switch to the base tutorial environment, which has Sciunit but not the RAG-Lite dependencies.

<span class="tutorial-route-label tutorial-route--live">Live tutorial</span>

```bash
source /opt/tutorial/activate.sh
```

<span class="tutorial-route-label tutorial-route--self-managed">Self-managed</span>

```bash
conda activate tutorial-env
```

**Continue with either setup**

This environment has Sciunit installed in it, but does not have any of the core dependencies required to execute RAG-Lite workflow, including `langchain` and `rank-bm25`. You can confirm by running the following:
```bash
conda list | grep sciunit
```
You will see the following output:
```
sciunit2  0.4.post164.dev115100208  pypi_0  pypi
```
Now run these:
```bash
conda list | grep langchain
conda list | grep rankbm25
```
You will not see any response since these do not exist in this environment.

Now repeat the executions one by one:
```bash
sciunit repeat e1
sciunit repeat e2
sciunit repeat e3
```

These will successfully execute the entire workflow and give the desired output as before.

[**Next: Run an interactive workflow with FLINC →**](rag-lite-flinc.md)
