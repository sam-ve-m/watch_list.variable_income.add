fission spec init
fission env create --spec --name wtc-list-add-env --image nexus.sigame.com.br/fission-wacth-list-add:0.2.0-0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-add-fn --env wtc-list-add-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-add-rt --method POST --url /watch_list/variable_income/add --function wtc-list-add-fn
