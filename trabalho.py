#! /usr/bin/python

from treetagger import TreeTagger
from collections import defaultdict

import csv
import re
import json
import sys
import random
import math

k = 8
saco_de_gato = {}
tt_pt = TreeTagger(language = 'portuguese2')
palavra_morfologia = {}
pattern = re.compile("(^PUNCT.*$|^AUX.*$|^PRON.*$|^DET.*$|^ADP.*$|^SCONJ.*$)")

def sort_second(value):
    return value[1]

# Ler csv
# ID;PERGUNTAS;RESPOSTAS;CLASSES;;
with open(sys.argv[1], 'r', encoding='utf-8', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ';')
    for row in csv_reader:
        pergunta = {}
        pergunta['id'] = row[0].strip()
        pergunta['pergunta'] = row[1].strip()
        pergunta['resposta'] = row[2].strip()
        pergunta['classe'] = row[3].strip()
        saco_de_gato.setdefault(row[3].strip(), []).append(pergunta)

# Divisão do 20/80%
saco_de_gato_teste = {}
saco_de_gato_treino = {}
for classe, perguntas in saco_de_gato.items():
    teste = random.sample(perguntas, k = math.ceil((len(perguntas) * 20) / 100))
    treino = [item for item in perguntas if item not in teste]
    saco_de_gato_teste[classe] = teste
    saco_de_gato_treino[classe] = treino

# Fazer a morfologia no conjunto de teste
for classe, perguntas in saco_de_gato_teste.items():
    for pergunta in perguntas:
        morfologia = tt_pt.tag(pergunta['pergunta'])
        pergunta['morfologia'] = morfologia

# Construir bag of words de cada classe e a global
for classe, perguntas in saco_de_gato_treino.items():
    bag_of_words = defaultdict(int)
    for pergunta in perguntas:
        morfologia = tt_pt.tag(pergunta['pergunta'])
        pergunta['morfologia'] = morfologia
        for palavra in morfologia:
            palavra_morfologia[palavra[2]] = palavra[1]
            bag_of_words[palavra[2]] += 1

    # Limpa a bag of words de cada classe
    bag_of_words_ordenada_e_limpinha = []
    for word, counter in bag_of_words.items():
        if not pattern.match(palavra_morfologia[word]):
            bag_of_words_ordenada_e_limpinha.append((word, counter))
    bag_of_words_ordenada_e_limpinha.sort(key = sort_second, reverse = True)

    saco_de_gato_treino[classe] = {'perguntas': perguntas, 'bag_of_words': bag_of_words_ordenada_e_limpinha}

# Limpa a bag of words global
bag_of_words = defaultdict(int)
for classe, perguntas_bag_of_words in saco_de_gato_treino.items():
    for word, counter in perguntas_bag_of_words['bag_of_words']:
        bag_of_words[word] += counter
bag_of_words = list(bag_of_words.items())
bag_of_words.sort(key = sort_second, reverse = True)

saco_de_gato_treino = {'classes': saco_de_gato_treino, 'bag_of_words': bag_of_words}

# Escreve o arquivo weka de treino
nome = f"treino_K{k:02d}"
with open(f'{nome}.arff', 'w+') as file:
    file.write(f"@relation {nome}\n")

    k_words = [word[0] for word in saco_de_gato_treino['bag_of_words'][:k]]

    for attribute in k_words:
        file.write("@attribute " + attribute + " integer\n")

    file.write("@attribute classe {")
    file.write(','.join(list(saco_de_gato_treino['classes'])))
    file.write("}\n")

    file.write("@data\n")

    for classe, perguntas_bag_of_words in saco_de_gato_treino['classes'].items():
        for pergunta in perguntas_bag_of_words['perguntas']:
            palavras_normalizadas = [i[2] for i in pergunta['morfologia']]
            for attribute in k_words:
                if attribute in palavras_normalizadas:
                    file.write("1, ")
                else:
                    file.write("0, ")
            file.write(classe + "\n")

# Escreve o arquivo weka de teste
nome = f"teste_K{k:02d}"
with open(f'{nome}.arff', 'w+') as file:
    file.write(f"@relation {nome}\n")

    k_words = [word[0] for word in saco_de_gato_treino['bag_of_words'][:k]]

    for attribute in k_words:
        file.write("@attribute " + attribute + " integer\n")

    file.write("@attribute classe {")
    file.write(','.join(list(saco_de_gato_teste)))
    file.write("}\n")

    file.write("@data\n")

    for classe, perguntas in saco_de_gato_teste.items():
        for pergunta in perguntas:
            palavras_normalizadas = [i[2] for i in pergunta['morfologia']]
            for attribute in k_words:
                if attribute in palavras_normalizadas:
                    file.write("1, ")
                else:
                    file.write("0, ")
            file.write(classe + "\n")
