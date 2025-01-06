# Helm Charts CI GitHub Workflow

## Presentation

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


## Prerequisites

If you want to publish your chart as an artefact in your Github project, and for it to be retrieved as a Chart by Helm, you must follow these steps : 
- Create a branch names `gh-pages` in your repository
- Set this branch as the Github Page branch in the github project's page, under the `Settings` tab -> `Code and automation/Pages` category, `Branch` section
- Set the correct permissions for Github Actions, under the `Settings` tab -> `Actions/General` category :
  - Set `Actions permissions` to `Allow all actions and reusable workflows`
  - Set `Workflow permissions` to `Read and write permissions`
- Place your Helm Chart under a `charts` directory in the root of your repository, and push your changes


## How to use

### Calling this workflow

To define a job that calls a reusable workflow, just read the [the corresponding documentation](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow).

### Inputs definition

This workflow's inputs are as follows : 
- `chart-dir`:
  - description: "Directory holding your Chart"
  - required: true
  - type: string 
  - default: "chart"
- `kubernetes-version`:
  - description: "Version of the target Kubernetes cluster the Chart will run on"
  - required: true
  - type: string 
  - default: "1.24.2"


## How to contribute?

We welcome any feedback and contributions. If you want to add your contribution to this component, you can fork this repository, open a PR with your changes, and ping a maintainer for us to have a look at it.

## How to raise bugs or issues?

You can open an Issue in the the Issue board of this project.