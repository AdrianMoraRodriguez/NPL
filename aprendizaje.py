import math
import string
import nltk
import emoji
import re
#import enchant


#nltk.download('stopwords') #Descomentar si es la primera vez que se ejecuta
#nltk.download('punkt')     #Descomentar si es la primera vez que se ejecuta
#nltk.download('wordnet')   #Descomentar si es la primera vez que se ejecuta

from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

def process_text(text, stem=True):
  tokens = word_tokenize(text)
  if stem:
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
  return tokens

def preprocessCorpus(corpus):
  url_regex = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
  html_tag_regex = "<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>"
  control_characters_regex = "[\x00-\x1F\x7F]"
  corpus = corpus.split("\n")
  translate_table = dict((ord(char), ' ') for char in string.punctuation)
  newCorpus = []
  print("Preprocessing corpus...")
  for email in corpus:
    email = email.translate(translate_table)
  stop_words = [process_text(w)[0] for w in stopwords.words('english')]
  email = ""
  stemmer = PorterStemmer()
  for email in corpus:
    newEmail = ""
    for word in email.split():
      if re.match(control_characters_regex, word):
        continue
      if re.match(url_regex, word):
        continue
      if re.match(html_tag_regex, word):
        continue
      if emoji.emoji_count(word) == 0:
        if word not in stop_words:
          newEmail += stemmer.stem(word) + " "
      else:
        listOfEmojis = emoji.emoji_list(word)
        for visual in listOfEmojis:
          word = word.replace(visual["emoji"], "")
        newEmail += stemmer.stem(word) + " "
        for visual in listOfEmojis:
          newEmail += emoji.demojize(visual["emoji"]) + " "
    newCorpus.append(newEmail)
  print("Corpus preprocessed, starting classification...")
  return newCorpus



def main():
  filename = input("Enter the name of the corpus file: ")
  with open(filename, "r") as file:
    texto = file.read()
  filename = input("Enter the name of the vocabulary file: ")
  with open(filename, "r") as file:
    vocabulario = file.read()
  vocabulario = vocabulario.split("\n")
  numeroCorreos = len(texto.split("\n"))
  numeroPalabrasVocabulario = int(vocabulario[0].split(" ")[3])
  numeroPalabrasCorpus = 0
  vocabulario = vocabulario[1:]
  palabras = {}
  for i in range(numeroPalabrasVocabulario):
    palabras[vocabulario[i]] = 0
  preprocess = input("Do you want to preprocess the corpus? (y/n): ")
  if preprocess == "y":
    texto = preprocessCorpus(texto)
  else:
    texto = texto.split("\n")
  for i in range(len(texto)):
    for word in texto[i].split():
      if (word == " " or word == ""):
        continue
      numeroPalabrasCorpus += 1
      if word in palabras:
        palabras[word] += 1
      else:
        palabras["<UNK>"] += 1
  # Recorrer el mapa, si hay palabras que aparezcan menos de k veces, sustituirlas por <UNK>
  k = int(input("Enter the minimum number of times a word must appear: "))
  for word in palabras:
    if palabras[word] < k:
      palabras["<UNK>"] += palabras[word]
      palabras[word] = 0
  # Hacer suavizado laplaciano
  for word in palabras:
    palabras[word] += 1
  # Calcular la frecuencia de cada palabra
  frecuencias = {}
  for word in palabras:
    frecuencias[word] = palabras[word] / (numeroPalabrasCorpus + numeroPalabrasVocabulario)
  # Guardar en un archivo
  filename = input("Enter the name of the file to save the model: ")
  with open(filename, "w") as file:
    file.write("Numero de documentos del corpus: " + str(numeroCorreos) + "\n")
    file.write("Numero de palabras del corpus: " + str(numeroPalabrasCorpus) + "\n")
    for word in frecuencias:
      file.write("Palabra: " + word + " Frec: " + str(palabras[word] - 1) + " LogProb: " + str(math.log(frecuencias[word])) + "\n") # Preguntar si la frecuencia es dividir o es el número de veces que aparece
  print("Created " + filename + " file")



if __name__ == "__main__":
  main()