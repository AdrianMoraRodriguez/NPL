def main():
  filename = input("Enter the name of the original files: ")
  with open(filename, "r") as file:
    texto = file.read()
  fields = texto.split(";")
  actualField = 0
  phishing = {}
  safe = {}
  for i in range(len(fields)):
    if actualField == 0:
      number = fields[i][1:]
      actualField = 1
    elif actualField == 1:
      email = fields[i]
      actualField = 2
    elif actualField == 2:
      if fields[i] == "Safe Email" or fields[i] == "safe email":
        safe[number] = [email, fields[i]]
      elif fields[i] == "Phishing Email" or fields[i] == "phishing email":
        phishing[number] = [email, fields[i]]
      actualField = 0
  #Poner en un archivo los correos phishing y en otro los correos seguros
  filename = input("Enter the name of the file to save the phishing emails: ")
  with open(filename, "w") as file:
    for key in phishing:
      file.write(key + ";" + phishing[key][0] + ";" + phishing[key][1] +  ";" + "\n")
  print("Created " + filename + " file")
  filename = input("Enter the name of the file to save the safe emails: ")
  with open(filename, "w") as file:
    for key in safe:
      file.write(key + ";" + safe[key][0] + ";" + safe[key][1] +  ";" + "\n")
  print("Created " + filename + " file")

if __name__ == "__main__":
  main()