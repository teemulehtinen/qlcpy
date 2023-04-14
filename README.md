# QLCpy

Generates questions about concrete constructs and patterns in a given Python
program. These questions (including answering options) can be posed to a
learner to practice introductory programming. These questions include elements
to develop program comprehension and program tracing.

Automatic generation enables systems to pose the generated questions to leaners
about their own programs that they previously programmed. Such Questions About
Learners' Code (QLCs) may have self-reflection and self-explanation effects
that are of interest in computing education research.

### References

The concept of Questions About Learners' Code (QLCs) is first introduced by Lehtinen et al. in
[Let's Ask Students About Their Programs, Automatically](https://doi.org/10.1109/ICPC52881.2021.00054).

---

### Example result

For the file [test/sample_code.py](test/sample_code.py):
```python
    from typing import List

    def find_first(words_list: List[str], initial: str) -> int:
      f = False
      for i in range(len(words_list)):
        if words_list[i].startswith(initial):
        return i

    def count_average() -> None:
      s = 0
      n = 0
      word = None
      while word is None or word != '':
        word = input('Enter number or empty line to count average')
        try:
          s += int(word)
          n += 1
        except ValueError:
          print('Not a number')
      if n > 0:
        print('Average', s / n)
      print('No numbers')
```

We use the CLI to create one question of each available type:
```
     % qlcpy test/sample_code.py --call 'find_first(["lorem", "ipsum", "dolor", "sit", "amet"], "s")' -n 9 --unique
    Which of the following are variable names in the program? [VariableNames]
      if: A reserved word in programming language [reserved_word]
      input: A function that is built in to programming language [builtin_function]
    * n: A variable in the program [variable]
      other: This word was not used in the program [unused_word]
    * word: A variable in the program [variable]

    Which of the following are parameter names of the function declared on line 3? [ParameterNames]
      f: A variable in the program [variable]
      find_first: A name of the function [function]
      i: A variable in the program [variable]
    * initial: A parameter of the function [parameter]
    * words_list: A parameter of the function [parameter]

    A program loop starts on line 5. Which is the last line inside it? [LoopEnd]
      4: The loop starts after this line [line_before_block]
      6: This line is inside the loop BUT it is not the last one [line_inside_block]
    * 7: Correct, this is the last line inside the loop [last_line_inside_block]
      8: The loop ends before this line [line_after_block]

    A value is accessed from variable <em>i</em> on line 6. On which line is <em>i</em> created? [VariableDeclaration]
      4: This is a random line that does not handle the given variable [random_line]
    * 5: Correct, this is the line where the variable is created. [declaration_line]
      6: This line references (reads or assigns) the given variable BUT it is created before [reference_line]
      7: This line references (reads or assigns) the given variable BUT it is created before [reference_line]

    From which line program execution may continue to line 18? [ExceptSource]
      13: Except-block cannot be entered from outside the corresponding try-block. [before_try_block]
      15: At least the first line inside try-block starts executing. [try_line]
    * 16: Correct, this line can raise an error of the expected type. [source_line]
      17: This line does NOT raise an error of the expected type. [not_source_line]

    Which of the following best describes the purpose of line 13? [LinePurpose]
      Accepts new data: Incorrect. [read_input]
      Guards against division by zero: Incorrect. [zero_div_guard]
      Ignores unwanted input: Incorrect. [ignores_input]
    * Is a condition for ending program: Correct. [end_condition]

    Which of the following best describes the role of variable <em>s</em>that is created on line 10? [VariableRole]
      A <em>fixed value</em> that is not changed after created: Incorrect. [fixed]
    * A <em>gatherer</em> that combines new values to itself: Correct. [gatherer]
      A <em>stepper</em> that systematically goes through evenly spaced values: Incorrect. [stepper]
      The variable is never accessed and could be removed: Incorrect. [dead]

    Line 5 has a loop structure. How many times does the loop execute when running <em>find_first(["lorem", "ipsum", "dolor", "sit", "amet"], "s")</em>? [LoopCount]
    * 4: Correct, this is the number of times the loop executed. [correct_count]
      5: This number is off by one. [one_off_count]
      6: This is an incorrect, random number. [random_count]
      7: This is an incorrect, random number. [random_count]

    Line 5 declares a variable named <em>i</em>. Which values and in which order are assigned to the variable when running <em>find_first(["lorem", "ipsum", "dolor", "sit", "amet"], "s")</em>? [VariableTrace]
      0, 1, 2: This sequence is missing a value that was assigned to the variable. [miss_value]
    * 0, 1, 2, 3: Correct, these values were assigned in this order to the variable. [correct_trace]
      3, 1, 0, 2: This is an incorrect, random sequence of values. [random_values]
      3, 1, 2: This is an incorrect, random sequence of values. [random_values]
```

---

### Installation

    pip install qlcpy

### Usage

The package offers a CLI for test prints as well as JSON output. See the example section
above for example output. Below is the usage instruction from the command.
```
     % qlcpy --help
    usage: __main__.py [-h] [-m] [-c CALL] [-sc SILENT_CALL] [-i INPUT] [-n N]
                       [-t TYPES [TYPES ...]] [-u] [-l LANG] [--json]
                       [--list-types]
                       [program]

    QLCpy generates questions that target analysed facts about the given program

    positional arguments:
      program               A python program file

    optional arguments:
      -h, --help            show this help message and exit
      -m, --main            Run with "__name__" = "__main__"
      -c CALL, --call CALL  A python call to execute
      -sc SILENT_CALL, --silent-call SILENT_CALL
                            A python call to execute silently without including it
                            in the question prompts
      -i INPUT, --input INPUT
                            A text file to use as stdin
      -n N                  Number of questions (at maximum)
      -t TYPES [TYPES ...], --types TYPES [TYPES ...]
                            Only these question types
      -u, --unique          Only unique question types
      -l LANG, --lang LANG  Language code for the text (en, fi)
      --json                Print question data as JSON
      --list-types          List available question types
```

For programmatic integration the library offers a [generate](qlcpy/generator.py#L22)
function that offers the same generation options as the CLI command. Type hints are
included and [models.py](qlcpy/models.py) describes the input and output data. Below
is an example python program using the library.
```python
    import qlcpy
    
    with open('test/sample_code.py', 'r') as f:
      src = f.read()
    
    qlcs = qlcpy.generate(
        src,
        [
            qlcpy.QLCRequest(1, types=['LoopCount', 'VariableTrace']),
            qlcpy.QLCRequest(10, fill=True, unique_types=True),
        ],
        call='find_first(["lorem", "ipsum", "dolor", "sit", "amet"], "s")',
    )

    for qlc in qlcs:
        print(f'{qlc.question} = {", ".join(str(o.answer) for o in qlc.options if o.correct)}')
    
    import json
    print(json.dumps(list(qlc.to_dict() for qlc in qlcs)))
```