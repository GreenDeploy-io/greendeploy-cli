"""Utilities for use with click."""

import difflib
import sys
import traceback
from collections import defaultdict
from itertools import chain
from typing import Iterable, List, Mapping, Sequence, Set, Tuple

import click
import pkg_resources

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
CUTOFF = 0.5
ENTRY_POINT_GROUPS = {
    "global": "gdeploy.global_commands",
    "project": "gdeploy.project_commands",
    "init": "gdeploy.init",
    "line_magic": "gdeploy.line_magic",
    "hooks": "gdeploy.hooks",
    "cli_hooks": "gdeploy.cli_hooks",
}
MAX_SUGGESTIONS = 3

def load_entry_points(name: str) -> Sequence[click.MultiCommand]:
    """Load package entry point commands.
    Args:
        name: The key value specified in ENTRY_POINT_GROUPS.
    Raises:
        KedroCliError: If loading an entry point failed.
    Returns:
        List of entry point commands.
    """
    entry_points = pkg_resources.iter_entry_points(group=ENTRY_POINT_GROUPS[name])
    entry_point_commands = []
    for entry_point in entry_points:
        try:
            entry_point_commands.append(entry_point.load())
        except Exception as exc:
            raise GDeployCliError(f"Loading {name} commands from {entry_point}") from exc
    return entry_point_commands

def _suggest_cli_command(
    original_command_name: str, existing_command_names: Iterable[str]
) -> str:
    matches = difflib.get_close_matches(
        original_command_name, existing_command_names, MAX_SUGGESTIONS, CUTOFF
    )

    if not matches:
        return ""

    if len(matches) == 1:
        suggestion = "\n\nDid you mean this?"
    else:
        suggestion = "\n\nDid you mean one of these?\n"
    suggestion += textwrap.indent("\n".join(matches), " " * 4)  # type: ignore
    return suggestion



class GDeployCliError(click.exceptions.ClickException):
    """Exceptions generated from the GDeploy CLI.
    Users should pass an appropriate message at the constructor.
    """

    VERBOSE_ERROR = False

    def show(self, file=None):
        if file is None:
            # pylint: disable=protected-access
            file = click._compat.get_text_stderr()
        if self.VERBOSE_ERROR:
            click.secho(traceback.format_exc(), nl=False, fg="yellow")
        else:
            etype, value, _ = sys.exc_info()
            formatted_exception = "".join(traceback.format_exception_only(etype, value))
            click.secho(
                f"{formatted_exception}Run with --verbose to see the full exception",
                fg="yellow",
            )
        click.secho(f"Error: {self.message}", fg="red", file=file)

class CommandCollection(click.CommandCollection):
    """Modified from the Click one to still run the source groups function."""

    def __init__(self, *groups: Tuple[str, Sequence[click.MultiCommand]]):
        self.groups = [
            (title, self._merge_same_name_collections(cli_list))
            for title, cli_list in groups
        ]
        sources = list(chain.from_iterable(cli_list for _, cli_list in self.groups))

        help_texts = [
            cli.help
            for cli_collection in sources
            for cli in cli_collection.sources
            if cli.help
        ]
        self._dedupe_commands(sources)
        super().__init__(
            sources=sources,
            help="\n\n".join(help_texts),
            context_settings=CONTEXT_SETTINGS,
        )
        self.params = sources[0].params
        self.callback = sources[0].callback

    @staticmethod
    def _dedupe_commands(cli_collections: Sequence[click.CommandCollection]):
        """Deduplicate commands by keeping the ones from the last source
        in the list.
        """
        seen_names: Set[str] = set()
        for cli_collection in reversed(cli_collections):
            for cmd_group in reversed(cli_collection.sources):
                cmd_group.commands = {  # type: ignore
                    cmd_name: cmd
                    for cmd_name, cmd in cmd_group.commands.items()  # type: ignore
                    if cmd_name not in seen_names
                }
                seen_names |= cmd_group.commands.keys()  # type: ignore

        # remove empty command groups
        for cli_collection in cli_collections:
            cli_collection.sources = [
                cmd_group
                for cmd_group in cli_collection.sources
                if cmd_group.commands  # type: ignore
            ]

    @staticmethod
    def _merge_same_name_collections(groups: Sequence[click.MultiCommand]):
        named_groups: Mapping[str, List[click.MultiCommand]] = defaultdict(list)
        helps: Mapping[str, list] = defaultdict(list)
        for group in groups:
            named_groups[group.name].append(group)
            if group.help:
                helps[group.name].append(group.help)

        return [
            click.CommandCollection(
                name=group_name,
                sources=cli_list,
                help="\n\n".join(helps[group_name]),
                callback=cli_list[0].callback,
                params=cli_list[0].params,
            )
            for group_name, cli_list in named_groups.items()
            if cli_list
        ]

    def resolve_command(self, ctx: click.core.Context, args: List):
        try:
            return super().resolve_command(ctx, args)
        except click.exceptions.UsageError as exc:
            original_command_name = click.utils.make_str(args[0])
            existing_command_names = self.list_commands(ctx)
            exc.message += _suggest_cli_command(
                original_command_name, existing_command_names
            )
            raise

    def format_commands(
        self, ctx: click.core.Context, formatter: click.formatting.HelpFormatter
    ):
        for title, cli in self.groups:
            for group in cli:
                if group.sources:
                    formatter.write(
                        click.style(f"\n{title} from {group.name}", fg="green")
                    )
                    group.format_commands(ctx, formatter)
