# Copyright 2019 Josh Bialkowski <josh.bialkowski@gmail.com>

from docutils import nodes, statemachine
from docutils.parsers.rst import directives, states
from docutils.statemachine import StringList

VERSION = "0.1.0"

def run_fence_as_directive(self, match, **option_presets):
    # NOTE(josh): copied from directive()
    type_name = "code"
    directive_class, messages = directives.directive(
        type_name, self.memo.language, self.document)
    self.parent += messages
    if not directive_class:
        return self.unknown_directive(type_name)

    # NOTE(josh): copied from run_directive():
    lineno = self.state_machine.abs_line_number()
    initial_line_offset = self.state_machine.line_offset
    # NOTE(josh): changed this from get_first_known_indented to
    # get_first_known_indented_until, which I wrote (well, sorta... I mean
    # I mostly copied the original function).
    indented, indent, line_offset, blank_finish \
              = self.state_machine.get_first_known_indented_until(
                    match.start(), match.group(0))

    padded = StringList()
    # padded += indented[0:1]
    # First line contains any optional arguments (in this case, language)
    padded += StringList([indented[0][3:]])
    # TODO(josh): check to see if there are any options specified, such
    # as :number-lines:, :class:, :name:.
    # Second line must be blank
    padded += StringList([""])
    padded += indented[1:-1]
    padded += StringList([""])
    # padded += indented[-1:]
    blank_finish = True

    # NOTE(josh): +1 to start, -1 to stop index, as compared to the usual
    # directive parsing. Also added a newline to the start
    block_text = '\n'.join(self.state_machine.input_lines[
        initial_line_offset + 1 : self.state_machine.line_offset])
    try:
        arguments, options, content, content_offset = (
            self.parse_directive_block(padded, line_offset,
                                        directive_class, option_presets))
    except MarkupError as detail:
        error = self.reporter.error(
            'Error in "%s" directive:\n%s.' % (type_name,
                                                ' '.join(detail.args)),
            nodes.literal_block(block_text, block_text), line=lineno)
        return [error], blank_finish

    directive_instance = directive_class(
        type_name, arguments, options, content, lineno,
        content_offset, block_text, self, self.state_machine)
    try:
        result = directive_instance.run()
    except docutils.parsers.rst.DirectiveError as error:
        msg_node = self.reporter.system_message(error.level, error.msg,
                                                line=lineno)
        msg_node += nodes.literal_block(block_text, block_text)
        result = [msg_node]
    assert isinstance(result, list), \
            'Directive "%s" must return a list of nodes.' % type_name
    for i in range(len(result)):
        assert isinstance(result[i], nodes.Node), \
                ('Directive "%s" returned non-Node object (index %s): %r'
                % (type_name, i, result[i]))
    return (result,
            blank_finish or self.state_machine.is_next_line_blank())


def fence(self, match, context, next_state):
    """Code fences."""
    nodelist, blank_finish = self.run_fence_as_directive(match)
    self.parent += nodelist
    self.explicit_list(blank_finish)
    return [], next_state, []



def get_first_known_indented_until(self, indent, sentinel,
                                    strip_indent=True):
    """
    Return an indented block and info up to and including the first
    occurance of `sentinel`.

    Extract an indented block where the indent is known for the first line
    and unknown for all other lines.

    :Parameters:
        - `indent`: The first line's indent (# of columns/characters).
        - `until_blank`: Stop collecting at the first blank line if true
          (1).
        - `strip_indent`: Strip `indent` characters of indentation if true
          (1, default).
        - `strip_top`: Strip blank lines from the beginning of the block.

    :Return:
        - the indented block,
        - its indent,
        - its first line offset from BOF, and
        - whether or not it finished with a blank line.
    """
    offset = self.abs_line_offset()
    indented, indent, blank_finish = self.input_lines.get_indented_until(
          sentinel, self.line_offset, strip_indent,
          first_indent=indent)
    self.next_line(len(indented) - 1) # advance to last indented line
    return indented, indent, offset, blank_finish

def get_indented_until(self, sentinel, start=0, strip_indent=True,
                        block_indent=None, first_indent=None):
    """
    Extract and return a StringList of indented lines of text up to and
    including the first occurance of `sentinel`.

    Collect all lines with indentation, determine the minimum indentation,
    remove the minimum indentation from all indented lines (unless
    `strip_indent` is false), and return them. All lines up to but not
    including the first unindented line will be returned.

    :Parameters:
      - `start`: The index of the first line to examine.
      - `until_blank`: Stop collecting at the first blank line if true.
      - `strip_indent`: Strip common leading indent if true (default).
      - `block_indent`: The indent of the entire block, if known.
      - `first_indent`: The indent of the first line, if known.

    :Return:
      - a StringList of indented lines with mininum indent removed;
      - the amount of the indent;
      - a boolean: did the indented block finish with a blank line or EOF?
    """
    indent = block_indent           # start with None if unknown
    end = start
    if block_indent is not None and first_indent is None:
        first_indent = block_indent
    if first_indent is not None:
        end += 1
    last = len(self.data)
    while end < last:
        line = self.data[end]
        stripped = line.lstrip()
        if block_indent is None:
            line_indent = len(line) - len(stripped)
            if indent is None:
                indent = line_indent
            else:
                indent = min(indent, line_indent)
        end += 1
        if stripped.startswith(sentinel):
            break

    block = self[start:end]
    if first_indent is not None and block:
        block.data[0] = block.data[0][first_indent:]
    if indent and strip_indent:
        block.trim_left(indent, start=(first_indent is not None))
    return block, indent or 0, False


def monkeypatch_docutils():
  states.Body.patterns["fence"] = r"[`~]{3}"

  templist = list(states.Body.initial_transitions)
  templist.insert(9, "fence")
  states.Body.initial_transitions = tuple(templist)
  states.Body.fence = fence
  states.Body.run_fence_as_directive = run_fence_as_directive

  statemachine.StateMachineWS.get_first_known_indented_until = \
      get_first_known_indented_until
  statemachine.StringList.get_indented_until = get_indented_until

def setup(app):
  monkeypatch_docutils()
