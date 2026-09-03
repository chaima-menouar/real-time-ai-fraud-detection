import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import LABEL_COLUMN, MAX_LENGTH, TEXT_COLUMN


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained classifier without exporting raw text")
    parser.add_argument("--data-file", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir or args.model_dir / "evaluation"
    output_dir.mkdir(parents=True, exist_ok=True)

    frame = pd.read_csv(args.data_file)
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir, local_files_only=True)
    model.eval()
    labels = [str(model.config.id2label[index]) for index in range(model.config.num_labels)]
    label_to_id = {label: index for index, label in enumerate(labels)}
    unknown = set(frame[LABEL_COLUMN]) - set(label_to_id)
    if unknown:
        raise ValueError(f"Test set contains unknown labels: {sorted(unknown)}")

    predictions: list[int] = []
    for start in range(0, len(frame), 32):
        batch = frame[TEXT_COLUMN].iloc[start : start + 32].astype(str).tolist()
        inputs = tokenizer(batch, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
        with torch.inference_mode():
            predictions.extend(model(**inputs).logits.argmax(dim=-1).tolist())

    truth = [label_to_id[label] for label in frame[LABEL_COLUMN]]
    summary = {
        "examples": len(frame),
        "accuracy": accuracy_score(truth, predictions),
        "macro_f1": f1_score(truth, predictions, average="macro"),
        "weighted_f1": f1_score(truth, predictions, average="weighted"),
        "per_class": classification_report(truth, predictions, target_names=labels, output_dict=True, zero_division=0),
    }
    (output_dir / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pd.DataFrame(confusion_matrix(truth, predictions), index=labels, columns=labels).to_csv(
        output_dir / "confusion_matrix.csv"
    )
    print(f"Wrote aggregate metrics to {output_dir}; no raw predictions were saved")


if __name__ == "__main__":
    main()
