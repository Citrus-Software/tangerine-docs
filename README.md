# Tangerine Docs

<p align="center">
  <a href="https://citrus-software.github.io/tangerine-docs">
    <img src="https://img.shields.io/website?url=https%3A%2F%2Fcitrus-software.github.io%2Ftangerine-docs&label=%F0%9F%93%96%20View%20Live%20Documentation&up_message=citrus-software.github.io%2Ftangerine-docs&down_message=offline&style=for-the-badge" alt="View Live Documentation" />
  </a>
</p>

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Requirements

- [Node.js](https://nodejs.org/) LTS, version in [`.nvmrc`](.nvmrc) (at least Node 22).
  - Linux / macOS: [nvm](https://github.com/nvm-sh/nvm), then `nvm install` in this folder.
  - Windows: the LTS installer from [nodejs.org](https://nodejs.org/), or [fnm](https://github.com/Schniz/fnm) (`fnm install` in this folder).
- [Yarn](https://classic.yarnpkg.com/) 1.x: `npm install -g yarn`

Use `yarn` only (never `npm install`): dependencies are pinned by `yarn.lock`.

## Installation

```bash
yarn install
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

French version: `yarn start --locale fr`

## Build

```bash
yarn build
```

This command generates static content into the `build` directory (all locales) and checks broken links. `yarn serve` serves it locally.

## Deployment

Work happens on `develop` (GitLab). To publish:

1. Run the manual GitLab CI job `publish_main` on `develop`: `main` becomes an exact copy of `develop`, in a single new commit.
2. `main` is mirrored to GitHub, where the `Deploy Docusaurus to GitHub Pages` workflow (`.github/workflows/deploy.yml`) builds the site and pushes it to the `gh-pages` branch.

## Upgrading dependencies

```bash
yarn upgrade-interactive --latest
yarn build
```

Commit `package.json` and `yarn.lock` together.
