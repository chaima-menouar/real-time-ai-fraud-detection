import pandas as pd

from src.processing.data_splitter import clean_dataframe, split_dataframe


def test_duplicates_and_conflicting_labels_do_not_cross_splits():
    rows = [{"text": f"unique example {index}", "label": "normal"} for index in range(20)]
    rows += [
        {"text": "duplicate content", "label": "spam"},
        {"text": " DUPLICATE   content ", "label": "spam"},
        {"text": "conflict", "label": "normal"},
        {"text": "conflict", "label": "spam"},
    ]
    cleaned = clean_dataframe(pd.DataFrame(rows))
    train, validation, test = split_dataframe(cleaned)
    combined = pd.concat([train, validation, test], ignore_index=True)
    assert combined["text"].str.casefold().duplicated().sum() == 0
    assert "conflict" not in combined["text"].tolist()
