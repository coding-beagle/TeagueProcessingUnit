import click


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
@click.argument("filepath")
@click.argument("outpath", default="")
def asm2hex(asmpath: str, outpath: str) -> None:
    """
    Convert a file from TeagueASM to machine readable Hex.

    Args:
        asmpath (str): Path of file to be converted
        outpath (str): Path of file to be written to (defaults to {asmpath}_hex.hex)
    """
    lint(asmpath)


@cli.command("hex2asm")  # type: ignore
@click.argument("filepath")
@click.argument("outpath", default="")
def hex2asm(hexpath: str, outpath: str) -> None:
    """
    Convert a file from hex to TeagueASM.

    Args:
        hexpath (str): Path of file to be converted
        outpath (str): Path of file to be written to (defaults to {hexpath}_asm.TeagueASM)
    """
    lint(asmpath)
