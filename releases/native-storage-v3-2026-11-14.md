# Package format v3 release — 2026-11-14

All 37 maintained packages move to package format v3 (`storage_version: 3`) and import
host code only from the Theta SDK. Optuna and Slurm, extracted from the IDE as optional
components, are listed for the first time. These releases require an IDE that reads
storage-v3 packages (SDK 2.2, execution contract v1); older IDEs cannot install them.

- Profiles are declared by selector (`model/nsfr.yaml`) and resolve from the installed
  package; installs never write workspace configuration.
- Packages share code through declared manifest `exports` (NSFR, NEUMANN, NatureCNN,
  MIMIC early prediction, Gym classic control) instead of importing each other's files.
- `sb3-suite` and `d3rlpy-suite` 2.0.0 are algorithm capabilities for execution contract v1:
  no script `entrypoint`, no bare aliases (`ppo`, `cql`, ...), and `d3rlpy/vector` as the
  d3rlpy encoder model. See their release notes in the package sources.
- The MuJoCo env profiles moved from `robotics` to `robotics-mujoco`, the env provider
  that declares those selectors.
- Registry entries list only the current release: storage-v2 archives cannot be installed by
  a storage-v3 IDE. Earlier archives remain in `packages/`.

`ai_assistant` and `theta_mcp` are unchanged (storage v2) and are not part of this release.

| Package | Previous current | v3 release |
| --- | --- | --- |
| clinical-timeseries-data | 1.0.1 | 1.1.0 |
| image-data | 1.0.1 | 1.1.0 |
| replay-buffer | 1.0.1 | 1.1.0 |
| tabular-data | 1.0.1 | 1.1.0 |
| atari-env | 1.0.1 | 1.1.0 |
| doom-env | 1.0.2 | 1.1.0 |
| gym_classic_control | 1.0.4 | 1.1.0 |
| mimic-env | 1.0.2 | 1.1.0 |
| mnist | 1.0.1 | 1.1.0 |
| robotics-mujoco | 1.0.2 | 1.1.0 |
| mimic-early-prediction | 1.0.2 | 1.1.0 |
| reward-shaping | 1.0.1 | 1.1.0 |
| mimic | 1.0.2 | 1.1.0 |
| robotics | 1.0.2 | 1.1.0 |
| d3rlpy-suite | 1.0.3 | 2.0.0 |
| sb3-suite | 1.1.1 | 2.0.0 |
| autoencoder | 1.0.1 | 1.1.0 |
| blendrl | 1.2.1 | 1.3.0 |
| cew | 1.0.1 | 1.1.0 |
| dnn | 1.1.1 | 1.2.0 |
| dueling_resnet | 1.0.1 | 1.1.0 |
| lstm | 1.0.1 | 1.1.0 |
| mlp | 1.0.2 | 1.1.0 |
| nature_cnn | 1.0.1 | 1.1.0 |
| neumann | 1.0.7 | 1.1.0 |
| nsfr | 1.0.7 | 1.1.0 |
| transformer | 1.0.1 | 1.1.0 |
| mimic-clinical-suite | 1.0.1 | 1.1.0 |
| standard-figures | 1.0.1 | 1.1.0 |
| antigravity | 1.0.1 | 1.1.0 |
| doom-sim | 1.0.1 | 1.1.0 |
| obsidian-notes | 1.0.1 | 1.1.0 |
| basic_suite | 1.0.1 | 1.1.0 |
| dl_basics_suite | 1.0.1 | 1.1.0 |
| robotics_suite | 1.0.2 | 1.1.0 |
| theta-validation-suite | 1.1.1 | 1.2.0 |
| thetalib | 1.0.2 | 1.1.0 |
| optuna | — | 1.1.0 |
| slurm | — | 1.1.0 |

Validation: all 57 maintained-source integration tests passed against the matching IDE,
including every provider import, real SB3 (DNN and BlendRL) and d3rlpy workers, checkpoint
reloads, editable copies, an Optuna trial with checkpoint promotion, objective and replicate
workers, and the app plugins. `validate_manifest.py --check-archives` passes for every
release entry, and each archive is byte-identical to a fresh local build.
Full MIMIC training needs external datasets; Atari/MuJoCo runtime assets and interactive
DOOM/Antigravity services are not exercised by these headless checks.
