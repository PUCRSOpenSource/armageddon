#! /usr/bin/bash

sed -i \
    -e 's/random forest/floresta aleatória/gI' \
    -e 's/decision tree/árvore de decisão/gI' \
    -e 's/emprestimos/empréstimos/gI' \
    -e 's/varios/vários/gI' \
    -e 's/aplicacao/aplicação/gI' \
    -e 's/calculos/cálculos/gI' \
    -e 's/maioritária/majoritária/gI' \
    $1
