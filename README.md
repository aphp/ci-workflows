# APHP CI GitHub Reusable Workflows

This directory holds the GitHub reusable workflows that you can import in your own project's CIs.

## Container Images

### Description

This component aims to provide with security and quality checks for container images, before pushing them on your project's GHCR (GitHub Container Registry).

### Tools

- Hadolint
  - Dockerfile linting

- Buildx
  - Docker Image build

- Dockle
  - Docker Image scan for misconfigurations and ba patterns

- Trivy
  - Docker Image scan for vulnerabilities
  - Docker Image scan for potential licensing issues

- Docker
  - Pushing Docker Image to the project's GHCR

### Reports 

All the tools used are generating SARIF reports that are uploaded to your Github project's dashboard. You can consult the reports entries of your project under the `Security` tab -> `Code scanning` category.


### Prerequisites

This workflow should work out-of-the-box for public projects. Execution on private projects is not supported for now, and may require some additional steps to set the correct permissions for the workflow being able to push the image in your private GHCR.  

### How to use

#### Calling this workflow

To define a job that calls a reusable workflow, just read the [the corresponding documentation](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow).

You can use the [redcap-containers project CIs](https://github.com/aphp/redcap-containers/tree/main/.github/workflows) as an example.

#### Inputs definition

This workflow's inputs are as follows : 
- `dockerfile-path`:
  - description: "Path to Dockerfile of your project"
  - required: false
  - type: string 
  - default: "Dockerfile"
- `image-name`:
  - description: "Image name, including tag"
  - required: true
  - type: string

#### Releases management

This workflow uses a blend of several actions and steps to handle the release process.

**This behavior could impact your lifecycle management practices, so be sure to read the lines below!**

The releases will be handled as follow, whenever you decide to call this workflow (when tagging, pushing, etc.):
- At build, you image will be tagged and version according to the [Docker Metadata Action](https://github.com/marketplace/actions/docker-metadata-action) rules (`build-image::Buildx - Image Build` step).
- If the scanning steps ends successfully, your previously tagged image will be pushed in the GHCR repository of your project (`push-docker-image::Push Image to GitHub Container Registry` step).


## Helm Charts

### Description

This component aims to provide with security and quality checks for Helm charts, before pushing them a repository hosted in your project's Github Page that can be used as a Helm Repository.

### Tools

- Linting (`lint-test` job)
  - Helm ct-lint
  - Kubeconform

- Security (`lint-test` job)
  - Polaris
  - Trivy

- Documentation (`generate-doc` job)
  - Helm Docs
  - Helm Values Schema JSON

- Publishing (`release` job)
  - Helm chart-releaser

### Reports 

A few tools (only Trivy at this time) are generating SARIF reports that are uploaded to your Github project's dashboard. You can consult the reports entries of your project under the `Security` tab -> `Code scanning` category.

### Prerequisites

If you want to publish your chart as an artefact in your Github project, and for it to be retrieved as a Chart by Helm, you must follow these steps : 
- Create a branch names `gh-pages` in your repository
- Set this branch as the Github Page branch in the github project's page, under the `Settings` tab -> `Code and automation/Pages` category, `Branch` section
- Set the correct permissions for Github Actions, under the `Settings` tab -> `Actions/General` category :
  - Set `Actions permissions` to `Allow all actions and reusable workflows`
  - Set `Workflow permissions` to `Read and write permissions`
- Place your Helm Chart under a `charts` directory in the root of your repository, and push your changes


### How to use

#### Calling this workflow

To define a job that calls a reusable workflow, just read the [the corresponding documentation](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow).

#### Inputs definition

This workflow's inputs are as follows : 
- `chart-dir`:
  - description: "Directory holding your Chart"
  - required: true
  - type: string 
  - default: "chart"
- `chart-values`:
  - description: "Chart values file that will be used for the testing and scanning steps"
  - required: false
  - type: string 
  - default: "chart/values.yaml"
- `kubernetes-version`:
  - description: "Version of the target Kubernetes cluster the Chart will run on"
  - required: true
  - type: string 
  - default: "1.24.2"

#### Releases management

This workflow uses [the Helm Cr Action](https://github.com/marketplace/actions/helm-chart-releaser) to release charts. 

**This behavior could impact your lifecycle management practices, so be sure to read the lines below!**

The releases will be handled as follow :

- `dev` branch : 
  - Update the Chart version Chart.yaml with the `-dev` suffix (`helm-chart-releaser::Add release suffix - DEV` step)
  - Create the tag with the Chart version (`helm-chart-releaser::Run chart-releaser - DEV` step)
  - Create the Release with the dev Chart archive as package (`helm-chart-releaser::Run chart-releaser - DEV` step)
  - Update the `index.yaml` file in the `gh-page` branch of your repo to include the reference to the new dev Chart (`helm-chart-releaser::Run chart-releaser - DEV` step)
- `main` branch : 
  - Create the tag with the Chart version (`helm-chart-releaser::Run chart-releaser - MAIN` step)
  - Create the Release with the Chart archive as package, and mark this release as `latest` (`helm-chart-releaser::Run chart-releaser - MAIN` step)
  - Update the `index.yaml` file in the `gh-page` branch of your repo to include the reference to the new Chart (`helm-chart-releaser::Run chart-releaser - MAIN` step)