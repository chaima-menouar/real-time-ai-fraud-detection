import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import BASE_MODEL, LABEL_COLUMN, MAX_LENGTH, RANDOM_SEED, TEXT_COLUMN


def metrics(prediction) -> dict[str, float]:
    predicted = np.argmax(prediction.predictions, axis=-1)
    return {
        "accuracy": accuracy_score(prediction.label_ids, predicted),
        "macro_f1": f1_score(prediction.label_ids, predicted, average="macro"),
        "weighted_f1": f1_score(prediction.label_ids, predicted, average="weighted"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune XLM-RoBERTa from a trusted base model")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-model", default=BASE_MODEL)
    parser.add_argument("--epochs", type=int, default=4)
    args = parser.parse_args()

    train_frame = pd.read_csv(args.data_dir / "train.csv")
    validation_frame = pd.read_csv(args.data_dir / "validation.csv")
    encoder = LabelEncoder().fit(train_frame[LABEL_COLUMN])

    unseen = set(validation_frame[LABEL_COLUMN]) - set(encoder.classes_)
    if unseen:
        raise ValueError(f"Validation contains labels missing from train: {sorted(unseen)}")

    tokenizer = AutoTokenizer.from_pretrained(args.base_model)

    def build_dataset(frame: pd.DataFrame) -> Dataset:
        encoded = frame.copy()
        encoded["labels"] = encoder.transform(encoded[LABEL_COLUMN])
        dataset = Dataset.from_pandas(encoded[[TEXT_COLUMN, "labels"]], preserve_index=False)
        return dataset.map(
            lambda batch: tokenizer(batch[TEXT_COLUMN], truncation=True, max_length=MAX_LENGTH),
            batched=True,
            remove_columns=[TEXT_COLUMN],
        )

    train_data = build_dataset(train_frame)
    validation_data = build_dataset(validation_frame)
    id_to_label = {index: label for index, label in enumerate(encoder.classes_.tolist())}
    model = AutoModelForSequenceClassification.from_pretrained(
        args.base_model,
        num_labels=len(id_to_label),
        id2label=id_to_label,
        label2id={label: index for index, label in id_to_label.items()},
    )
    training_args = TrainingArguments(
        output_dir=str(args.output_dir / "checkpoints"),
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=args.epochs,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        save_total_limit=2,
        seed=RANDOM_SEED,
        report_to="none",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=validation_data,
        processing_class=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
    )
    trainer.train()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))
    (args.output_dir / "label_mapping.json").write_text(
        json.dumps(id_to_label, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.output_dir / "training_metadata.json").write_text(
        json.dumps({"base_model": args.base_model, "seed": RANDOM_SEED}, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
