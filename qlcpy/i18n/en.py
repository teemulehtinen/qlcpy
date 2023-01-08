texts = {
  'q_loop_end':
    lambda line: f'A program loop starts on line {line}. Which is the last line inside it?',
  'o_loop_end_correct': 'Correct, this is the last line inside the loop',
  'o_loop_end_before': 'The loop starts after this line',
  'o_loop_end_after': 'The loop ends before this line',
  'o_loop_end_inside': 'This line is inside the loop BUT it is not the last one',

  'q_variable_write_declaration':
    lambda id, line: (
      f'A value is assigned to variable <em>{id}</em> on line {line}. '
      f'On which line is <em>{id}</em> created?'
    ),
  'q_variable_read_declaration':
    lambda id, line: (
      f'A value is accessed from variable <em>{id}</em> on line {line}. '
      f'On which line is <em>{id}</em> created?',
    ),
  'q_variable_del_declaration':
    lambda id, line: (
      f'Variable <em>{id}</em> is deleted on line {line}. '
      f'On which line is <em>{id}</em> created?',
    ),
  'o_variable_declaration_correct': 'Correct, this is the line where the variable is created.',
  'o_variable_declaration_reference':
    f'This line references (reads or assigns) the given variable BUT it is created before',
  'o_variable_declaration_random': 'This is a random line that does not handle the given variable',

  'q_loop_count':
    lambda line: (
      f'Line {line} has a loop structure. How many times does the loop execute '
      'when the program is run.'
    ),
  'q_loop_count_call':
    lambda line, call: (
      f'Line {line} has a loop structure. How many times does the loop execute '
      f'when running <em>{call}</em>?'
    ),
  'o_loop_count_correct': 'Correct, this is the number of times the loop executed.',
  'o_loop_count_one_off': 'This number is off by one.',
  'o_loop_count_random': 'This is an incorrect, random number.',

  'q_variable_trace':
    lambda id, line: (
      f'Line {line} declares a variable named <em>{id}</em>. Which values and in which '
      'order are assigned to the variable when the program is run?'
    ),
  'q_variable_trace_call':
    lambda id, line, call: (
      f'Line {line} declares a variable named <em>{id}</em>. Which values and in which '
      f'order are assigned to the variable when running <em>{call}</em>?'
    ),
  'o_variable_trace_correct': 'Correct, these values were assigned in this order to the variable.',
  'o_variable_trace_miss': 'This sequence is missing a value that was assigned to the variable.',
  'o_variable_trace_random': 'This is an incorrect, random sequence of values.',

  'q_variable_trace_start':
    lambda id, line: (
      f'Line {line} declares a variable named <em>{id}</em>. Which are the first 4 values '
      'that are assigned to the variable in the given order when the program is run?'
    ),
  'q_variable_trace_start_call':
    lambda id, line, call: (
      f'Line {line} declares a variable named <em>{id}</em>. Which are the first 4 values '
      f'that are assigned to the variable in the given order when running <em>{call}</em>?'
    ),
  'o_variable_trace_start_correct': 'Correct, these 4 values where first assigned in this order to the variable.',
  'o_variable_trace_start_random': 'This is an incorrect, random sequence of values.',
}