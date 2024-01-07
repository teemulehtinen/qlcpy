texts = {
  'q_variable_names': 'Which of the following are variable names in the program?',
  'o_variable_name': 'A variable in the program',
  'o_reserved_word': 'A reserved word in programming language',
  'o_built_in_function': 'A function that is built in to programming language',
  'o_unused_word': 'This word was not used in the program',
  'q_parameter_names':
    lambda line: f'Which of the following are parameter names of the function declared on line {line}?',
  'o_parameter_name': 'A parameter of the function',
  'o_function_name': 'A name of the function',

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
      f'On which line is <em>{id}</em> created?'
    ),
  'q_variable_del_declaration':
    lambda id, line: (
      f'Variable <em>{id}</em> is deleted on line {line}. '
      f'On which line is <em>{id}</em> created?'
    ),
  'o_variable_declaration_correct': 'Correct, this is the line where the variable is created.',
  'o_variable_declaration_reference':
    f'This line references (reads or assigns) the given variable BUT it is created before',
  'o_variable_declaration_random': 'This is a random line that does not handle the given variable',

  'q_except_source': lambda line: f'From which line program execution may continue to line {line}?',
  'o_except_source': 'Correct, this line can raise an error of the expected type.',
  'o_except_not_source': 'This line does NOT raise an error of the expected type.',
  'o_except_try_line': 'At least the first line inside try-block starts executing.',
  'o_except_outside_try': 'Except-block cannot be entered from outside the corresponding try-block.',

  'q_line_purpose': lambda line: f'Which of the following best describes the purpose of line {line}?',
  'o_line_purpose_read_input': 'Accepts new data',
  'o_line_purpose_zero_div_guard': 'Guards against division by zero',
  'o_line_purpose_end_condition': 'Is a condition for ending program',
  'o_line_purpose_ignores_input': 'Ignores unwanted input',
  'o_line_purpose_even_or_odd': 'Tells even and odd numbers apart',
  
  'q_variable_role':
    lambda id, line: (
      f'Which of the following best describes the role of variable <em>{id}</em> '
      f'that is created on line {line}?'
    ),
  'o_variable_dead': 'The variable is never accessed and could be removed',
  'o_variable_fixed': 'A <em>fixed value</em> that is not changed after created',
  'o_variable_stepper': 'A <em>stepper</em> that systematically goes through evenly spaced values',
  'o_variable_gatherer': 'A <em>gatherer</em> that combines new values to itself',
  'o_variable_holder': 'A <em>holder</em> that replaces it\'s value with the next acceptable value',

  'o_correct': 'Correct.',
  'o_incorrect': 'Incorrect.',

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