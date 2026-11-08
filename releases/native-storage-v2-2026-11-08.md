# Native package release — 2026-11-08

All 37 maintained components now declare the native storage-v2/API-1 contract.
These releases require the IDE native package loader and installer. Existing release archives remain unchanged.

Packages explicitly declare capabilities, implementations, resources, config destinations and dependencies.
Suites install independently owned dependencies; Thetalib is now a suite. NSFR owns shared symbolic rules.
Registry validation and deployment verify current archive hashes and embedded manifests.

The four unmaintained Pyrenees records moved to `retired/registry`; their historical archives are preserved.

| Package | Previous current | Native release |
| --- | --- | --- |
| clinical-timeseries-data | 1.0.0 | 1.0.1 |
| image-data | 1.0.0 | 1.0.1 |
| replay-buffer | 1.0.0 | 1.0.1 |
| tabular-data | 1.0.0 | 1.0.1 |
| atari-env | 1.0.0 | 1.0.1 |
| doom-env | 1.0.1 | 1.0.2 |
| gym_classic_control | 1.0.3 | 1.0.4 |
| mimic-env | 1.0.1 | 1.0.2 |
| mnist | 1.0.0 | 1.0.1 |
| robotics-mujoco | 1.0.1 | 1.0.2 |
| mimic-early-prediction | 1.0.1 | 1.0.2 |
| reward-shaping | 1.0.0 | 1.0.1 |
| mimic | 1.0.1 | 1.0.2 |
| robotics | 1.0.1 | 1.0.2 |
| d3rlpy-suite | 1.0.2 | 1.0.3 |
| sb3-suite | 1.1.0 | 1.1.1 |
| autoencoder | 1.0.0 | 1.0.1 |
| blendrl | 1.2.0 | 1.2.1 |
| cew | 1.0.0 | 1.0.1 |
| dnn | 1.1.0 | 1.1.1 |
| dueling_resnet | 1.0.0 | 1.0.1 |
| lstm | 1.0.0 | 1.0.1 |
| mlp | 1.0.1 | 1.0.2 |
| nature_cnn | 1.0.0 | 1.0.1 |
| neumann | 1.0.5 | 1.0.7 |
| nsfr | 1.0.5 | 1.0.7 |
| transformer | 1.0.0 | 1.0.1 |
| mimic-clinical-suite | 1.0.0 | 1.0.1 |
| standard-figures | 1.0.0 | 1.0.1 |
| antigravity | 0.1.5 | 1.0.1 |
| doom-sim | 0.1.0 | 1.0.1 |
| obsidian-notes | 0.1.0 | 1.0.1 |
| basic_suite | 1.0.0 | 1.0.1 |
| dl_basics_suite | 1.0.0 | 1.0.1 |
| robotics_suite | 1.0.1 | 1.0.2 |
| theta-validation-suite | 1.1.0 | 1.1.1 |
| thetalib | 1.0.1 | 1.0.2 |

Validation: all 57 maintained-source integration tests passed, including all provider imports, real SB3/DNN and SB3/BlendRL workers, checkpoint reloads, editable copies, objective/tuner workers and app plugins.
Native manifest, dependency, archive identity/hash, generated feed and client installation checks cover all 37 release artifacts.
Full MIMIC training needs external datasets; Atari/MuJoCo runtime assets and interactive DOOM/Antigravity services are not exercised by these headless checks.
