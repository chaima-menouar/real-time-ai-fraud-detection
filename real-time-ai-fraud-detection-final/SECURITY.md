# Security policy

This repository is an academic demonstration and is not approved for processing real learner or financial data.

## Reporting

Do not open a public issue containing credentials, personal information, malicious payloads, or private dataset samples. Contact the maintainer privately through the profile contact channel and include only the minimum information needed to reproduce the problem.

## Safe defaults

- model failures return `503` and never fall back to a guessed result;
- raw comments are not written to application logs;
- WebSocket origins are configurable and are not open to every website;
- H2 Console is disabled;
- secrets, datasets, predictions, checkpoints, and model weights are ignored by Git.
