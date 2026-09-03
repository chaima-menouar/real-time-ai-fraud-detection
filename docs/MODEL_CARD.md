# Model card

## Intended use

Research and classroom demonstration of multilingual suspicious-comment classification in an e-learning context. Predictions support a human reviewer; they do not make disciplinary decisions.

## Model

XLM-RoBERTa multiclass sequence classification. The API preserves the model's predicted category and maps every non-normal class to `risk=true`. The exact historical class names must be recovered from the private training metadata; this repository does not invent a replacement mapping.

## Historical evaluation

- accuracy: 0.926963
- weighted F1: 0.938208
- macro F1: 0.825518
- examples: 76,605

Only aggregate results are published. Because the dataset and matching weights are private, these values should be treated as a historical experiment rather than a reproducible benchmark.

## Limitations

- class imbalance is visible in the gap between weighted and macro F1;
- dialect, sarcasm, spelling variation, code-switching, and domain shift can reduce accuracy;
- confidence is a softmax score, not a guarantee and not necessarily calibrated;
- duplicate-aware splitting reduces one leakage path but does not prove source independence;
- performance must be measured per class and language before deployment;
- false positives can unfairly affect learners, so human review and an appeal process are required.
