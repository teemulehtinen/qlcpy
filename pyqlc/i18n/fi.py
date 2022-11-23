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
}
