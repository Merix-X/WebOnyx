import json

def search(file, encoding, string):
  with open(file, encoding=encoding, mode='r') as fd:
    radky = fd.readlines()
    for radek in radky:
      cislo_radku = radky.index(radek)
      if radek.find(string) != -1:
        cislo_radku =+ 1   #Číslo řádku je C
        return cislo_radku, radek  #Celý přečtený řádek je radek
      else:
        continue
#Funkce search(file, encoding, string) vrací čísko řádku hledaného textu
# a celý přečtený řádek

def writeIndex(file: str, encoding: str, string: any, seek: int):
  with open(file, encoding=encoding, mode="a+") as fd:
    fd.seek(seek)
    obsah = fd.read()
    if len(obsah) > 0:
      fd.write("\n")
    fd.write(str(string))

def write_with_new_line(file: str, string: any):
  with open(file, encoding="utf-8", mode="a+") as fd:
    fd.seek(0)
    obsah = fd.read()
    if len(obsah) > 0:
      fd.write("\n")
    fd.write(str(string))


def write_no_new_line(file: str, string: any):
  with open(file, encoding="utf-8", mode="a+") as fd:
    fd.seek(0)
    fd.write(str(string))


def replace(replace_search, replace_write):
    with open("Hesla.txt", encoding="utf-8") as fd:
        obsah = fd.readlines()
        search = SearchIndex("Hesla.txt", "utf-8", replace_search)
        obsah[search] = replace_write

def SearchIndex(file, coding, string):
  with open(file, encoding=coding, mode='r') as soubor:
    obsah = soubor.readlines()
    for line in obsah:
      C = obsah.index(line)
      if line.find(string) != -1:
        return int(C)

def findLine(file, search_content):
  with open(file, 'r') as f:
    for i, line in enumerate(f, 1):
      if search_content in line:
        return i
  return None

def findLineString(file, search_content):
  with open(file, 'r') as f:
    for i, line in enumerate(f, 1):
      if search_content in line:
        return line
  return None

def replaceAll(file, search_content, new_content):
  line_number = findLine(file, search_content)

  if line_number is not None:
    updated_lines = []

    with open(file, 'r') as f:
      for i, line in enumerate(f, 1):
        if i == line_number:
          print(line, " -1-")
          updated_lines.append(new_content + '\n')
        else:
          updated_lines.append(line)
          print(line, " -2-")

    with open(file, 'w') as f:
      f.writelines(updated_lines)
      return "přepsáno"

  else:
    return "nepřepsáno"

def SearchString(file, string):
  with open(file, mode='r') as soubor:
    obsah = soubor.readlines()
    C = 0  # Inicializujeme proměnnou C mimo cyklus
    for line in obsah:
      if line.find(string) != -1:
        C += 1  # Zvýšíme C o 1, když nalezneme hledaný řetězec
        return bool(line)
  return None  # Pokud se řetězec nenalezne, vrací se None

def WriteBytes(file, string):
  with open(file, encoding="utf-8", mode="a+") as fd:
    fd.seek(0)
    obsah = fd.read()
    if len(obsah) > 0:
      fd.write("\n")
    fd.write(string)


def SearchStringAsBool(file, string):
  with open(file, mode='r') as soubor:
    obsah = soubor.readlines()
    for line in obsah:
      if string in line:
        return True, line  # Vrátíme nalezený řetězec a True
    return False  # Pokud není nalezen žádný řetězec, vrátíme False