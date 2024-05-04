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
  filename = input("Enter the name of the file from where you want to generate the corpus: ")
  with open(filename, "r") as file:
    texto = file.read()
  #texto = texto.replace("\n", " ")
  texto = texto.lower()
  fields = texto.split("\n")
  header = input("The file has a header? (y,n): ")
  if header == "y":
    fields = fields[3:]
  actualField = 0
  emails = {}
  number = 0
  email = ""
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
    print(emails[key][0].translate(translate_table))
    emails[key][0] = emails[key][0].translate(translate_table)
  stop_words = [process_text(w)[0] for w in stopwords.words('english')]
  email = ""
  stemmer = PorterStemmer()
  for key in emails:
    email = ""
    for word in emails[key][0].split():
      if re.match(control_characters_regex, word):
        continue
      if re.match(url_regex, word):
        continue
      if re.match(html_tag_regex, word):
        continue
      if emoji.emoji_count(word) == 0:
        if word not in stop_words:
          email += stemmer.stem(word) + " "
      else:
        listOfEmojis = emoji.emoji_list(word)
        for visual in listOfEmojis:
          word = word.replace(visual["emoji"], "")
        email += stemmer.stem(word) + " "
        for visual in listOfEmojis:
          email += emoji.demojize(visual["emoji"]) + " "
    emails[key][0] = email
    print("Se procesó el correo " + key + " de " + str(len(emails)) + " correos.")
  filename = input("Enter the name of the file to save the corpus: ")
  with open(filename, "w") as file:
    for key in emails:
      file.write(emails[key][0] + "\n")
  print("Created " + filename + " file")

def process_text(text, stem=True):
  tokens = word_tokenize(text)
  if stem:
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
  return tokens

if __name__ == "__main__":
  main()
