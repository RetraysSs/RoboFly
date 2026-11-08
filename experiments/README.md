# experiments/

One script (or notebook) per experiment, named after the version and topic, for example `v0_1_single_neuron.py`.

Conventions:

- Every figure in the README or report must be regenerable by a script in this folder.
- Scripts write outputs to `results/` (gitignored); figures referenced in the docs are committed explicitly under `docs/figures/`.
- Fix random seeds and record parameters at the top of each script.
