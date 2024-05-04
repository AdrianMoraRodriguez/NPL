

def calcular_porcentaje(dataBase, classification):
  hits = 0
  actualField = 0
  actualRealClasification = []
  for i in range(len(dataBase)):
    if actualField == 0:
      actualField = 1
    elif actualField == 1:
      actualField = 2
    elif actualField == 2:
      actualRealClasification.append(dataBase[i])
      actualField = 0
  for i in range(len(classification) - 2):
    if actualRealClasification[i][0].lower() == classification[i].lower():
      hits += 1
  print("Porcentaje de aciertos: " + str(hits / len(classification) * 100) + "%")


def main():
  dataBaseFile = input("Enter the name of the file with the real classification: ")
  classificationFile = input("Enter the name of the file with the classification: ")
  with open(dataBaseFile, "r") as file:
    dataBase = file.read()
  with open(classificationFile, "r") as file:
    classification = file.read()
  dataBase = dataBase.split(";")
  dataBase = dataBase[3:]
  classification = classification.split("\n")
  calcular_porcentaje(dataBase, classification)


if __name__ == "__main__":
  main()
