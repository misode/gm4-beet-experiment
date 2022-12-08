import click
import json
import subprocess
from beet.toolchain.cli import beet
from contextlib import suppress

@beet.command()
@click.argument("modules", nargs=-1)
@click.option("-r", "--reload", is_flag=True, help="Enable live data pack reloading.")
@click.option("-l", "--link", metavar="WORLD", help="Link the project before watching.")
def dev(modules: tuple[str], reload: bool, link: str | None):
	"""Watch modules for development."""

	modules = tuple(m if m.startswith("gm4_") else f"gm4_{m}" for m in modules)
	if len(modules) == 0:
		click.echo("You need at least one module")
		return
	click.echo(f"Building modules: {', '.join(modules)}")

	args = ["beet"]

	args.extend(["--set", f"pipeline[0].broadcast = {json.dumps(modules)}"])
	args.extend(["--set", "meta.autosave.link = false"])

	args.append("watch")

	if reload:
		args.append("--reload")

	if link:
		args.extend(["--link", link])

	with suppress(KeyboardInterrupt):
		subprocess.run(args)
