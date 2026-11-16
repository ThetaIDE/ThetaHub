# Package format v3 release — 2026-11-16

34 packages move to package format v3 (`storage_version: 3`), import host code only
from the Theta SDK and declare compatibility on their capabilities. Optuna and Slurm,
extracted from the IDE as optional components, are listed as separate packages. These
releases require an IDE with Theta SDK 3.1 (execution contract v1, scheduler contract v2);
older IDEs cannot install them.

- Profiles are declared by selector (`model/nsfr.yaml`) and resolve from the installed
  package; installs never write workspace configuration.
- Packages share code through declared manifest `exports` instead of importing each
  other's files. NSFR exports `resolve_ruleset` and declares the `rules` workspace
  resource; NEUMANN and BlendRL use them.
- Compatibility is a capability's `requires` rules (paradigm, selected kinds, provided
  contracts, configuration values) and `provides` contracts. Package/profile `paradigms`,
  `compatible_paradigms`, execution `input_types` and `get_supported_paradigms` are gone.
- `sb3-suite` and `d3rlpy-suite` 2.1.0 are algorithm capabilities for execution contract v1:
  no script `entrypoint`, no bare aliases (`ppo`, `cql`, ...), `d3rlpy/vector` as the
  d3rlpy encoder model.
- BlendRL 1.4.0 selects its symbolic state builder as the model parameter `symbolic_state`
  (a data module providing `symbolic_state/v1`).
- Slurm 2.0.0 implements scheduler contract v2; Optuna 1.2.0 is the `theta_sweeper` tuner.
- The MuJoCo env profiles moved from `robotics` to `robotics-mujoco`.
- Registry entries list only the current release: storage-v2 archives cannot be installed by
  a storage-v3 IDE. Published archives remain in `packages/`.

Removed from the feed (manifests in `retired/registry/`): `ai_assistant`, `theta_mcp`, and
the MIMIC packages `mimic`, `mimic-env`, `mimic-early-prediction`, `reward-shaping` and
`mimic-clinical-suite`.

| Package | Previous current | v3 release |
| --- | --- | --- |
| clinical-timeseries-data | 1.0.1 | 1.2.0 |
| image-data | 1.0.1 | 1.2.0 |
| replay-buffer | 1.0.1 | 1.2.0 |
| tabular-data | 1.0.1 | 1.2.0 |
| atari-env | 1.0.1 | 1.2.0 |
| doom-env | 1.0.2 | 1.2.0 |
| gym_classic_control | 1.0.4 | 1.2.0 |
| mnist | 1.0.1 | 1.2.0 |
| robotics-mujoco | 1.0.2 | 1.2.0 |
| robotics | 1.0.2 | 1.2.0 |
| d3rlpy-suite | 1.0.3 | 2.1.0 |
| sb3-suite | 1.1.1 | 2.1.0 |
| autoencoder | 1.0.1 | 1.2.0 |
| blendrl | 1.2.1 | 1.4.0 |
| cew | 1.0.1 | 1.1.1 |
| dnn | 1.1.1 | 1.2.0 |
| dueling_resnet | 1.0.1 | 1.1.0 |
| lstm | 1.0.1 | 1.2.0 |
| mlp | 1.0.2 | 1.2.0 |
| nature_cnn | 1.0.1 | 1.1.0 |
| neumann | 1.0.7 | 1.1.1 |
| nsfr | 1.0.7 | 1.2.0 |
| transformer | 1.0.1 | 1.2.0 |
| slurm | — | 2.0.0 |
| standard-figures | 1.0.1 | 1.2.0 |
| antigravity | 1.0.1 | 1.2.0 |
| doom-sim | 1.0.1 | 1.2.0 |
| obsidian-notes | 1.0.1 | 1.2.0 |
| basic_suite | 1.0.1 | 1.1.0 |
| dl_basics_suite | 1.0.1 | 1.1.0 |
| robotics_suite | 1.0.2 | 1.1.0 |
| theta-validation-suite | 1.1.1 | 1.3.0 |
| thetalib | 1.0.2 | 1.2.0 |
| optuna | 1.1.1 | 1.2.0 |

Validation: the maintained-source integration suite (`tests/test_native_integration.py`)
passed against the matching IDE, including every provider import, real SB3 (DNN and
BlendRL) and d3rlpy workers, checkpoint reloads, editable copies, an Optuna trial with
checkpoint promotion, objective and replicate workers, and the app plugins.
`validate_manifest.py --check-archives` passes for every release entry, and each archive is
the builder's output for the tagged source. An installed IDE distribution reads this feed
cleanly (`verify_installed_distribution.py --hub-root`). Atari/MuJoCo runtime assets and
interactive DOOM/Antigravity services are not exercised by these headless checks.
