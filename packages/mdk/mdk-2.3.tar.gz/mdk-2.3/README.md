# mdk

`mdk` is a cli helper for docker-compose built at [Matician](https://matician.com/).

## Prerequisites
* Python (3)
* pip (3)
* Docker

### About docker/docker-compose versions
As of 10/23/19, we are using **compose file version 3.7**. Requirements:
  * docker(engine) >= 18.06.0
  * docker-compose >= 1.22.0

Determine compose file compatibility with versions of
  * [docker(engine)](https://docs.docker.com/compose/compose-file/)
  * [docker-compose](https://docs.docker.com/release-notes/docker-compose/)

## Installation
```sh
pip install --user mdk
```

Note: you must have the `mdk` executable in your `$PATH`. If you used the installation instructions above, the executable is in `~/.local/bin`.

## Usage
Run the `mdk` command after installation for a full list of commands. For help on individual commands, use `mdk COMMAND --help`.

## mdkshared
All services launched by `mdk` contain a folder `/mdkshared`, which is bound to the `~/mdkshared` folder on your host machine.

## FAQ

### How do I keep a container running after `mdk up`?
Try setting the command to `top -b`, which will idle the container indefinitely.