import typing

def autoGreet() -> str:
  return greeting("12")

def greeting(name: str) -> str:
  return "hi {0}".format(name)

def p() -> int:
  print("hi")
  return 1

if __name__ == '__main__':
  print(autoGreet())
  a = p()