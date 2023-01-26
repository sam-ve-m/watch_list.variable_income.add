fission spec init
fission env create --spec --name wtc-list-var-add-env --image nexus.sigame.com.br/fission-wacth-list-variable-income-add:0.2.0-0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name wtc-list-var-add-fn --env wtc-list-var-add-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name wtc-list-var-add-rt --method POST --url /watch_list/variable_income/add --function wtc-list-var-add-fn
