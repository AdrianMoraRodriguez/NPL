
def main():
  filename = input("Enter the name of the corpus file: ")
  with open(filename, "r") as file:
    texto = file.read()
  # En una línea hay esto: Palabra: 0 Frec: 2033 LogProb:-6.290352040258224, quiero sacar el número de la frecuencia
  frecuencias = {}
  texto = texto.split("\n")
  texto = texto[2:]
  for i in range(len(texto)):
    if texto[i] == "":
      continue
    palabra = texto[i].split(" ")
    frecuencias[palabra[1]] = palabra[3]
    
  # Sumar todas las frecuencias
  suma = 0
  for key in frecuencias:
    suma += int(frecuencias[key])
  print("La suma de las frecuencias es: " + str(suma))

if __name__ == "__main__":
  main()