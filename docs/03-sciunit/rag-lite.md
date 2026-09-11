# Running Multi-Step Workflow with Sciunit

Sciunit can be used to execute and containerize complex scientific workflows consisting of multiple steps. The whole workflow can be repeated at a later stage with the same fidelity. We share a real-life workflow of a lightweight retrieval-augmented generation (RAG) pipeline as an example to demonstrate this.

## RAG-Lite

## Executing RAG-Lite with Sciunit

### Step 1: Ingest and Chunk Text Data
```
python 01_ingest_and_chunk_local.py --data-dir ./data --output gutenberg_corpus.json --workers 8
```

### Step 2: Build a BM25 Retrieval Index
```
python 02_build_bm25_index.py --corpus gutenberg_corpus.json --index-out /home/exouser/Downloads/raglite-manual/bm25_index.pkl
```

### Step 3: Context-based Retrieval from Index
```
python 03_query_rag.py --index /home/exouser/Downloads/raglite-manual/bm25_index.pkl "What happens when Alice falls down the rabbit hole?" --k 4
```