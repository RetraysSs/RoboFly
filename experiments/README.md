# experiments/

One script (or notebook) per experiment, named after the version and topic, for example `v0_1_single_neuron.py`.

Rules:

- Every figure in the README or report must be regenerable by a script in this folder.
- Scripts write outputs to `results/` (gitignored); commit the figures you reference in docs explicitly under `docs/figures/`.
- Fix random seeds and record parameters at the top of each script.
