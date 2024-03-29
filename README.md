# GreenDeploy

GreenDeploy is a framework that makes it easy to build Dockerized Django projects
by providing uniform templates.

This is mostly a cli software.

## Release Schedule

1. py3.8 will be on `to-be-frozen` status starting 2022-10. This serves as a 1 year countdown to `frozen` status where it will no longer be supported
2. py3.8 will be supported till 2023-10 after which it will be on `frozen` status and removed from main brach and no longer supported.
3. py3.9 will be on `to-be-frozen` status starting 2023-10. This serves as a 1 year countdown to `frozen` status where it will no longer be supported

So the full schedule for this package is

| Python | add | `to-be-frozen` status | `frozen` status and stop supporting | PSF start release | PSF stop full support | PSF stop security fix |
|---|---|---|---|---|---|---|
| 3.8 | since package inception | 2022-10 | 2023-10 | 2019-10 | 2021-05 | 2024-10 |
| 3.9 | since package inception | 2023-10 | 2024-10 | 2020-10 | 2022-05 | 2025-10 |
| 3.10 **(latest)** | since package inception | 2024-10 | 2025-10 | 2021-10 | 2023-05 | 2026-10 |
| 3.11 *(preview)* | 2023-04 |2025-10 | 2026-10 | 2022-10 | 2024-05 | 2027-10 |

## How to install

Minimum python version: 3.9

Recommended to have a venv running python 3.9 before you run

```
pip install greendeploy-cli
```

Latest greendeploy-cli version is 0.0.11

Watch asciicast on installation for v0.0.9. Steps are the same.

[![asciicast](https://asciinema.org/a/481569.svg)](https://asciinema.org/a/481569)

## How to use

### Check info

```
greendeploy info
```

### Create a new Dockerized Django project from starter

```
greendeploy new --verbose
```

The starter is from https://github.com/GreenDeploy-io/greendeploy-starters/tree/main/starters/dockerized-django/default

Watch asciicast on creating new project locally on desktop
Requires: Docker and Docker Compose

[![asciicast](https://asciinema.org/a/481582.svg)](https://asciinema.org/a/481582)

Watch loom on how it should look like at first webpage load after first `new` command

[![[GreenDeploy CLI] First Web Load After First New Django Project - 29 March 2022 - Watch Video by Clicking](https://cdn.loom.com/sessions/thumbnails/5c11103b6f914ea58e53cf92b44c5ac8-with-play.gif)](https://www.loom.com/share/5c11103b6f914ea58e53cf92b44c5ac8)


#### Related Docker commands

To bring up the docker containers locally
```
docker-compose -f local.yml up
```

To stop the docker, use control + C

To bring down the docker containers locally
```
docker-compose -f local.yml down --remove-orphans
```
