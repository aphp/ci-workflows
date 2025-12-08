# APHP CI GitHub Reusable Workflows

This repository hosts a collection of **reusable GitHub Actions workflows** for AP‑HP projects.

The goal is to **centralize CI/CD best practices** (linting, security scans, packaging and publishing) so that each project can:

- reuse the same, opinionated workflows,
- get consistent quality and security checks,
- keep CI configuration as small as possible.

Current workflows mainly target:

- **Container images** (build, scan and push to GHCR),
- **Helm charts** (lint, test, secure, document and publish).

---

## Table of contents

- [Overview](#overview)
- [Available reusable workflows](#available-reusable-workflows)
  - [Container Images workflow](#container-images-workflow)
  - [Helm Charts workflow](#helm-charts-workflow)
- [How to call a reusable workflow](#how-to-call-a-reusable-workflow)
- [Branching, versions and environments](#branching-versions-and-environments)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

All workflows are stored under:

```text
.github/workflows/
```

You **do not copy** these YAML files into your own repositories.  
Instead, your project **calls them as reusable workflows** using the `uses:` syntax described in the GitHub Actions documentation.

This repository is meant to be used across all AP‑HP GitHub projects that need a **standard CI pipeline** for:

- building and scanning Docker images,
- validating, scanning and releasing Helm charts.

---

## Available reusable workflows

Below is an overview of the main families of workflows currently documented.

### Container Images workflow

#### Description

Provides **security and quality checks** for container images before pushing them to your project’s **GitHub Container Registry (GHCR)**.

Typical use cases:

- container images for applications (e.g. APIs, frontends, backends),
- base or runtime images (e.g. Jupyter EDS notebooks images),
- internal utilities or tools.

#### Tools

The workflow chains several tools:

- **Hadolint**
  - Linting of `Dockerfile` (style, best practices, common pitfalls).
- **Buildx**
  - Docker image build (supports advanced features like build kits, multi‑arch, extra build args…).
- **Dockle**
  - Image scan for misconfigurations and bad patterns.
- **Trivy**
  - Vulnerability scanning of images.
  - License scanning of included dependencies.
- **Docker / GHCR**
  - Push of validated images to your project’s GHCR repository.

#### Reports

All tools that support it produce **SARIF reports**, automatically uploaded to your repository:

- GitHub UI: `Security` tab → `Code scanning` section.
- You can browse findings by tool, severity, and impacted files.

#### Prerequisites

- Works **out of the box for public repositories**.
- For **private repositories**, you may need to:
  - adjust **Actions permissions** so the workflow can push to your private GHCR,
  - ensure the workflow can **write packages** (GHCR).

> The exact permission model may depend on your organization policies; coordinate with your AP‑HP GitHub admins if needed.

#### Inputs

Inputs currently supported by the container images workflow:

| Input                      | Type   | Required | Default            | Description |
|---------------------------:|:------:|:--------:|:------------------:|-------------|
| `dockerfile-path`         | string | No       | `Dockerfile`       | Path to the Dockerfile of your project. |
| `hadolint-ignore`         | string | No       | `""`               | Comma‑separated list of **Hadolint rule IDs** to ignore in **blocking** checks. Findings still appear in reports. |
| `image-name`              | string | **Yes**  | –                  | Full image name including registry and repository, e.g. `ghcr.io/aphp/my-service`. |
| `image-custom-tag`        | string | No       | `""`               | Custom tag added **in addition** to automatically generated tags. Typical values: `x86_64-ubuntu-24.04`, `x86_64-ubuntu-24.04-dev`, `nightly`. |
| `extra-build-args`        | string | No       | `""`               | Extra Docker build arguments, provided as `KEY=VALUE`. Usually passed as a multiline YAML scalar (one `KEY=VALUE` per line). |
| `dockle-ignore`           | string | No       | `""`               | Comma‑separated list of **Dockle rule IDs** to ignore in **blocking** checks. |
| `dockle-accept-file`      | string | No       | `""`               | Comma‑separated list of file names to accept in Dockle (`--accept-file`). |
| `dockle-accept-key`       | string | No       | `""`               | Comma‑separated list of keys to accept in Dockle (`--accept-key`). |
| `trivy-ignore-vuln-ids`   | string | No       | `""`               | List of vulnerability IDs (`CVE-…`, `GHSA-…`, `AVD-…`) to ignore for **blocking** Trivy checks. Can be comma‑separated or one per line. |
| `trivy-ignore-license-ids`| string | No       | `""`               | List of license identifiers (e.g. `GPL-3.0-only`, `MIT`) to ignore in **blocking** Trivy license checks. Can be comma‑separated or one per line. |

Always refer to the workflow file in `.github/workflows/` for the most up‑to‑date list of inputs and defaults.

#### Release management

The workflow relies on a combination of actions and steps to handle **image tagging and publishing**:

- During the build step, tags are computed according to **Docker Metadata Action** rules.
- If all scans pass successfully:
  - the previously tagged image is pushed to your project’s GHCR repository.

This behavior directly impacts your **release and tagging strategy**; make sure to align it with your project’s lifecycle (branching model, tags, environments).

---

### Helm Charts workflow

#### Description

Provides **security and quality checks for Helm charts**, and automates **publishing** to a Helm repository hosted via your project’s GitHub Pages (`gh-pages` branch).

Typical use cases:

- Helm charts for applications like **HELIX**, **REDCap**, etc.,
- any Kubernetes deployment managed via Helm within AP‑HP projects.

#### Tools

The Helm charts workflow is organized by job:

- **Linting (`lint-test` job)**
  - `ct lint` (Helm chart-testing),
  - `kubeconform` (Kubernetes manifest validation against schemas).

- **Security (`lint-test` job)**
  - **Polaris** (configuration and security best practices),
  - **Trivy** (vulnerability scanning on rendered manifests).

- **Documentation (`generate-doc` job)**
  - **helm-docs** (README / values documentation from chart),
  - **Values schema JSON** generation (for validation and tooling).

- **Publishing (`release` job)**
  - **helm/chart-releaser** to package charts and update the Helm index.

#### Reports

Some tools (currently **Trivy**) generate **SARIF reports**, uploaded to:

- `Security` tab → `Code scanning`.

This allows you to track vulnerabilities and security issues directly in GitHub.

#### Prerequisites

To be able to **publish charts** and use the repository as a **Helm repository**, ensure:

1. A branch named `gh-pages` exists in your repository.
2. In your repository **Settings**:
   - `Code and automation / Pages` → `Branch`: select `gh-pages`.
3. In **Settings → Actions → General**:
   - `Actions permissions`: set to **Allow all actions and reusable workflows**.
   - `Workflow permissions`: set to **Read and write permissions**.
4. Your chart lives under a `charts` directory at the repository root:

   ```text
   charts/
     mychart/
       Chart.yaml
       values.yaml
       templates/...
   ```

#### Inputs

Inputs currently supported by the Helm charts workflow:

| Input               | Type   | Required | Default               | Description |
|--------------------:|:------:|:--------:|:---------------------:|-------------|
| `chart-dir`        | string | **Yes**  | `chart`               | Directory containing your Helm chart (must contain a `Chart.yaml`). |
| `chart-values`     | string | No       | `chart/values.yaml`   | Values file used for `kubeconform`, Polaris, Trivy and `ct install` tests. |
| `kubernetes-version`| string| No       | `1.24.2`              | Target Kubernetes version used by kubeconform and Trivy for validations and scans. |

Again, always check the workflow file in `.github/workflows/` for the authoritative list of inputs.

#### Release management

Chart releases are handled via the **Helm CR action**, with behavior depending on the branch:

- On **`dev` branch**:
  - Chart version in `Chart.yaml` is suffixed with `-dev`,
  - A Git tag is created with this dev version,
  - A **Release** is created containing the dev chart archive,
  - `index.yaml` in the `gh-pages` branch is updated to reference the new **dev** chart.

- On **`main` branch**:
  - A Git tag is created with the chart version from `Chart.yaml`,
  - A **Release** is created with the chart archive, marked as **latest**,
  - `index.yaml` in `gh-pages` is updated to reference the new **stable** chart.

This gives you a standard separation between **dev** and **stable** releases for Helm charts.

---

## How to call a reusable workflow

To use one of these workflows from another repository:

1. Create a workflow file in your project, e.g.:

   ```text
   .github/workflows/container-ci.yml
   ```

2. In that file, define a job that **uses** one of the workflows from this repo:

   ```yaml
   name: Container CI

   on:
     push:
       branches: [ main, dev ]
     pull_request:

  permissions:
    contents: write
    security-events: write

   jobs:
     container-ci:
       uses: aphp/ci-workflows/.github/workflows/<container-workflow-filename>.yml@dev
       with:
         image-name: ghcr.io/aphp/my-service
         dockerfile-path: Dockerfile
         image-custom-tag: x86_64-ubuntu-24.04
   ```

3. For Helm charts, a similar pattern applies:

   ```yaml
   name: Helm Chart CI

   on:
     push:
       branches: [ main, dev ]
     pull_request:

  permissions:
    contents: write
    security-events: write

   jobs:
     helm-ci:
       uses: aphp/ci-workflows/.github/workflows/<helm-workflow-filename>.yml@dev
       with:
         chart-dir: charts/mychart
         chart-values: charts/mychart/values.yaml
         kubernetes-version: "1.24.2"
   ```

> Replace `<container-workflow-filename>.yml` and `<helm-workflow-filename>.yml` with the actual filenames from this repository’s `.github/workflows` directory.

For a concrete example of usage, you can refer to a project CI configuration that calls these workflows (e.g. container image or Helm chart repositories within the AP‑HP GitHub organization).

---

## Branching, versions and environments

This repository is versioned like any other Git repository:

- **Branches** such as `dev` or `main` represent the maturity of workflows.
- In your consuming projects, you should:
  - Prefer **tags** (once defined) for stable usage, e.g. `@v1`,
  - Use the `dev` branch (`@dev`) when experimenting or adopting new features early.

Examples:

- Stable usage (recommended when available):

  ```yaml
  uses: aphp/ci-workflows/.github/workflows/<workflow>.yml@v1
  ```

- Development usage (bleeding edge):

  ```yaml
  uses: aphp/ci-workflows/.github/workflows/<workflow>.yml@dev
  ```

Coordinate with the AP‑HP CI maintainers to know which refs are recommended for production usage.

---

## Contributing

Contributions, bug reports and improvement ideas are welcome.

- See [`CONTRIBUTING.md`](CONTRIBUTING.md) for:
  - coding standards,
  - how to run tests/linters locally,
  - the release workflow for this repository.
- Use **GitHub Issues** to:
  - report problems with existing workflows,
  - request new reusable workflows,
  - ask for documentation improvements.

Before opening a pull request:

1. Check there is an existing issue (or open a new one) describing the change.
2. Update or add documentation for new inputs/behavior.
3. Run relevant tests or dry‑runs for the workflows you modify.

---

## License

This project is licensed under the **Apache License 2.0**.

- See [`LICENSE`](LICENSE) for details.

By contributing to this repository, you agree that your contributions will be licensed under the same terms.
