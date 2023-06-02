texts = {
  'q_variable_names': 'Mitkä seuraavista ovat muuttujien nimiä ohjelmassa?',
  'o_variable_name': 'Muuttuja tässä ohjelmassa',
  'o_reserved_word': 'Varattu sana ohjelmointikielessä',
  'o_built_in_function': 'Funktio, joka on määritelty ohjelmointikielen sisään',
  'o_unused_word': 'Käyttämätön sana tässä ohjelmassa',
  'q_parameter_names':
    lambda line: f'Mitkä seuraavista ovat rivillä {line} määritellyn funktion parametrien nimiä?',
  'o_parameter_name': 'Funktion parametri',
  'o_function_name': 'Funktion nimi',

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
      f'Millä rivillä <em>{id}</em> luodaan?'
    ),
  'q_variable_del_declaration':
    lambda id, line: (
      f'Muuttuja <em>{id}</em> poistetaan rivillä {line}. '
      f'Millä rivillä <em>{id}</em> luodaan?'
    ),
  'o_variable_declaration_correct': 'Oikein, annettu muuttuja luodaan tällä rivillä.',
  'o_variable_declaration_reference':
    'Tämä rivi viittaa (lukee tai sijoittaa) annettuun muuttujaan, MUTTA se luodaan aiemmin',
  'o_variable_declaration_random': 'Tämä on satunnainen rivi, joka ei käsittele annettua muuttujaa',

  'q_except_source': lambda line: f'Miltä riviltä ohjelman suoritus voi siirtyä riville {line}?',
  'o_except_source': 'Oikein, tämä rivi voi nostaa odotettua tyyppiä olevan virheen.',
  'o_except_not_source': 'Tämä rivi EI voi nostaa odotettua tyyppiä olevaa virhettä.',
  'o_except_try_line': 'Vähintään try-lohkon ensimmäistä riviä aletaan suorittaa.',
  'o_except_outside_try': 'Except-lohkoon ei voida siirtyä vastaavan try-lohkon ulkopuolelta.',

  'q_line_purpose': lambda line: f'Mikä seuraavista kuvaa parhaiten rivin {line} tarkoitusta?',
  'o_line_purpose_read_input': 'Vastaanottaa uutta dataa',
  'o_line_purpose_zero_div_guard': 'Suojaa nollalla jakamiselta',
  'o_line_purpose_end_condition': 'On ehto ohjelman loppumiselle',
  'o_line_purpose_ignores_input': 'Ohittaa ei halutun syötteen',
  'o_line_purpose_even_or_odd': 'Erottelee parilliset ja parittomat numerot',

  'q_variable_role':
    lambda id, line: (
      f'Mikä seuraavista kuvaa parhaiten rivillä {line} luodun muuttujan <em>{id}</em> roolia?'
    ),
  'o_variable_dead': 'Muuttujaa ei koskaan lueta ja se voitaisiin poistaa',
  'o_variable_fixed': '<em>Kiintoarvo</em>, jota ei muuteta luomisen jälkeen',
  'o_variable_stepper': '<em>Askeltaja</em>, joka käy systemaattisesti läpi tasavälisiä arvoja',
  'o_variable_gatherer': '<em>Kokooja</em>, joka yhdistää itseensä uusia arvoja',
  'o_variable_holder': '<em>Säilyttäjä</em>, joka korvaa arvonsa seuraavaksi kelpaavalla arvolla',

  'o_correct': 'Oikein.',
  'o_incorrect': 'Väärin.',

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
