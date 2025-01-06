# Helm Charts CI GitHub Workflow

## Presentation

### Description

This component aims to provide with security and quality checks for container images, before pushing them on your project's GHCR (GitHub Container Registry).

### Tools

- Linting (`lint-dockerfile` job)
  - Hadolint
  - Dockle

- Security (`scan-docker-image` job)
  - Trivy

- Publishing (`release` job)
  - Docker build-and-push

### Reports 

All the tools used are generating sarif reports that are uploaded y the workflow to your Github project's dashboard. You can consult the reports entries of your project under the `Security` tab -> `Code scanning` category.


## Prerequisites

This workflow should work out-of-the-box for public projects. Execution on private projects is not supported for now, and may require some additional steps to set the correct permissions for the workflow being able to push the image in your private GHCR.  

## How to use

### Calling this workflow

To define a job that calls a reusable workflow, just read the [the corresponding documentation](https://docs.github.com/en/actions/sharing-automations/reusing-workflows#calling-a-reusable-workflow).

### Inputs definition

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

## How to contribute?

We welcome any feedback and contributions. If you want to add your contribution to this component, you can fork this repository, open a PR with your changes, and ping a maintainer for us to have a look at it.

## How to raise bugs or issues?

You can open an Issue in the the Issue board of this project.