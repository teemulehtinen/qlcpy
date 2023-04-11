from typing import List

def find_first(words_list: List[str], initial: str) -> None:
  for i in range(len(words_list)):
    if words_list[i].startswith(initial):
      print(i)

def find_first_w(words_list: List[str], initial: str) -> int:
  j = 0
  while j < len(words_list):
    if words_list[j].startswith(initial):
      return j
    j += 1
  return -1

def is_a_number(n):
  try:
    v = int(n)
    return True
  except ValueError:
    return False
