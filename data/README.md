# data/

Connectome files are **not committed** (see `.gitignore`). Download them yourself so the original sources and licences apply.

## Where to get the data

- FlyWire Codex download portal: https://codex.flywire.ai/ (look for the data download page; a Google login may be required).
- The reference model repositories ship the neuron list and connectivity tables for FlyWire public release 783, which is what the Shiu et al. model uses:
  - https://github.com/philshiu/Drosophila_brain_model
  - https://github.com/eonsystemspbc/fly-brain

At the time of writing, the Eon repo lists files named like `2025_Completeness_783.csv` (neuron list) and `2025_Connectivity_783.parquet` (synapse connectivity). File names and column layout can change; check the source repo before writing a loader.

## Layout (suggested)

```
data/
  raw/        files exactly as downloaded
  processed/  your own derived files (sparse matrices, subsets)
```

## Attribution

When you publish results, cite Dorkenwald et al. 2024 and Schlegel et al. 2024 (see the main README).
