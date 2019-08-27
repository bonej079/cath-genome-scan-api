import io

from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from dotenv import load_dotenv
from Bio import SeqIO
import socket

app = Flask(__name__)
app.debug = True

# Environment
env_path = 'environment.env'
load_dotenv(verbose=True, dotenv_path=env_path)

# API
api = Api(app)
hostname = socket.gethostname()
port = '80'
if hostname in ['uom-1a26']:
    port = '8080'

@app.route('/')
def hello_world():
    return render_template('home.html', hostname=hostname, port=port)

parser = reqparse.RequestParser()
parser.add_argument('command')
parser.add_argument('sequence')


class APIv4_0(Resource):
    def get(self):
        return {'Information': 'The api needs to be called with a PUT and an execute command. Check the help on the homepage.'}

    def put(self):
        args = parser.parse_args()

        command = args['command'].lower()
        if command == 'version':
            return {'version': 'cathv4_0'}
        elif command == 'funfams':
            sequence = args['sequence'].upper()
            if sequence is None:
                return {'error': 'Sequence not provided'}
            else:
                fasta_handle = io.StringIO(sequence)
                for seq_record in SeqIO.parse(fasta_handle, "fasta"):
                    protein_description = seq_record.description
                    searchable_sequence = seq_record.seq

                from classes.funfhmmer import Funfhmmer
                fhmmer = Funfhmmer()
                results = fhmmer.fhmmer_search(protein_description,str(searchable_sequence),[])

                if results is not None or len(results) > 0:
                    return {'funfams': ','.join(results)}
                else:
                    return {'funfams' : None}
        elif command is None:
            return {'error': 'No command was provided.'}
        return {'unknown': 'An unknown error has occurred.'}


api.add_resource(APIv4_0, '/api_4_0/api', endpoint='APIv4_0')

if __name__ == '__main__':
    app.run()
