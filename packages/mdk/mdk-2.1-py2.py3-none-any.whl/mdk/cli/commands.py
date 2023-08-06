"""define all mdk cli commands"""
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=unused-variable
from pathlib import Path
from shutil import copy2, copytree
import sys
from typing import Callable

import click

from . import log_printer as log
from .shell_invoker import ShellInvoker
from .service_initializer import ServiceInitializer
from .. import errors
from ..filesystem.config import Config
# from ..filesystem.dev_socket import DevSocket


def define_commands(mdk_command: Callable[..., Callable]):
    """define all mdk cli commands"""
    config = Config()
    invoker = ShellInvoker()

    # mdk_socket = None
    # if config.dev_mode is True:
    #     mdk_socket = DevSocket()

    @mdk_command(
        name="bash",
        short_help="attach a bash shell for the active, running service",
    )
    def mdk_bash():
        """attach a bash shell for the active, running service

        docker-compose exec SERVICE bash"""
        if not invoker.has_active_service():
            log.error("attaching bash", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["exec", config.service, "bash"])


    @mdk_command(
        name="build",
        short_help="build the current service",
    )
    def mdk_build():
        """Build the active service

        docker-compose build SERVICE"""
        if not invoker.has_active_service():
            log.error("building service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)
        invoker.docker_compose_cwd(["build", config.service])


    @mdk_command(
        context_settings={"ignore_unknown_options": True},
        name="dc",
        short_help="run a docker-compose command",
    )
    @click.argument("command", nargs=-1, type=click.STRING)
    def mdk_dc(command):
        """Passthrough for running docker-compose commands

        docker-compose COMMAND"""
        invoker.docker_compose(list(command))


    @mdk_command(
        name="dev",
    )
    @click.argument("status")
    def mdk_dev(status):
        """activate/deactivate dev mode"""
        status_sanitized = status.strip().lower()
        if status_sanitized not in ["on", "off"]:
            log.error("(de)activating dev mode", "invalid [STATUS] {}\nValid options: 'on', 'off'")

        config.dev_mode = (status_sanitized == "on")
        log.success("{} Dev Mode".format("Activated" if config.dev_mode else "Deactivated"))


    @mdk_command(
        name="down",
        short_help="start a container for the current service",
    )
    def mdk_down():
        """stop and remove service containers for *all* services in active docker-compose.yaml

        docker-compose down"""
        if not invoker.has_active_service():
            log.error("building service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)
        if not click.confirm(
                "\nDestroying containers for active service {}\nProceed?".format(config.service),
                default=True):
            sys.exit(0)
        invoker.docker_compose_cwd(["down"])


    @mdk_command(
        context_settings={"ignore_unknown_options": True},
        name="dr",
        short_help="run a docker command",
    )
    @click.argument("command", nargs=-1, type=click.STRING)
    def mdk_dr(command):
        """Passthrough for running docker commands

        docker COMMAND"""
        invoker.docker(list(command))


    @mdk_command(
        name="init",
    )
    def mdk_init():
        """Initialize a new docker-compose service"""
        try:
            initializer = ServiceInitializer()
            initializer.prompt()
            initializer.confirm()
            service_name = initializer.generate()
            invoker.set_service(service_name)
        except errors.InitializationError as err:
            log.error("initializing new service", err.message)
        else:
            log.success("{} initiailized. Launch service:".format(service_name))
            log.notify("mdk up\n", indent_depth=2)


    @mdk_command(
        name="logs",
        short_help="view container logs",
    )
    def mdk_logs():
        """"view container logs

        docker-compose logs SERVICE
        """
        if not invoker.has_active_service():
            log.error("viewing service logs", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["logs", config.service])


    @mdk_command(
        name="lsi",
        short_help="list all docker images",
    )
    @click.option("-v", "--verbose", is_flag=True)
    def mdk_lsi(verbose):
        """list all docker images

        docker images"""
        images_command = ["images"]
        if not verbose:
            images_command.extend([
                "--format",
                "table {{.Repository}}\t{{.Tag}}\t{{.Size}}",
            ])
        ShellInvoker.docker(images_command)


    @mdk_command(
        name="lsc",
        short_help="list all docker containers",
    )
    @click.option("-v", "--verbose", is_flag=True)
    def mdk_lsc(verbose):
        """list all docker containers

        docker ps -a"""
        ls_command = ["ps", "-a"]
        if not verbose:
            ls_command.extend([
                "--format",
                "table {{.Names}}\t{{.Image}}\t{{.Status}}",
            ])
        ShellInvoker.docker(ls_command)


    @mdk_command(
        name="exec",
        short_help="run a command using the active service",
    )
    @click.argument("command", nargs=-1, type=click.STRING)
    @click.option("-d", "--detach", is_flag=True)
    def mdk_exec(command, detach):
        """run a command using the active service

        docker-compose exec [-d] SERVICE COMMAND"""
        if not invoker.has_active_service():
            log.error("executing command", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        exec_command = ["exec", config.service]
        invoker.docker_compose_cwd(exec_command + list(command), detach=detach)
        if detach:
            log.success("Executed {} with service {}".format(
                " ".join(command),
                config.service,
            ))


    @mdk_command(name="load")
    @click.argument(
        "resource",
        type=click.STRING,
    )
    def mdk_load(resource):
        """copy [RESOURCE] into mdk shared directory"""
        resource_path = Path(resource)
        if not resource_path.exists():
            log.error(
                "loading resource ",
                "Resource {} does not exist".format(resource))
        elif resource_path.is_dir():
            copytree(resource, config.host_shared_path/resource_path.stem)
        else:
            copy2(resource, config.host_shared_path)

        log.success("Copied {} to {}".format(resource, config.host_shared_path))


    @mdk_command(
        name="pause",
        short_help="pause a running container for the current service",
    )
    def mdk_pause():
        """"pause a running container for the current service

        docker-compose pause SERVICE
        """
        if not invoker.has_active_service():
            log.error("pausing service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["pause", config.service])


    @mdk_command(
        name="prune",
    )
    @click.option("-v", "--volumes", is_flag=True)
    def mdk_prune(volumes):
        """remove dangling docker assets (containers, images, and (optionally) volumes)"""
        prune_command = ["system", "prune", "-a", "-f"]
        action_string = "Destroying all inactive containers and unused images."
        if volumes:
            prune_command.append("--volumes")
            action_string = "Destroying all inactive containers, volumes, and unused images."
        if not click.confirm("\n{}\nProceed?".format(action_string), default=True):
            sys.exit(0)

        invoker.docker(prune_command)


    @mdk_command(
        name="run",
        short_help="Run a one-time command for the active service",
    )
    @click.argument("command", nargs=-1, type=click.STRING)
    def mdk_run(command):
        """Run a one-time command for the active service

        docker-compose run SERVICE COMMAND"""
        if not invoker.has_active_service():
            log.error("running service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        run_command = ["run", config.service]

        invoker.docker_compose_cwd(run_command + list(command))


    @mdk_command(
        name="start",
        short_help="start an existing container for the current service",
    )
    def mdk_start():
        """"start an existing container for the current service

        docker-compose start SERVICE"""
        if not invoker.has_active_service():
            log.error("starting service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["start", config.service])


    @mdk_command(
        name="status",
    )
    def mdk_status():
        """print the current active service"""
        if invoker.has_active_service():
            log.notify("active service:")
            log.notify("{:12}{}".format("name", config.service), indent_depth=2)
            log.notify("{:12}{}".format("root", config.working_dir), indent_depth=2)
            log.notify("mdk status:")
            log.notify(
                "{:12}{}".format(
                    "dev mode",
                    "On" if config.dev_mode else "Off",
                ),
                indent_depth=2,
            )
            log.notify("{:12}{}".format("shared dir", config.host_shared_path), indent_depth=2)
        else:
            log.notify("no active service")


    @mdk_command(
        name="stop",
        short_help="stop running container for the current service",
    )
    def mdk_stop():
        """stop running container for the current service

        docker-compose stop SERVICE
        """
        if not invoker.has_active_service():
            log.error("stopping service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["stop", config.service])


    @mdk_command(
        name="term",
        short_help="Open up a new detatched alacritty terminal",
    )
    def mdk_term():
        """Open up a new detatched alacritty terminal
        Only works for dev images with alacritty installed

        docker-compose exec -d SERVICE alacritty
        """
        if not invoker.has_active_service():
            log.error("opening terminal", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["exec", "-d", config.service, "alacritty"])


    @mdk_command(
        name="unpause",
        short_help="unpause a paused container for the current service",
    )
    def mdk_unpause():
        """"unpause a paused container for the current service

        docker-compose unpause SERVICE
        """
        if not invoker.has_active_service():
            log.error("unpausing service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["unpause", config.service])


    @mdk_command(
        name="use",
    )
    @click.argument(
        "service",
        type=click.STRING,
    )
    def mdk_use(service):
        """Set the active docker-compose service"""
        try:
            invoker.set_service(service)
        except errors.ConfigError as err:
            log.error("setting active service to \"{}\"".format(service), err.message)
        else:
            log.success("New active service: {}".format(service))


    @mdk_command(
        name="up",
        short_help="start a container for the current service",
    )
    @click.option("-a", "--attach", is_flag=True)
    @click.option("-b", "--build", is_flag=True)
    @click.option("--bash", is_flag=True)
    def mdk_up(attach, build, bash):
        """Start a container for the active service

        docker-compose up [--build] [-d] SERVICE"""
        if not config.service:
            log.error("starting service", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        up_command = ["up"]
        if build:
            up_command.append("--build")
        if not attach:
            up_command.append("-d")
        up_command.append(config.service)
        invoker.docker_compose_cwd(up_command)
        if bash:
            invoker.docker_compose_cwd(["exec", config.service, "bash"])


    @mdk_command(
        name="zsh",
        short_help="attach a zsh shell for the active, running service",
    )
    def mdk_zsh():
        """attach a zsh shell for the active, running service

        docker-compose exec SERVICE bash"""
        if not invoker.has_active_service():
            log.error("attaching zsh", "No active service. Try \"mdk use SERVICE\"")
            sys.exit(0)

        invoker.docker_compose_cwd(["exec", config.service, "zsh"])
