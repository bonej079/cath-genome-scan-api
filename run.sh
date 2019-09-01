#! /bin/bash

. /home/jbon4/anaconda3/etc/profile.d/conda.sh
conda activate phd37flask

# if permission denied error do
# sudo setcap CAP_NET_BIND_SERVICE=+eip /home/jbon4/anaconda3/envs/phd37flask/bin/python3.7
# sudo setcap CAP_NET_BIND_SERVICE=+eip /home/jbon4/anaconda3/envs/phd37flask/bin/flask
# Reference: https://superuser.com/questions/710253/allow-non-root-process-to-bind-to-port-80-and-443

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
nohup flask run --host=0.0.0.0 --port=8080 &

sleep 5

tail -f ./nohup.out
