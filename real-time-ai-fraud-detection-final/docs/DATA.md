# Data and privacy

The dataset is not included in this public repository. It contains user-generated language and may include personal or unsafe content.

Before training, the preparation script:

1. validates the required `text` and `label` columns;
2. normalizes whitespace and redacts URLs, email addresses, and phone numbers;
3. removes empty and exact duplicate texts;
4. drops identical texts carrying conflicting labels;
5. assigns normalized-text groups to only one split.

The split is deterministic and group-aware, but it cannot eliminate every source or temporal bias. Dataset origin, collection consent, class definitions, and demographic coverage must be documented before real-world use.
