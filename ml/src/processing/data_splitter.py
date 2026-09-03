from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from src.config import LABEL_COLUMN, RANDOM_SEED, TEXT_COLUMN
from src.processing.text_cleaner import clean_text, normalized_group_id


def clean_dataframe(frame: pd.DataFrame) -> pd.DataFrame:
    missing = {TEXT_COLUMN, LABEL_COLUMN} - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    cleaned = frame[[TEXT_COLUMN, LABEL_COLUMN]].copy()
    cleaned[TEXT_COLUMN] = cleaned[TEXT_COLUMN].map(clean_text)
    cleaned[LABEL_COLUMN] = cleaned[LABEL_COLUMN].astype(str).str.strip().str.lower()
    cleaned = cleaned[(cleaned[TEXT_COLUMN].str.len() >= 3) & cleaned[LABEL_COLUMN].ne("")]
    cleaned["group_id"] = cleaned[TEXT_COLUMN].map(normalized_group_id)

    label_counts = cleaned.groupby("group_id")[LABEL_COLUMN].nunique()
    conflicting = label_counts[label_counts > 1].index
    cleaned = cleaned[~cleaned["group_id"].isin(conflicting)]
    return cleaned.drop_duplicates(subset=["group_id"], keep="first").reset_index(drop=True)


def split_dataframe(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if len(frame) < 10:
        raise ValueError("At least 10 cleaned examples are required for a three-way split")

    first = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=RANDOM_SEED)
    train_idx, temporary_idx = next(first.split(frame, groups=frame["group_id"]))
    train = frame.iloc[train_idx]
    temporary = frame.iloc[temporary_idx]

    second = GroupShuffleSplit(n_splits=1, test_size=0.50, random_state=RANDOM_SEED)
    validation_idx, test_idx = next(
        second.split(temporary, groups=temporary["group_id"])
    )
    validation = temporary.iloc[validation_idx]
    test = temporary.iloc[test_idx]
    return tuple(part.drop(columns="group_id").reset_index(drop=True) for part in (train, validation, test))


def save_splits(frame: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, split in zip(("train", "validation", "test"), split_dataframe(frame)):
        split.to_csv(output_dir / f"{name}.csv", index=False)
