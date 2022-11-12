from typing import List

def find_first(words_list: List[str], initial: str) -> None:
  for i in range(len(words_list)):
    if words_list[i].startswith(initial):
      print(i)

def find_first_w(words_list: List[str], initial: str) -> int:
  i = 0
  while i < len(words_list):
    if words_list[i].startswith(initial):
      return i
    i += 1
  return -1
