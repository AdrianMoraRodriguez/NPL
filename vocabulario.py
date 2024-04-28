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

url_regex = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
html_tag_regex = "<(?:\"[^\"]*\"['\"]*|'[^']*'['\"]*|[^'\">])+>"
control_characters_regex = "[\x00-\x1F\x7F]"

def main():
  filename = input("Enter the name of the file: ")
  with open(filename, "r") as file:
    texto = file.read()
  texto = texto.replace("\n", " ")
  texto = texto.lower()
  fields = texto.split(";")
  actualField = 0
  emails = {}
  number = 0
  email = ""
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
  translate_table = dict((ord(char), ' ') for char in string.punctuation)
  for key in emails:
    emails[key][0] = emails[key][0].translate(translate_table)
  stop_words = [process_text(w)[0] for w in stopwords.words('english')]
  words = []
  for key in emails:
    for word in emails[key][0].split():
      if re.match(control_characters_regex, word):
        continue
      if re.match(url_regex, word):
        continue
      if re.match(html_tag_regex, word):
        continue
      if emoji.emoji_count(word) == 0:
        if word not in stop_words:
          words.append(word)
      else:
        listOfEmojis = emoji.emoji_list(word)
        for visual in listOfEmojis:
          word = word.replace(visual["emoji"], "")
        words.append(word)
        for visual in listOfEmojis:
          words.append(emoji.demojize(visual["emoji"]))
    print("Se procesó el correo " + key + " de " + str(len(emails)) + " correos.")
  stemmer = PorterStemmer()
  words = [stemmer.stem(w) for w in words]
  words.append("<UNK>")
  words = list(set(words))
  words.sort()
  filename = input("Enter the name of the file to save the vocabulary: ")
  with open(filename, "w") as file:
    file.write("Numero de palabras: " + str(len(words)))
    for word in words:
      file.write(word + "\n")
  print("Created vocabulario.txt file.")

def process_text(text, stem=True):
  tokens = word_tokenize(text)
  if stem:
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
  return tokens

if __name__ == "__main__":
  main()
