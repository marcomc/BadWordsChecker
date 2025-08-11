import logging
from collections import Counter
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def generate_per_file_report(
    mp3_path: Path, matches: Counter, output_dir: Path
) -> None:
    """Generates a report for a single file."""
    if not matches:
        return

    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"{mp3_path.name}.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"File: {mp3_path.name}\n")
        f.write(f"Total bad words: {sum(matches.values())}\n")
        f.write("--------------------------------\n")
        for word, count in sorted(matches.items()):
            f.write(f"{word}: {count}\n")
    logger.info(f"Generated per-file report for {mp3_path.name} at {report_path}")


def generate_aggregated_report(
    all_matches: Dict[str, Counter], output_dir: Path, total_files: int
) -> None:
    """Generates an aggregated report of all bad words found."""
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "parolacce.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Bad Words Summary\n")
        f.write("=================\n")
        f.write(f"Total files scanned: {total_files}\n")
        f.write(f"Files with bad words: {len(all_matches)}\n\n")

        if not all_matches:
            f.write("No bad words found.\n")
            return

        aggregated_counts = Counter()
        for file_matches in all_matches.values():
            aggregated_counts.update(file_matches)

        word_to_files: Dict[str, List[str]] = {}
        for word in aggregated_counts:
            word_to_files[word] = []
            for filename, matches in all_matches.items():
                if word in matches:
                    word_to_files[word].append(filename)

        # Sort words by frequency (descending) and then alphabetically (ascending)
        sorted_words = sorted(
            aggregated_counts.items(), key=lambda item: (-item[1], item[0])
        )

        f.write("{:<20} | {:<12} | {}\n".format("Word", "Total Count", "Files"))
        f.write("-" * 60 + "\n")
        for word, count in sorted_words:
            files_str = ", ".join(sorted(word_to_files[word]))
            f.write(f"{word:<20} | {count:<12} | {files_str}\n")

    logger.info(f"Generated aggregated report at {report_path}")
