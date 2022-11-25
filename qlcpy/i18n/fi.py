texts = {
  'q_loop_end':
    lambda line: f'Toistorakenne alkaa riviltä {line}. Mikä on viimeinen rivi sen sisällä?',
  'o_loop_end_correct': 'Oikein, tämä on viimeinen rivi toistorakenteen sisällä',
  'o_loop_end_before': 'Toistorakenne alkaa tämän rivin jälkeen',
  'o_loop_end_after': 'Toistorakenne loppuu ennen tätä riviä',
  'o_loop_end_inside': 'Tämä rivi on toistorakenteen sisällä, MUTTA se ei ole viimeinen rivi',

  'q_variable_write_declaration':
    lambda var, line: (
      f'Muuttujaan <em>{var}</em> asetetaan arvo rivillä {line}. '
      f'Millä rivillä <em>{var}</em> luodaan?'
    ),
  'q_variable_read_declaration':
    lambda var, line: (
      f'Muuttujasta <em>{var}</em> luetaan arvo rivillä {line}. '
      f'Millä rivillä <em>{var}</em> luodaan?',
    ),
  'q_variable_del_declaration':
    lambda var, line: (
      f'Muuttuja <em>{var}</em> poistetaan rivillä {line}. '
      f'Millä rivillä <em>{var}</em> luodaan?',
    ),
  'o_variable_declaration_correct': f'Oikein, annettu muuttuja luodaan tällä rivillä.',
  'o_variable_declaration_reference':
    f'Tämä rivi viittaa (lukee tai sijoittaa) annettuun muuttujaan, MUTTA se luodaan aiemmin',
  'o_variable_declaration_random': 'Tämä on satunnainen rivi, joka ei käsittele annettua muuttujaa',

  'q_loop_count':
    lambda line: f'Rivillä {line} on toistorakenne. Kuinka monta kertaa toisto suoritetaan?',
  'q_loop_count_call':
    lambda line, call: (
      f'Rivillä {line} on toistorakenne. Kuinka monta kertaa toisto suoritetaan '
      f'kutsuttaessa <em>{call}</em>?'
    ),
  'o_loop_count_correct': f'Oikein, näin monta kertaa toisto tapahtui',
  'o_loop_count_random': f'Tämä on satunnainen väärä lukumäärä',
}
