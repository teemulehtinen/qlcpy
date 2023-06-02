from typing import List

def find_first(words_list: List[str], initial: str) -> int:
  f = False
  for i in range(len(words_list)):
    if words_list[i].startswith(initial):
      return i

def count_average_of_even() -> None:
  s = 0
  n = 0
  word = None
  while word is None or word != '':
    word = input('Enter number or empty line to count average of even numbers')
    try:
      v = int(word)
      if v % 2 == 0:
        s += v
        n += 1
    except ValueError:
      print('Not a number')

  if n > 0:
    print('Average of even numbers', s / n)
  print('No even numbers')

while False:
  pass
