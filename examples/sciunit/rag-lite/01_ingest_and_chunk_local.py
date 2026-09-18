#!/usr/bin/env python3
"""
01_ingest_and_chunk_local.py

Workflow step 1 of 3: discovers local Gutenberg .txt books,
cleans and chunks each one in parallel using a local process pool
(concurrent.futures.ProcessPoolExecutor), and writes the combined corpus to
gutenberg_corpus.json for step 2 (02_build_bm25_index.py).

Example:
    python 01_ingest_and_chunk_local.py --data-dir data --workers 8
"""

import argparse
import json
import os
import concurrent.futures as cf
from collections import Counter
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    p.add_argument("--data-dir", type=Path, default=Path("data"),
                    help="Directory containing Gutenberg .txt files (default: data)")
    p.add_argument("--workers", type=int, default=os.cpu_count(),
                    help="Number of local worker processes (default: number of CPU cores)")
    p.add_argument("--output", type=Path, default=Path("gutenberg_corpus.json"),
                    help="Where to write the combined corpus JSON (default: gutenberg_corpus.json)")

    return p.parse_args()


def book_id_from_path(path: Path) -> str:
    return path.stem


def clean_and_chunk_book(local_filename: str, book_id: str):
    """
    Read a local Gutenberg .txt file, clean it, and chunk it into ~1000-character
    segments for RAG-style use. Imports are kept inside the function so it can be
    shipped to a worker process cleanly (matches the original TaskVine worker shape).

    Returns:
        list[dict]: one dict per chunk (book_id, chunk_id, total_chunks,
                    relative_position, text, chunk_length, n_chars, n_words, preview)
    """
    import re
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # --- 1. Read full file ---
    with open(local_filename, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # --- 2. Strip Gutenberg boilerplate (best-effort) ---
    start_markers = [
        "*** START OF THIS PROJECT GUTENBERG",
        "*** START OF THE PROJECT GUTENBERG",
        "***START OF THE PROJECT GUTENBERG",
        "*END*THE SMALL PRINT",  # older texts
    ]
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[idx + len(marker):]
            break

    end_markers = [
        "*** END OF THIS PROJECT GUTENBERG",
        "*** END OF THE PROJECT GUTENBERG",
        "***END OF THE PROJECT GUTENBERG",
    ]
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break

    # --- 3. Basic normalization ---
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = re.sub(r" +", " ", text)
    text = text.strip()

    # --- 4. Chunking ---
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_text(text)
    total_chunks = len(chunks)

    # --- 5. Build result records ---
    results = []
    for i, chunk in enumerate(chunks):
        words = re.findall(r"\b\w+\b", chunk)
        n_words = len(words)

        relative_position = i / (total_chunks - 1) if total_chunks > 1 else 0.0
        preview = chunk[:160].replace("\n", " ")

        results.append({
            "book_id": book_id,
            "chunk_id": i,
            "total_chunks": total_chunks,
            "relative_position": relative_position,
            "text": chunk,
            "chunk_length": len(chunk),
            "n_chars": len(chunk),
            "n_words": n_words,
            "preview": preview,
        })

    return results


def main():
    args = parse_args()

    book_paths = sorted(args.data_dir.glob("*.txt"))
    if not book_paths:
        raise RuntimeError(f"No .txt files found in {args.data_dir}")

    print("Found books:")
    for p in book_paths:
        print(f" - {p.name} ({p.stat().st_size} bytes)")

    book_ids = [book_id_from_path(p) for p in book_paths]
    print("\nBook IDs:", book_ids)
    print(f"\nLocal workers: {args.workers}")

    corpus = []
    with cf.ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for path in book_paths:
            book_id = book_id_from_path(path)
            fut = executor.submit(clean_and_chunk_book, str(path), book_id)
            futures[fut] = {"book_id": book_id, "path": str(path), "file_size": path.stat().st_size}

        total_tasks = len(futures)
        print(f"\nSubmitted {total_tasks} local chunking tasks")

        completed = 0
        for fut in cf.as_completed(futures):
            completed += 1
            meta = futures[fut]
            book_id = meta["book_id"]

            try:
                book_chunks = fut.result()
                corpus.extend(book_chunks)
                print(f"[{completed}/{total_tasks}] \u2713 book {book_id} -> {len(book_chunks)} chunks")
            except Exception as e:
                print(f"[{completed}/{total_tasks}] \u2717 book {book_id} FAILED: {e}")

    print("\nAll tasks done.")
    print(f"Total chunks collected: {len(corpus)}")

    # ---- Save corpus + stats -------------------------------------------
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    print(f"\n\u2713 Saved {len(corpus)} chunks to {args.output}")

    book_counts = Counter(c["book_id"] for c in corpus)
    print("\nChunks per book:")
    for b, cnt in sorted(book_counts.items()):
        print(f"  {b}: {cnt} chunks")

    chunk_lengths = [c["chunk_length"] for c in corpus]
    if chunk_lengths:
        print("\nChunk length stats:")
        print(f"  min: {min(chunk_lengths)}")
        print(f"  max: {max(chunk_lengths)}")
        print(f"  avg: {sum(chunk_lengths) / len(chunk_lengths):.1f}")


if __name__ == "__main__":
    main()
