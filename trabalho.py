from treetagger import TreeTagger
from pprint import pprint

import csv
import json

saco_de_gato = {}
tt_pt = TreeTagger(language = 'portuguese2')

# ID;PERGUNTAS;RESPOSTAS;CLASSES;;
with open('parcial.csv', 'r', encoding='utf-8', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ';')
    line_count = 0
    for row in csv_reader:
        pergunta = {}
        pergunta['id'] = row[0]
        pergunta['pergunta'] = row[1]
        pergunta['resposta'] = row[2]
        pergunta['classe'] = row[3]
        saco_de_gato.setdefault(row[3], []).append(pergunta)
        line_count += 1
    print(f'Processed {line_count} lines.')

for classe, perguntas in saco_de_gato.items():
    for pergunta in perguntas:
        pergunta['morfologia'] = tt_pt.tag(pergunta['pergunta'])

print(json.dumps(saco_de_gato, indent = 4, ensure_ascii = False))

