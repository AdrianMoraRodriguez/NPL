
def main():
  with open("PH_train.csv", "r") as file:
    texto = file.read()
  texto = texto.replace("\n", " ")
  texto = texto.lower()
  fields = texto.split(";")
  actualField = 0
  emails = {}
  number = 0
  email = ""
  header = fields[0] + ";" + fields[1] + ";" + fields[2] + ";\n"
  fields = fields[3:]
  for i in range(len(fields)):
    if actualField == 0:
      number = fields[i][1:]
      actualField = 1
    elif actualField == 1:
      email = fields[i]
      actualField = 2
      emails[number] = email
    elif actualField == 2:
      emails[number] = [email, fields[i]]
      actualField = 0
  # Dividir el texto en dos, en uno los primeros 10000 emails y en otro los restantes
  emails1 = {}
  emails2 = {}
  for key in emails:
    if int(key) < 10000:
      emails1[key] = emails[key]
    else:
      emails2[key] = emails[key]
  # Guardar los emails en dos archivos
  with open("PH_train1.csv", "w") as file:
    file.write(header)
    for key in emails1:
      file.write(key + ";" + emails1[key][0] + ";" + emails1[key][1] + ";\n")
  with open("PH_train2.csv", "w") as file:
    file.write(header)
    for key in emails2:
      file.write(key + ";" + emails2[key][0] + ";" + emails2[key][1] + ";\n")
  print("Created PH_train1.csv and PH_train2.csv files.")



if __name__ == "__main__":
  main()