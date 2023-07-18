import subprocess
import csv
import sys
import os
from lizard import FileAnalyzer,get_extensions,parse_args,OutputScheme,print_result,analyze
from lizard import AllResult


analyze_file = FileAnalyzer(get_extensions([]))  # pylint: disable=C0103

def main(argv=None):
    options = parse_args(argv or sys.argv)
    printer = options.printer or print_result
    schema = OutputScheme(options.extensions)
    if schema.any_silent():
        printer = silent_printer
    schema.patch_for_extensions()
    if options.input_file:
        options.paths = auto_read(options.input_file).splitlines()
    original_stdout = sys.stdout
    output_file = None
    if options.output_file:
        output_file = open_output_file(options.output_file)
        sys.stdout = output_file
    result = analyze(
        options.paths,
        options.exclude,
        options.working_threads,
        options.extensions,
        options.languages)
    warning_count = printer(result, options, schema, AllResult)

if __name__ == "__main__":

  if len(sys.argv) <= 1:

    print("Please provide a repo directory and a branch name")
    print(f"命令行如下： {sys.argv[0]} <repo_dir>  <branch_name>")
  main()