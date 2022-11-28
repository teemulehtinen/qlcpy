import argparse
import ast
import json

from . import i18n
from .generator import generate, QLCRequest, QLC
from .questions import TEMPLATES

def cmd_string(str):
  return str.replace('\\n', '\n')

def main():
  parser = argparse.ArgumentParser(
    description='QLCpy generates questions that target analysed facts about the given program'
  )
  parser.add_argument('program', nargs='?', default=None, help='A python program file')
  parser.add_argument('-c', '--call', help='A python call to execute')
  parser.add_argument('-i', '--input', help='Use as stdio when executing')
  parser.add_argument('-n', default=3, help='Number of questions (at maximum)')
  parser.add_argument('-t', '--types', nargs='+', help='Only these question types')
  parser.add_argument('-u', '--unique', action='store_true', help='Only unique question types')
  parser.add_argument('-l', '--lang', help='Language code for the text (en, fi)')
  parser.add_argument('--json', action='store_true', help='Print question data as JSON')
  parser.add_argument('--list-types', action='store_true', help='List available question types')
  args = parser.parse_args()

  if args.list_types:
    print('Available QLC types:')
    for t in TEMPLATES:
      print(f'* {t.type:<25} {t.description}')
    parser.exit()

  if not args.program:
    parser.print_usage()
    parser.exit()
  with open(args.program, 'r') as f:
    tree = ast.parse(f.read())

  if args.lang:
    i18n.lang = args.lang

  qlcs = generate(
    tree,
    [QLCRequest(args.n, types=args.types, unique_types=args.unique)],
    cmd_string(args.call),
    cmd_string(args.input)
  )

  if args.json:
    print(json.dumps(list(qlc.to_dict() for qlc in qlcs)))
  else:
    print('\n\n'.join(str(qlc) for qlc in qlcs))
