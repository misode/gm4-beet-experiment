import click
import subprocess
from beet import Project
from beet.toolchain.cli import beet
from contextlib import suppress

pass_project = click.make_pass_decorator(Project) # type: ignore

@beet.command()
@pass_project
@click.argument("modules", nargs=-1)
def dev(modules: str):
	click.echo(f"Building modules: {', '.join(modules)}")
	broadcast = ", ".join([f"\"gm4_{m}\"" for m in modules])

	with suppress(KeyboardInterrupt):
		subprocess.run([
			"beet",
			"--set",
			f"pipeline[0].broadcast = [{broadcast}], meta.autosave.link = false",
			"watch",
			"--link",
			"gm4"
		])
