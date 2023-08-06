from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


def find_top():
  import os.path
  path = os.path.abspath(__file__)

  while True:
    prevpath = path
    path = os.path.dirname(prevpath)
    
    if prevpath == path:
      break

    elif os.path.exists(os.path.join(path, '.top')):
      yield path


def env_export_top():
  from os import environ
  environ['TOP'] = next(find_top())


def main():
  for top in find_top():
    print(top)


if __name__ == '__main__':
  exit(main())
