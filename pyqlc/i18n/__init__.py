from typing import Any, List

from . import en, fi

# No languages implemented
locale = 'fi'

texts = {
  'en': en.texts,
  'fi': fi.texts,
}

def t(key: str, *args: Any) -> str:
  txt = texts[locale][key]
  if callable(txt):
    return txt(*args)
  return txt
