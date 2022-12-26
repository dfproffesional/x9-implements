def read_json(json:dict):
  return read_file_header(json['FileHeader'])

def read_file_header(json:dict):
  from modules.ImageCashLetter import FileHeader
  
  if not json:
    raise Exception('Not found FileHeader')
  
  FileHeader.set_data(json,None)
  FileHeader.init()
  return FileHeader.get_buffer_data()

