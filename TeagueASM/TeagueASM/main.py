import click
from pathlib import Path
from .parsing import (
    initial_parse,
    convert_to_hex,
    resolve_macros_and_tags,
    list_to_instruction,
)
from .types.instructions import Instruction, hex_instruction_to_string
from typing import Union


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

    asmpath_object: Path = Path(filepath)
    if not (asmpath_object).exists():
        click.echo(f"{filepath} does not exist, please enter a valid file.", err=True)
    if asmpath_object.suffix.lower() != ".tgasm":
        click.echo(
            click.style(
                f"Uh oh! It seems like {filepath} is not a valid .tgasm file!", fg="red"
            ),
            err=True,
        )

    assembly_text: str = ""
    with open(asmpath_object, "r") as read_file:
        assembly_text = read_file.read()

    initial_parse_res: list[str] = initial_parse(assembly_text)
    resolved_macros_and_tags: list[str] = resolve_macros_and_tags(initial_parse_res)

    click.echo(
        click.style(f"All Green, no errors found!", fg="green"),
    )


@cli.command("asm2hex")  # type: ignore
@click.argument("asmpath")
@click.option("--outpath", "-o", default="")
def asm2hex(asmpath: str, outpath: str = "") -> None:
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

    assembly_text: str = ""
    with open(asmpath_object, "r") as read_file:
        assembly_text = read_file.read()

    initial_parse_res: list[str] = initial_parse(assembly_text)
    resolved_macros_and_tags: list[str] = resolve_macros_and_tags(initial_parse_res)
    instruction_list: list[Instruction] = list_to_instruction(resolved_macros_and_tags)
    hex_out = convert_to_hex(instruction_list)

    click.echo(
        click.style(f"All Green, no errors found!", fg="green"),
    )

    if outpath == "":
        path_to_write: Path = Path(asmpath.split(".tgasm")[0] + "_hex.hex")
    else:
        path_to_write: Path = Path(outpath)

    with open(path_to_write, "w") as outfile:
        outfile.write(hex_out)


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
    click.echo(f"Attempting to convert {filepath} to TeagueASM!")

    path_object: Path = Path(filepath)
    if not (path_object).exists():
        click.echo(f"{filepath} does not exist, please enter a valid file.", err=True)
    if path_object.suffix.lower() != ".hex":
        click.echo(
            click.style(
                f"Uh oh! It seems like {filepath} is not a valid .hex file!", fg="red"
            ),
            err=True,
        )

    with open(filepath, "r") as read_file:
        hex_text = read_file.read()

    output = ""
    for line_num, line in enumerate(hex_text.split("\n")):
        output += hex_instruction_to_string(line, line_num)
        output += "\n"

    if outpath == "":
        path_to_write: Path = Path(filepath.split(".hex")[0] + "_decoded.tgasm")
    else:
        path_to_write: Path = Path(outpath)

    with open(path_to_write, "w") as outfile:
        outfile.write(output)

    click.echo(
        click.style(f"Successfully decoded!, no errors found!", fg="green"),
    )
