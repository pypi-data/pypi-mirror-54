# -*- coding: utf-8 -*-
import os
import sys
import json
import yaml
import time
import itertools
import threading
import traceback

from scalrctl import click, defaults, settings


def read_spec(api_level, ext='json'):
    """
    Reads Scalr specification file, json or yaml.
    """

    spec_path = os.path.join(defaults.CONFIG_DIRECTORY,
                             '{}.{}'.format(api_level, ext))

    if os.path.exists(spec_path):
        with open(spec_path, 'r') as fp:
            spec_data = fp.read()

        if ext == 'json':
            return json.loads(spec_data)
        elif ext == 'yaml':
            return yaml.safe_load(spec_data)
    else:
        msg = "Scalr specification file '{}' does  not exist, " \
              "try to run 'scalr-ctl update'.".format(spec_path)
        raise click.ClickException(msg)


def read_routes():
    if os.path.exists(defaults.ROUTES_PATH):
        with open(defaults.ROUTES_PATH, 'r') as fp:
            api_routes = fp.read()
        return json.loads(api_routes)


def read_scheme():
    with open(os.path.join(os.path.dirname(__file__),
                           'scheme/scheme.json')) as fp:
        return json.load(fp)


def read_config(profile=None):
    confpath = os.path.join(
        defaults.CONFIG_DIRECTORY,
        '{}.yaml'.format(profile)
    ) if profile else defaults.CONFIG_PATH

    if os.path.exists(confpath):
        with open(confpath, 'r') as fp:
            return yaml.safe_load(fp)


def warning(*messages):
    """
    Prints the warning message(s) to stderr.

    :param tuple messages: The list of the warning messages.
    :rtype: None
    """
    color = 'yellow' if settings.colored_output else None
    for index, message in enumerate(messages or [], start=1):
        index = index if len(messages) > 1 else None
        code = message.get('code') or ''
        text = message.get('message') or ''
        click.secho("Warning{index}{code} {text}".format(
            index=' {}:'.format(index) if index else ':',
            code=' {}:'.format(code) if code else '',
            text=text
        ), err=True, fg=color)


def debug(msg):
    if settings.debug_mode:
        click.secho("DEBUG: {}".format(msg),
                    fg='green' if settings.colored_output else None)


def reraise(message):
    import sys
    exc_info = sys.exc_info()
    if isinstance(exc_info[1], click.ClickException):
        exc_class = exc_info[0]
    else:
        exc_class = click.ClickException
    debug(traceback.format_exc())
    message = str(message)
    if not settings.debug_mode:
        message = "{}, use '--debug' option for details.".format(message)
    raise click.ClickException(message)


class _spinner(object):

    @staticmethod
    def draw(event):
        if settings.colored_output:
            cursor = itertools.cycle('|/-\\')
            while not event.isSet():
                sys.stdout.write(next(cursor))
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')
            sys.stdout.write(' ')
            sys.stdout.flush()

    def __init__(self):
        self.event = threading.Event()
        self.thread = threading.Thread(target=_spinner.draw,
                                       args=(self.event,))
        self.thread.daemon = True

    def __enter__(self):
        self.thread.start()

    def __exit__(self, type, value, traceback):
        self.event.set()
        self.thread.join()



