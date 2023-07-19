import subprocess
import csv
import sys
import os
from lizard import FileAnalyzer,get_extensions,parse_args,OutputScheme,print_result,analyze
from lizard import AllResult, silent_printer,open_output_file
from gitop.gitop import get_commit_list,checkout_commit
from pic_gen.drawpolt import draw_skewed_curve



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
          # print(funcresult)
          nloc += funcresult[0]
          _calc_cc(cc,funcresult[1])
        except UnicodeEncodeError:
          print("Found ill-formatted unicode function name.")
  return (nloc,cc)

def cc_distribution(options,schema):
  result = analyze(
    options.paths,
    options.exclude,
    options.working_threads,
    options.extensions,
    options.languages)
  counts = {}
  for module_info in result:
    if module_info:
      for fun in module_info.function_list:
        try:
          funcresult = [getattr(fun, item['value']) for item in schema.items if item['caption']]
          print(','.join(str(num) for num in funcresult[:5]),end='\r')
          if funcresult[1] not in counts:
            counts[funcresult[1]] = 1
          else:
            counts[funcresult[1]] += 1
        except UnicodeEncodeError:
          print("Found ill-formatted unicode function name.")
  return counts


def exceedance_rate(options,schema):
  result = analyze(
    options.paths,
    options.exclude,
    options.working_threads,
    options.extensions,
    options.languages)
  (nloc,cc)= _sum(result, schema)
  if(nloc > 0):
    results = [ round(c*1000/nloc, 2) for c in cc]
    results.insert(0,nloc)
  else:
    # 目录中没有代码
    results = [0 for i in range(7)]
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
  commitlist = get_commit_list(options.paths[0],options.branch,options.interval)
  print(len(commitlist))
  results =[]
  for commit in commitlist:
    checkout_commit(options.paths[0],commit["commit_id"])
    ret = exceedance_rate(options,schema)
    ret.insert(0,commit["commit_id"])
    ret.insert(0,commit["commit_date"])
    results.append(ret)
  return results

def generate_report(lst):
    print('time,rev,nloc,C5,C10,C15,C20,C25,C30')
    for sub_list in lst:
      line = ','.join(str(x) for x in sub_list)
      print(line)

def main(argv=None):
  original_stdout = sys.stdout
  (options,schema,printer) = preparing(argv)
  # 打开输出文件
  output_file = None
  if options.skewed:
    counts = cc_distribution(options,schema)
    draw_skewed_curve(counts)
    return
  if options.output_file:
    output_file = open_output_file(options.output_file)
    sys.stdout = output_file
  result = counting_repo(options,schema)
  generate_report(result)
  # 关闭输出文件
  if output_file:
    sys.stdout = original_stdout
    output_file.close()


if __name__ == "__main__":

  if len(sys.argv) <= 1:

    print("Please provide a repo directory and a branch name")
    print(f"命令行如下： {sys.argv[0]} <repo_dir>  <branch_name>")
  main()