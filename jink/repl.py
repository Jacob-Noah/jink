import sys
from jink.lexer import Lexer
from jink.parser import Parser
from jink.optimizer import optimize
from jink.interpreter import Interpreter
from jink.utils.classes import Environment


class REPL:
  def __init__(self, stdin, stdout, environment=Environment(), lexer=Lexer(), parser=Parser(), interpreter=Interpreter()):
    self.stdin = stdin
    self.stdout = stdout
    self.env = environment
    self.lexer = lexer
    self.parser = parser
    self.interpreter = interpreter

  def main_loop(self):
    while True:
      self.stdout.write("> ")
      self.stdout.flush()
      try:
        line = input()
      except KeyboardInterrupt:
        sys.exit(0)
      if not line:
        break
      self.run(line)

  def run(self, code):
    try:
      lexed = self.lexer.parse(code)
      if len(lexed) == 1 and lexed[0].type == 'ident':
        var = self.env.get_var(lexed[0].text)
        ret = var['value'] if var != None and isinstance(var, (dict)) else var or 'null'
        print(ret)
      else:
        AST = optimize(self.parser.parse(lexed))
        e = self.interpreter.evaluate(AST, self.env)
        if len(e) == 1:
          print(e[0] if e[0] is not None else 'null')
        else:
          print(e[0] if e[0] is not None else 'null')
    except Exception as exception:
      print("Exception: {}".format(exception))
