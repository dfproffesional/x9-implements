def read_json(filename:str)->dict:
  import json
  return json.loads(get_file_content(filename))

def get_file_content(filename:str)->str:
  # open file
  file = open(filename,'rb')
  # get content
  content = file.read()
  # close file
  file.close()

  return content