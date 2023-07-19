import subprocess
import csv
import sys
import os
from lizard import FileAnalyzer,get_extensions,parse_args,OutputScheme,print_result,analyze
from lizard import AllResult, silent_printer,open_output_file
from gitop.gitop import get_commit_list,checkout_commit


analyze_file = FileAnalyzer(get_extensions([]))  # pylint: disable=C0103

def _calc_cc(cc,cnn):
  for i in range (6):
    exceed = cnn - 5*(i+1)
    cc[i]+=(exceed if exceed > 0 else 0)

def _sum(all_fileinfos, scheme):
  saved_fileinfos = []
  nloc = 0
  cc=[0,0,0,0,0,0]
  for module_info in all_fileinfos:
    if module_info:
      for fun in module_info.function_list:
        try:
          funcresult = [getattr(fun, item['value']) for item in scheme.items if item['caption']]
          nloc += funcresult[0]
          _calc_cc(cc,funcresult[1])
        except UnicodeEncodeError:
          print("Found ill-formatted unicode function name.")
    #print(nloc,cc, end="\r")
  return (nloc,cc)

def exceedance_rate(options,schema):
  result = analyze(
    options.paths,
    options.exclude,
    options.working_threads,
    options.extensions,
    options.languages)
  (nloc,cc)= _sum(result, schema)
  results = [ round(c*1000/nloc, 2) for c in cc]
  results.insert(0,nloc)
  return results # [nloc,c5,c10,c15,c20,c25,c30]

def preparing(argv):

  options = parse_args(argv or sys.argv)
  printer = options.printer or print_result
  schema = OutputScheme(options.extensions)
  if schema.any_silent():
    printer = silent_printer
  schema.patch_for_extensions()
  if options.input_file:
    options.paths = auto_read(options.input_file).splitlines()
  return (options,schema,printer)


def counting_repo(options,schema):
  commitlist = get_commit_list(options.paths[0],'master',options.interval)
  results =[]
  print(len(commitlist))
  for commit in commitlist:
    checkout_commit(options.paths[0],commit["commit_id"])
    ret = exceedance_rate(options,schema)
    ret.insert(0,commit["commit_id"])
    results.append(ret)
  return results
def main(argv=None):
  original_stdout = sys.stdout
  (options,schema,printer) = preparing(argv)
  # 打开输出文件
  output_file = None
  if options.output_file:
    output_file = open_output_file(options.output_file)
    sys.stdout = output_file
  print(counting_repo(options,schema))

  # 关闭输出文件
  if output_file:
    sys.stdout = original_stdout
    output_file.close()


if __name__ == "__main__":

  if len(sys.argv) <= 1:

    print("Please provide a repo directory and a branch name")
    print(f"命令行如下： {sys.argv[0]} <repo_dir>  <branch_name>")
  main()