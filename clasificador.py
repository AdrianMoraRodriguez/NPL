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
  phishingFilename = input("Enter the model of lenguage of the phishing emails: ")
  with open(phishingFilename, "r") as file:
    phishing = file.read()
  phishing = phishing.split("\n")
  firstLine = phishing[0]
  phishing = phishing[2:]
  numOfPhishingEmails = int(firstLine.split(":")[1]);
  safeFilename = input("Enter the model of lenguage of the safe emails: ")
  with open(safeFilename, "r") as file:
    safe = file.read()
  safe = safe.split("\n")
  firstLine = safe[0]
  safe = safe[2:]
  numOfSafeEmails = int(firstLine.split(":")[1]);
  probPhishing = numOfPhishingEmails / (numOfPhishingEmails + numOfSafeEmails)
  probSafe = numOfSafeEmails / (numOfPhishingEmails + numOfSafeEmails)
  wordProbPhishing = {}
  wordProbSafe = {}
  for line in phishing:
    if line == "":
      continue
    line = line.split(":")
    word = line[1].split(" ")[1]
    prob = float(line[-1])
    wordProbPhishing[word] = prob
  for line in safe:
    if line == "":
      continue
    line = line.split(":")
    word = line[1].split(" ")[1]
    prob = float(line[-1])
    wordProbSafe[word] = prob
  corpus = input("Enter the corpus to classify: ")
  with open(corpus, "r") as file:
    corpus = file.read()
  corpus = preprocessCorpus(corpus)
  print("Number of emails to classify: " + str(len(corpus)))
  classificationOfEmails = []
  contador = 1
  for email in corpus:
    originalEmail = email
    email = email.split(" ")
    probEmailPhishing = 0
    probEmailSafe = 0
    for word in email:
      if word in wordProbPhishing:
        probEmailPhishing += wordProbPhishing[word]
      else:
        probEmailPhishing += wordProbPhishing["<UNK>"]
      if word in wordProbSafe:
        probEmailSafe += wordProbSafe[word]
      else:
        probEmailSafe += wordProbSafe["<UNK>"]
    probEmailPhishing += probPhishing
    probEmailSafe += probSafe
    classificationOfEmails.append([originalEmail[:10], probEmailSafe, probEmailPhishing])
    if contador % 100 == 0:
      print("Email " + str(contador) + " of "+ str(len(corpus)) + " classified")
    contador += 1
  nameOfOutput = input("Enter the name of the output file: ")
  emailsP = 0
  emailsS = 0
  with open(nameOfOutput, "w") as file:
    for email in classificationOfEmails:
      file.write(email[0] + "," + str(round(email[1], 2)) + "," + str(round(email[2], 2)))
      if email[1] > email[2]:
        file.write(",S")
        emailsS += 1
      else:
        file.write(",P")
        emailsP += 1
      file.write("\n")
  print("The classification of the emails is in the file " + nameOfOutput)
  with open("resumen_" + nameOfOutput, "w") as file:
    for email in classificationOfEmails:
      if email[1] > email[2]:
        file.write("S\n")
      else:
        file.write("P\n")
  print("Number of emails classified as phishing: " + str(emailsP))
  print("Number of emails classified as safe: " + str(emailsS))
    
  

if __name__ == "__main__":
  main()