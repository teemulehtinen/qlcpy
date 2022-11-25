texts = {
  'q_loop_end':
    lambda line: f'A program loop starts on line {line}. Which is the last line inside it?',
  'o_loop_end_correct': 'Correct, this is the last line inside the loop',
  'o_loop_end_before': 'The loop starts after this line',
  'o_loop_end_after': 'The loop ends before this line',
  'o_loop_end_inside': 'This line is inside the loop BUT it is not the last one',

  'q_variable_write_declaration':
    lambda var, line: (
      f'A value is assigned to variable <em>{var}</em> on line {line}. '
      f'On which line is <em>{var}</em> created?'
    ),
  'q_variable_read_declaration':
    lambda var, line: (
      f'A value is accessed from variable <em>{var}</em> on line {line}. '
      f'On which line is <em>{var}</em> created?',
    ),
  'q_variable_del_declaration':
    lambda var, line: (
      f'Variable <em>{var}</em> is deleted on line {line}. '
      f'On which line is <em>{var}</em> created?',
    ),
  'o_variable_declaration_correct': f'Correct, this is the line where the variable is created.',
  'o_variable_declaration_reference':
    f'This line references (reads or assigns) the given variable BUT it is created before',
  'o_variable_declaration_random': 'This is a random line that does not handle the given variable',
}