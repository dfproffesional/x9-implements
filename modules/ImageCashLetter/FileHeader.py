import io
from modules import read_json
from pprint import pprint
from config import MODULES_DIR

# Directories and files
PATH = MODULES_DIR+"/ImageCashLetter"
STRUCTURE = read_json(PATH+"/X9Structure/X9.100-187-2008.json")['FileHeader']

# Rules
RULES = STRUCTURE["rules"]
POSITIONS = STRUCTURE["positions"]

# Default Data:
# Example: DATA = read_json(PATH+"/X9Structure/example.local.json")['FileHeader']
DATA = {'recordType': None}
OUTPUT = io.StringIO()

def init()->None:
  __set_record_type()
  __write()
  __write_on_file_encoded()

def set_data(data:dict, memory_info:str )->None:
  global DATA,OUTPUT
  DATA = {**DATA,**data}
  OUTPUT = io.StringIO()

def set_structure(name:str)->None:
  global STRUCTURE,RULES,POSITIONS
  STRUCTURE = read_json(PATH+"/X9Structure/X9."+name+".json")['FileHeader']
  RULES = STRUCTURE["rules"]
  POSITIONS = STRUCTURE["positions"]

def get_buffer_data()->str:
  return OUTPUT.getvalue()

def get_data()->dict:
  return DATA

def __set_record_type()->None:
  DATA['recordType'] = STRUCTURE['type']

def __set_parser(keyname:str):
  size = __get_dimension(keyname)
  justify = __get_align(keyname)
  if type(DATA[keyname]) == int:
    DATA[keyname] = str(DATA[keyname]).zfill(size)
  else:
    DATA[keyname] = DATA[keyname].ljust(size) if justify == "left" else DATA[keyname].rjust(size)

def __get_align(keyname):
  return RULES[keyname]['align']

def __get_dimension(keyname:str)->int:
  sep = POSITIONS[keyname].split(":")
  sep[0] = int(sep[0]) - 1
  sep[1] = int(sep[1])
  return sep[1] - sep[0]

def __write():
  for keyname in DATA:
    __validate_values(keyname)
    __set_parser(keyname)
    __write_on_buffer(keyname)

def __write_on_buffer(keyname):
  OUTPUT.write(DATA[keyname])

def __write_on_file_encoded(filename='test.dat'):
  import ebcdic
  output = OUTPUT.getvalue()
  output = output.encode('cp1148')
  f = open(filename, "ab")
  f.write(output)
  f.close()

def __validate_values(keyname)->None:
  if(type(DATA[keyname]) != eval(RULES[keyname]['type'])):
    raise ValueError(RULES[keyname]['message'])