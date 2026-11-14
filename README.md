# Theta Community Hub

Official community registry for [ThetaIDE](https://github.com/CameronEgb/Theta-IDE) plugins, reinforcement learning algorithms, symbolic models, and benchmark environments.

---

## 🌟 How It Works

1. **Decentralized & Free ($0.00)**: Package archives are hosted directly on the author's own GitHub Releases.
2. **Automated CI Validation**: Pull requests are automatically verified by GitHub Actions against schema requirements and integrity hashes.
3. **Instant Global Distribution**: Manifests compile into a lightweight `index.json` published via GitHub Pages.

---

## 📦 Component Categories

| Category | Description |
|---|---|
| `plugin` | UI extensions, activity bar panels, telemetry tools |
| `method` | RL algorithms (PPO, CQL, SAC, hybrid agents) |
| `model` | Neural architectures and NeSy symbolic reasoners |
| `env` | Simulation wrappers and benchmark environments |
| `datamodule`, `evaluator`, `plotter` | Data loading, evaluation and figures |
| `experiment` | Pre-bundled benchmark configs and hyperparameter sweeps |
| `suite`, `package` | Dependency bundles and general packages |
| `tuner`, `scheduler` | Hyperparameter tuning and remote-site scheduling components |

ThetaIDE installs every package under `src/plugins/{components,app}/installed/<id>/`. A package's
config profiles stay inside it; users override them with files under `src/usr/config`.

Every listing uses the native package format: `storage_version: 3`, `api_version: 1`, explicit
`capabilities`, a `payload` of implementations, resources and configs, and config destinations
written as selectors relative to the config root (`model/my_model.yaml`). The registry entry
repeats these fields from the archive's `.theta_component.json`.

---

## 🚀 How to Submit a Component to the Hub

### Step 1: Package Your Release
1. In your GitHub repository, create a release tag (e.g. `v1.0.0`).
2. Attach a `.zip` archive containing your component source files as a Release Asset.
3. Compute the SHA-256 hash of your archive:
   ```bash
   # On macOS
   shasum -a 256 your-package.zip

   # On Linux
   sha256sum your-package.zip
   ```

### Step 2: Create Your Manifest
In this repository, add a new JSON file under `registry/<category>/<your-component-id>.json`.

**Example (`registry/plugins/my-awesome-tool.json`):**
```json
{
  "id": "my-awesome-tool",
  "name": "My Awesome Tool",
  "kind": "plugin",
  "version": "1.0.0",
  "description": "Interactive visualization and telemetry panel for ThetaIDE.",
  "author": {
    "name": "Your Name",
    "github": "your-username"
  },
  "repository": "https://github.com/your-username/my-awesome-tool",
  "license": "MIT",
  "tags": ["visualization", "telemetry"],
  "storage_version": 3,
  "api_version": 1,
  "capabilities": [{"id": "my-awesome-tool", "kind": "plugin", "entry_point": "__init__.py:MyAwesomeTool"}],
  "payload": {"implementations": ["__init__.py"], "resources": [], "configs": {}},
  "releases": {
    "1.0.0": {
      "tag": "v1.0.0",
      "url": "https://github.com/your-username/my-awesome-tool/releases/download/v1.0.0/package.zip",
      "sha256": "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a"
    }
  }
}
```

### Step 3: Test Locally
```bash
# Validate your manifest
python scripts/validate_manifest.py registry/plugins/my-awesome-tool.json

# Test index compilation
python scripts/build_index.py
```

### Step 4: Open a Pull Request
Submit a PR to `main`. Once GitHub Actions passes and the PR is merged, your component will be immediately available to all ThetaIDE users worldwide in the Community Hub!

---

## 🛠️ Repository Scripts

- `python scripts/validate_manifest.py`: Checks all manifests for schema conformity, package format 3 and config selectors; `--check-archives` also verifies each current archive's hash and embedded manifest.
- `python scripts/build_index.py`: Compiles manifests into `dist/index.json` and `dist/index.min.json`.
