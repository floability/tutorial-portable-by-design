#!/usr/bin/env python3
"""
03_query_rag.py

Workflow step 3 of 3: loads the pickled BM25 retriever from step 2
(02_build_bm25_index.py) and runs one or more RAG-lite queries against it,
printing the retrieved chunks and the assembled context+question prompt
(no LLM call is made -- same scope as the original notebook).

Examples:
    python 03_query_rag.py "What happens when Alice falls down the rabbit hole?"

    python 03_query_rag.py \\
        "What happens when Alice falls down the rabbit hole?" \\
        "What does Hamlet mean when he says 'To be or not to be'?" \\
        --k 4
"""

import argparse
import pickle
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument("queries", nargs="+", help="One or more questions to query the corpus with")
    p.add_argument("--index", type=Path, default=Path("bm25_index.pkl"),
                    help="Pickled BM25 retriever from step 2 (default: bm25_index.pkl)")
    p.add_argument("--k", type=int, default=4, help="Top-k chunks to retrieve per query (default: 4)")

    return p.parse_args()


def rag_query(retriever, query: str, k: int = 4):
    """
    RAG-style helper using the modern LangChain 'invoke' interface.
    Returns (results, prompt); also prints a readable summary.
    """
    retriever.k = k
    results = retriever.invoke(query)

    print("\n" + "=" * 70)
    print(f"RAG query: {query!r}")
    print("=" * 70)
    print(f"Retrieved {len(results)} chunks:\n")

    for i, doc in enumerate(results, 1):
        meta = doc.metadata
        pos_pct = f"{100 * meta.get('relative_position', 0.0):.1f}%"
        print(f"[{i}] book_id={meta['book_id']}  chunk_id={meta['chunk_id']}  pos={pos_pct}")
        preview = doc.page_content[:200].replace("\n", " ")
        print(f"    {preview}...")
        print()

    context = "\n\n".join(
        f"[book {doc.metadata['book_id']} | chunk {doc.metadata['chunk_id']}] {doc.page_content}"
        for doc in results
    )

    prompt = f"""You are a helpful assistant answering questions about classic literature.

Use ONLY the following context to answer the question. If the answer is not in the context, say you don't know.

Context:
{context}

Question: {query}
Answer:"""

    return results, prompt


def main():
    args = parse_args()

    with open(args.index, "rb") as f:
        retriever = pickle.load(f)
    print(f"Loaded BM25 retriever from {args.index}")

    for query in args.queries:
        _, prompt = rag_query(retriever, query, args.k)
        print(prompt)
        print()


if __name__ == "__main__":
    main()
