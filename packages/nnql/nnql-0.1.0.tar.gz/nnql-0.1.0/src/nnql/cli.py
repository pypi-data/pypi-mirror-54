import runpy
import sys
from typing import List

from nnql.executor import set_program_args


# @click.command(context_settings=dict(
#     ignore_unknown_options=True,
# ))
# @click.option("--tool", "-t")
# @click.argument('rest_args', nargs=-1, type=click.UNPROCESSED)
def nnql():
    def parse_rest_args(tool: str, rest_args: List[str]):
        # print(f"rest_args: {rest_args}")
        separator_index = rest_args.index("--program")
        assert separator_index != -1
        tool_args = rest_args[:separator_index]
        sys.argv = [tool] + list(tool_args)
        set_program_args(rest_args[separator_index + 1 :])

    args = sys.argv[1:]
    assert len(args) >= 2 and (args[0] == "--tool" or args[0] == "-t")
    args = args[1:]
    if args[0] == "-m":
        assert len(args) >= 2
        module_name = args[1]
        parse_rest_args(tool=module_name, rest_args=args[2:])
        runpy.run_module(module_name, run_name="__main__")
    else:
        assert len(args) >= 1
        file_path = args[0]
        parse_rest_args(tool=file_path, rest_args=args[1:])
        runpy.run_path(file_path, run_name="__main__")
