from ..types.instructions import (
    string_to_instruction,
    Instruction,
    Jump,
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
                # don't validate jump instructions for now
                if not (instruction.validate_args()) and not (isinstance(instruction, Jump)):  # type: ignore
                    raise ValueError(
                        f"ERROR ON LINE {index}, Call {line} violates arg rules!"
                    )
                flattened_new_lines += line + "\n"

    text_string_split: list[str] = flattened_new_lines.split("\n")

    text_string_split_ignore_comments: list[str] = [
        i.split("//")[0].strip() for i in text_string_split if i != ""
    ]

    return text_string_split_ignore_comments


# TODO, this will be very useful, but currently not needed for an MVP ASSEMBLER
def second_parser(lines_split: list[str]) -> list[Instruction]:
    """
    Any remaining instructions here will need their macros resolved, and jump counts need to be resolved as well

    Args:
        lines_split (list[str]): _description_

    Returns:
        list[Instruction]: _description_
    """
    pass


def convert_to_hex(object_list: list[Instruction]) -> str:
    """
    Takes in a list of instruction objects and serialises all of them

    Args:
        object_list (list[Instruction]): A list of instruction objects to be serialised

    Returns:
        str: A .hex-like string
    """
    output = ""
    for i in object_list:
        print(f"{i} will get serialised")
        output += i.serialise() + "\n"

    return output.strip()
