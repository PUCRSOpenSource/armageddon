from treetagger import TreeTagger
from pprint import pprint
from collections import defaultdict

import csv
import re
import json

saco_de_gato = {}
tt_pt = TreeTagger(language = 'portuguese2')

def sort_second(value):
    return value[1]

# ID;PERGUNTAS;RESPOSTAS;CLASSES;;
with open('parcial.csv', 'r', encoding='utf-8', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ';')
    for row in csv_reader:
        pergunta = {}
        pergunta['id'] = row[0]
        pergunta['pergunta'] = row[1]
        pergunta['resposta'] = row[2]
        pergunta['classe'] = row[3]
        saco_de_gato.setdefault(row[3], []).append(pergunta)

for classe, perguntas in saco_de_gato.items():
    bag_of_words = defaultdict(int)
    palavra_morfologia = {}
    for pergunta in perguntas:
        morfologia = tt_pt.tag(pergunta['pergunta'])
        pergunta['morfologia'] = morfologia
        for palavra in morfologia:
            palavra_morfologia[palavra[2]] = palavra[1]
            bag_of_words[palavra[2]] += 1

    bag_of_words_ordenada_e_limpinha = []
    pattern = re.compile("(^PUNCT.*$|^AUX.*$|^PRON.*$|^DET.*$)")

    for word, counter in bag_of_words.items():
        if not pattern.match(palavra_morfologia[word]):
            bag_of_words_ordenada_e_limpinha.append((word, counter))
    bag_of_words_ordenada_e_limpinha.sort(key = sort_second, reverse = True)

    saco_de_gato[classe] = {'perguntas': perguntas, 'bag_of_words': bag_of_words_ordenada_e_limpinha}

print(json.dumps(saco_de_gato, indent = 4, ensure_ascii = False))

