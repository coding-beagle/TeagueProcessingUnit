import click
from pathlib import Path


@click.group()
def cli():
    click.echo("Starting the TeagueAssembler ...")


@cli.command("lint")  # type: ignore
@click.argument("filepath")
def lint(filepath: str) -> None:
    """
    Lint a file for formatting errors

    Args:
        filepath (str): The path of the file to lint
    """
    click.echo(f"Attempting to lint {filepath}")


@cli.command("asm2hex")  # type: ignore
@click.argument("asmpath")
@click.option("--outpath", "-o", default="")
def asm2hex(asmpath: str, outpath: str) -> None:
    """
    Convert a file from TeagueASM to machine readable Hex.

    Args:
        asmpath (str): Path of file to be converted
        outpath (str): Path of file to be written to (defaults to {asmpath}_hex.hex)
    """
    asmpath_object: Path = Path(asmpath)
    if not (asmpath_object).exists():
        click.echo(f"{asmpath} does not exist, please enter a valid file.", err=True)
    if asmpath_object.suffix.lower() != ".tgasm":
        click.echo(
            click.style(
                f"Uh oh! It seems like {asmpath} is not a valid .tgasm file!", fg="red"
            ),
            err=True,
        )


@cli.command("hex2asm")  # type: ignore
@click.argument("filepath")
@click.option("--outpath", "-o", default="")
def hex2asm(filepath: str, outpath: str) -> None:
    """
    Convert a file from hex to TeagueASM.

    Args:
        hexpath (str): Path of file to be converted
        outpath (str): Path of file to be written to (defaults to {hexpath}_asm.tgasm)
    """
    click.echo(f"Attempting to convert {hexpath} to TeagueASM!")
