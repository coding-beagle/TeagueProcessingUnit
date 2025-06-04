from ..types.instructions import (
    string_to_instruction,
    Instruction,
    Jump,
)  # for initial line validation
import re
from typing import Optional


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
        test_line: str = line.strip()
        if test_line.startswith("#"):
            flattened_new_lines += "#" + test_line.split("#")[-1].strip() + "#"
        else:
            if not (test_line.startswith("//")) and (test_line):
                if not test_line.startswith("JMP"):
                    instruction: Instruction = string_to_instruction(
                        test_line, index + 1
                    )  # use this for validation, not the cleanest but hey ho
                    # don't validate jump instructions for now
                    if not (instruction.validate_args()) and not (isinstance(instruction, Jump)):  # type: ignore
                        raise ValueError(
                            f"ERROR ON LINE {index + 1}, Call {line} violates arg rules!"
                        )
                flattened_new_lines += test_line + "\n"

    text_string_split: list[str] = flattened_new_lines.split("\n")

    text_string_split_ignore_comments: list[str] = [
        i.split("//")[0].strip() for i in text_string_split if i != ""
    ]

    return text_string_split_ignore_comments


def resolve_macros_and_tags(lines_split: list[str]) -> list[str]:
    """
    Any remaining instructions here will need their macros resolved, and jump counts need to be resolved as well

    Args:
        lines_split (list[str]): An instruction-like list of strings, with all comments removed and each list item
        corresponding to an instruction.

    Returns:
        list[str]: A list of instruction-like strings that have had all macros and tags resolved.
    """

    # two passes, one to get which tags correspond to which line number
    # and the second pass to replace the arg for JMP
    tag_dict: dict[str, int] = {}  # which lines have tags
    jump_location_dict: dict[int, str] = {}  # line number: tag

    BRACKET_REGEX = r"\$\{(.*?)\}"
    TAG_GROUP = r"#(.*?)#"
    TAG_AS_ARG = r"'(.*?)'"

    output: list[str] = []

    for index, line in enumerate(lines_split):
        ## Resolve macros
        potential_match_macro: Optional[re.Match] = re.search(BRACKET_REGEX, line)
        potential_match_tagline: Optional[re.Match] = re.search(TAG_GROUP, line)
        potential_match_tagarg: Optional[re.Match] = re.search(TAG_AS_ARG, line)

        if potential_match_macro:
            # Extract the content inside the brackets
            macro_content = potential_match_macro.group(
                1
            )  # group(1) gets the first capture group

            # Evaluate the macro content
            try:
                evaluated_result = eval(macro_content)
                # Replace the entire match (including brackets) with the evaluated result
                out_line: str = line.replace(
                    potential_match_macro.group(0), str(evaluated_result)
                )

                output.append(out_line)

            except Exception as e:
                raise ValueError(f"Error evaluating macro '{macro_content}': {e}")
        elif potential_match_tagline:
            tag_name = potential_match_tagline.group(1)
            tag_dict[tag_name] = index
            output.append(re.sub(TAG_GROUP, "", line, 1))

        elif potential_match_tagarg:
            tag_name = potential_match_tagarg.group(1)
            jump_location_dict[index] = tag_name
            output.append(re.sub(TAG_AS_ARG, "", line, 1))

        else:
            output.append(line)

    for line_number, tag in jump_location_dict.items():
        if tag not in tag_dict:
            raise ValueError(f"ERROR RESOLVING TAGS: Unresolved tag {tag}")
        output[line_number] = f"JMP {tag_dict[tag]}"

    return output


def list_to_instruction(instruction_string_list: list[str]) -> list[Instruction]:
    """
    Take an instruction-like list, and turn them all into instruction objects

    Args:
        instruction_string_list (list[str]): An instruction-like list of strings, with all comments removed and each list item
        corresponding to an instruction. Jump tags and macros should all be resolved by this point

    Raises:
        ValueError: If errors in serialising
        ValueError: If errors in serialising

    Returns:
        list[Instruction]: A list of instruction objects to be serialised.
    """
    output: list[Instruction] = []

    for line in instruction_string_list:
        if len(output) == 0:
            try:
                output = [string_to_instruction(input_string=line)]
            except ValueError as exc:
                raise ValueError(
                    f"Something went wrong when we tried to serialise {line}"
                ) from exc
        else:
            try:
                output.append(string_to_instruction(input_string=line))
            except ValueError as exc:
                raise ValueError(
                    f"Something went wrong when we tried to serialise {line}"
                ) from exc

    return output


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
        # print(f"{i} will get serialised")
        output += i.serialise() + "\n"

    return output.strip()
