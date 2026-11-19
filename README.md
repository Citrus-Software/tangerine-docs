# Tangerine Docs

<p align="center">
  <a href="https://citrus-software.github.io/tangerine-docs">
    <img src="https://img.shields.io/website?url=https%3A%2F%2Fcitrus-software.github.io%2Ftangerine-docs&label=%F0%9F%93%96%20View%20Live%20Documentation&up_message=citrus-software.github.io%2Ftangerine-docs&down_message=offline&style=for-the-badge" alt="View Live Documentation" />
  </a>
</p>

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
