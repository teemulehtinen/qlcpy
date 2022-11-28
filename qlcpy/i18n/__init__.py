from typing import Any, List

from . import en, fi

# No languages implemented
lang = 'en'

texts = {
  'en': en.texts,
  'fi': fi.texts,
}

def t(key: str, *args: Any) -> str:
  txt = texts[lang][key]
  if callable(txt):
    return txt(*args)
  return txt
