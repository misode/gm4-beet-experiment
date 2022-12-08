import click
import subprocess
# from beet import Project
# from beet.toolchain.cli import beet
from contextlib import suppress

@click.group()
def main():
	pass

# pass_project = click.make_pass_decorator(Project) # type: ignore

@main.command()
# @beet.command()
# @pass_project
@click.argument("modules", nargs=-1)
@click.option("-r", "--reload", is_flag=True, help="Enable live data pack reloading.")
@click.option("-l", "--link", metavar="WORLD", help="Link the project before watching.")
def dev(modules: tuple[str], reload: bool, link: str | None):
	if len(modules) == 0:
		click.echo("You need at least one module")
		return
	click.echo(f"Building modules: {', '.join(modules)}")

	args = ["beet"]

	broadcast = ", ".join([f"\"gm4_{m}\"" for m in modules])
	args.extend(["--set", f"pipeline[0].broadcast = [{broadcast}]"])
	args.extend(["--set", "meta.autosave.link = false"])

	args.append("watch")

	if reload:
		args.append("--reload")

	if link:
		args.extend(["--link", link])

	with suppress(KeyboardInterrupt):
		subprocess.run(args)


if __name__ == "__main__":
	main()
