texts = {
  'q_loop_end':
    lambda line: f'Toistorakenne alkaa riviltä {line}. Mikä on viimeinen rivi sen sisällä?',
  'o_loop_end_correct': 'Oikein, tämä on viimeinen rivi toistorakenteen sisällä',
  'o_loop_end_before': 'Toistorakenne alkaa tämän rivin jälkeen',
  'o_loop_end_after': 'Toistorakenne loppuu ennen tätä riviä',
  'o_loop_end_inside': 'Tämä rivi on toistorakenteen sisällä, MUTTA se ei ole viimeinen rivi',

  'q_variable_write_declaration':
    lambda id, line: (
      f'Muuttujaan <em>{id}</em> asetetaan arvo rivillä {line}. '
      f'Millä rivillä <em>{id}</em> luodaan?'
    ),
  'q_variable_read_declaration':
    lambda id, line: (
      f'Muuttujasta <em>{id}</em> luetaan arvo rivillä {line}. '
      f'Millä rivillä <em>{id}</em> luodaan?',
    ),
  'q_variable_del_declaration':
    lambda id, line: (
      f'Muuttuja <em>{id}</em> poistetaan rivillä {line}. '
      f'Millä rivillä <em>{id}</em> luodaan?',
    ),
  'o_variable_declaration_correct': 'Oikein, annettu muuttuja luodaan tällä rivillä.',
  'o_variable_declaration_reference':
    'Tämä rivi viittaa (lukee tai sijoittaa) annettuun muuttujaan, MUTTA se luodaan aiemmin',
  'o_variable_declaration_random': 'Tämä on satunnainen rivi, joka ei käsittele annettua muuttujaa',

  'q_loop_count':
    lambda line: (
      f'Rivillä {line} on toistorakenne. Kuinka monta kertaa toisto suoritetaan, '
      'kun ohjelma ajetaan.'
    ),
  'q_loop_count_call':
    lambda line, call: (
      f'Rivillä {line} on toistorakenne. Kuinka monta kertaa toisto suoritetaan, '
      f'kun ajetaan <em>{call}</em>?'
    ),
  'o_loop_count_correct': 'Oikein, näin monta kertaa toisto tapahtui',
  'o_loop_count_one_off': 'Tämä lukumäärä heittää yhdellä oikeasta.',
  'o_loop_count_random': 'Tämä on satunnainen väärä lukumäärä',

  'q_variable_trace':
    lambda id, line: (
      f'Rivillä {line} määritellään muuttuja <em>{id}</em>. Mitkä arvot ja missä ',
      'järjestyksessä siihen sijoitetaan, kun ohjelma ajetaan.'
    ),
  'q_variable_trace_call':
    lambda id, line, call: (
      f'Rivillä {line} määritellään muuttuja <em>{id}</em>. Mitkä arvot ja missä järjestyksessä '
      f'siihen sijoitetaan, kun ajetaan <em>{call}</em>?'
    ),
  'o_variable_trace_correct': 'Oikein, nämä arvot sijoitettiin tässä järjestyksessä muuttujaan.',
  'o_variable_trace_miss': 'Tästä sarjasta puuttuu muuttujaan sijoitettu arvo.',
  'o_variable_trace_random': 'Tämä on satunnainen väärä arvojen sarja.',

  'q_variable_trace_start':
    lambda id, line: (
      f'Rivillä {line} määritellään muuttuja <em>{id}</em>. Mitkä ovat 4 ensimmäistä arvoa, '
      'jotka siihen sijoitetaan annetussa järjestyksessä, kun ohjelma ajetaan?'
    ),
  'q_variable_trace_start_call':
    lambda id, line, call: (
      f'Rivillä {line} määritellään muuttuja <em>{id}</em>. Mitkä ovat 4 ensimmäistä arvoa, '
      f'jotka siihen sijoitetaan annetussa järjestyksessä, kun ajetaan <em>{call}</em>?'
    ),
  'o_variable_trace_start_correct': 'Oikein, ensimmäiseksi muuttujaan sijoitettiin nämä 4 arvoa tässä järjestyksessä.',
  'o_variable_trace_start_random': 'Tämä on satunnainen väärä arvojen sarja.',
}
