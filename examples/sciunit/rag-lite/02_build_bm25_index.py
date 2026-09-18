#!/usr/bin/env python3
"""
02_build_bm25_index.py

Workflow step 2 of 3: loads gutenberg_corpus.json from step 1
(01_ingest_and_chunk_local.py), converts chunks into LangChain Documents,
builds a BM25Retriever, and pickles it to disk so step 3
(03_query_rag.py) can load it instantly without rebuilding the index.

Example:
    python 02_build_bm25_index.py --corpus gutenberg_corpus.json --index-out bm25_index.pkl
"""

import argparse
import json
import pickle
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever  # uses rank-bm25 under the hood


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument("--corpus", type=Path, default=Path("gutenberg_corpus.json"),
                    help="Corpus JSON written by step 1 (default: gutenberg_corpus.json)")
    p.add_argument("--index-out", type=Path, default=Path("bm25_index.pkl"),
                    help="Where to write the pickled BM25 retriever (default: bm25_index.pkl)")
    p.add_argument("--k", type=int, default=4,
                    help="Default top-k chunks the retriever returns per query (default: 4)")

    return p.parse_args()


def main():
    args = parse_args()

    with open(args.corpus, "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print(f"Loaded {len(corpus)} chunks from {args.corpus}")

    documents = [
        Document(
            page_content=c["text"],
            metadata={
                "book_id": c["book_id"],
                "chunk_id": c["chunk_id"],
                "relative_position": c["relative_position"],
                "n_words": c["n_words"],
            },
        )
        for c in corpus
    ]
    print(f"Built {len(documents)} Documents from corpus")

    retriever = BM25Retriever.from_documents(documents)
    retriever.k = args.k
    print(f"\u2713 BM25 retriever ready (k={args.k})")

    with open(args.index_out, "wb") as f:
        pickle.dump(retriever, f)
    print(f"\u2713 Saved BM25 index to {args.index_out.resolve()}")


if __name__ == "__main__":
    main()
