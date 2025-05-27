from ..types.instructions import (
    string_to_instruction,
    Instruction,
)  # for initial line validation


def parse(file_text: str) -> bool:  # return a success or fail
    return False


def initial_parse(file_text: str) -> list[str]:
    """
    Initial parse will check if each line either contains
    a jump tag or an instruction-like string.

    Jump tags will get flattened onto the same line as the next instruction-like string
    for the second parser to resolve jump addresses.

    Args:
        file_text (str): input string to be parsed

    Returns:
        List[str]: A list of instruction like strings
    """

    flattened_new_lines: str = ""

    for index, line in enumerate(file_text.split("\n")):
        if line.startswith("#"):
            flattened_new_lines += "#" + line.split("#")[-1].strip() + "#"
        else:
            if not (line.startswith("//")) and (line.strip()):
                instruction: Instruction = string_to_instruction(
                    line, index
                )  # use this for validation, not the cleanest but hey ho
                if not (instruction.validate_args()):  # type: ignore
                    raise ValueError(
                        f"ERROR ON LINE {index}, Call {line} violates arg rules!"
                    )
                flattened_new_lines += line + "\n"

    text_string_split: list[str] = flattened_new_lines.split("\n")

    text_string_split_ignore_comments: list[str] = [
        i.split("//")[0].strip() for i in text_string_split if i != ""
    ]

    return text_string_split_ignore_comments


def second_parser(file_text: str) -> list[str]:
    """
    Resolve any jump locations and inline macros.

    Args:
        file_text (str): _description_

    Returns:
        list[str]: _description_
    """
