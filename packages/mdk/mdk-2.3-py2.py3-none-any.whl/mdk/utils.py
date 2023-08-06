"""mdk utility functions & classes"""
from copy import deepcopy
import os
from pathlib import Path
import shelve
import subprocess
from typing import Any, Dict, List, Union
import click
import yaml
from yaml import SafeDumper

class Config():
    """manage interaction with mdk config file"""
    def __init__(self):
        config_dir_path = Path.home()/".config/mdk"
        if not config_dir_path.exists():
            config_dir_path.mkdir(parents=True)
            os.chown(
                config_dir_path,
                os.geteuid(),
                os.getgid(),
            )

        if not self.shared_path_host.exists():
            self.shared_path_host.mkdir(parents=True)
            os.chown(
                self.shared_path_host,
                os.geteuid(),
                os.getgid(),
            )

    def __getattr__(self, name):
        """get val of key from persistent storage"""
        if name == "shared_on":
            return True

        data_store = shelve.open(str(Path.home()/".config/mdk/config.mdk"))
        config_defaults = {
            "service_name": None,
            "service_dir": None,
            "shared_extension": "shared",
            "shared_path_host": Path.home()/"mdkshared",
            "shared_path_target": "/mdkshared",
        }

        # when pulling value, use data store > default > None
        val = data_store.get(
            name,
            config_defaults.get(
                name,
                None,
            )
        )

        data_store.close()
        return val

    def __setattr__(self, name, value):
        """set key:val in persistent storage"""
        data_store = shelve.open(str(Path.home()/".config/mdk/config.mdk"))
        data_store[name] = value
        data_store.close()


class Log():
    """unified mdk console logging"""
    @staticmethod
    def __call__(message):
        """generic message formatting"""
        click.echo(message)

    @staticmethod
    def error(context, message):
        """error formatting"""
        click.echo("{} {}:\n  {}".format(click.style("ERROR", fg="red"), context, message))

    @staticmethod
    def success(context):
        """success formatting"""
        click.echo("{}: {}".format(click.style("SUCCESS", fg="green"), context))


def docker(args: List[str], detach=False):
    """$ docker [args]"""
    command_builder = ["docker"] + args
    if detach is True:
        return subprocess.getoutput(" ".join(command_builder))
    return subprocess.call(command_builder)


def docker_compose(args: List[str], detach=False):
    """$ docker-compose [args], from directory of current service"""
    config = Config()
    command_builder = ["docker-compose"]
    if config.shared_on is True:
        write_shared_config()
        command_builder.extend(["-f", "docker-compose.yaml"])
        command_builder.extend(
            ["-f", "docker-compose.{}.yaml".format(config.shared_extension)]
        )

    command_builder.extend(args)

    run_from = config.service_dir
    if run_from is None:
        run_from = Path.cwd()

    if detach is True:
        return subprocess.getoutput(" ".join(args))

    return subprocess.call(
        command_builder,
        cwd=config.service_dir,
    )


def parse_yaml(file_path: Path) -> Union[Dict[str, Any], None]:
    """yaml file reader & parser"""
    if not file_path.is_file():
        return None
    file_data = file_path.read_text()
    parsed_yaml = yaml.load(file_data, Loader=yaml.Loader) # type: Dict[str, Any]
    return parsed_yaml


def write_shared_config():
    """write a dev override file using a list of service names"""
    config = Config()
    if config.service_dir is None:
        return

    original_compose_contents = parse_yaml(config.service_dir/"docker-compose.yaml")
    if original_compose_contents is None or "services" not in original_compose_contents:
        return

    service_contents = {
        "volumes": [
            "{}:{}".format(
                config.shared_path_host,
                config.shared_path_target,
            ),
            "vscode:/home/matic/.vscode-server",
            "vscode-insiders:/home/matic/.vscode-server-insiders"
        ],
    }
    service_blocks = {}

    for service, _ in original_compose_contents["services"].items():
        service_blocks[service] = deepcopy(service_contents)

    compose_contents = {
        "services": service_blocks,
        "version": original_compose_contents["version"],
        "volumes": {
            "vscode": None,
            "vscode-insiders": None,
        }
    }

    SafeDumper.add_representer(
        type(None),
        lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
    )
    compose_path = config.service_dir/("docker-compose.{}.yaml".format(config.shared_extension))
    compose_stream = compose_path.open("w")
    yaml.dump(compose_contents, compose_stream, Dumper=SafeDumper)
    return
