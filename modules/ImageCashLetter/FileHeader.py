import io
from modules import read_json
from pprint import pprint
from config import MODULES_DIR
import ebcdic

PATH = MODULES_DIR+"/ImageCashLetter"
STRUCTURE = read_json(PATH+"/X9Structure/X9.100-187-2008.json")['FileHeader']
RULES = STRUCTURE["rules"]
POSITIONS = STRUCTURE["positions"]
DATA = read_json(PATH+"/X9Structure/example.local.json")['FileHeader']
OUTPUT = io.StringIO()

def init():
  try:
    set_record_type()
    write()
    writeOnFileEncoded()

  except Exception as err:
    print(str(err))

def set_record_type():
  DATA['recordType'] = STRUCTURE['type']

def set_parser(keyname:str):
  size = get_dimension(POSITIONS[keyname])
  justify = RULES[keyname]['align']

  if type(DATA[keyname]) == int:
    DATA[keyname] = str(DATA[keyname]).zfill(size)
  else:
    DATA[keyname] = DATA[keyname].ljust(size) if justify == "left" else DATA[keyname].rjust(size)

def get_dimension(position:str)->int:
  sep = position.split(":")
  sep[0] = int(sep[0]) - 1
  sep[1] = int(sep[1])
  return sep[1] - sep[0]

def write():
  for keyname in DATA:
    validate_values(keyname)
    set_parser(keyname)
    writeOnBuffer(keyname)

def writeOnBuffer(keyname):
  OUTPUT.write(DATA[keyname])

def writeOnFileEncoded(filename='test.dat'):
  output = OUTPUT.getvalue()
  output = output.encode('cp1148')
  f = open(filename, "ab")
  f.write(output)
  f.close()

def validate_values(keyname)->None:
  if(type(DATA[keyname]) != eval(RULES[keyname]['type'])):
    raise ValueError(RULES[keyname]['message'])

init()
