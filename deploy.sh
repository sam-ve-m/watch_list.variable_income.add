#!/bin/bash
fission spec init
fission env create --spec --name wathc-list-save-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/python-builder-3.8:0.0.2
fission fn create --spec --name wathc-list-save-fn --env wathc-list-save-env --src "./func/*" --entrypoint main.save_symbols  --rpp 100000
fission route create --spec --method POST --url /wathc_list/add --function wathc-list-save-fn
