from flask import Flask, request
from flask_api import status
import requests

import socket

import dns.resolver as dns

app = Flask(__name__)
#http://127.0.0.1:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&as_ip=1&as_port=1&number=10

@app.route('/')
def hello_world():
    return 'Hello, this is user server!'

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    args = request.args
    try:
        hostname = args.get("hostname")
        fs_port = int(args.get("fs_port"))
        number = args.get("number")
        as_ip = args.get("as_ip")
        as_port = int(args.get("as_port"))
        assert hostname!=None
        assert fs_port!=None
        assert number!=None
        assert as_ip!=None
        assert as_port!=None
    except:
        return "Parameters are missing", status.HTTP_400_BAD_REQUEST

    fib = requests.get("http://{}:{}/fibonacci?number={}".format("0.0.0.0", fs_port, number)).content.decode() #update hostname ip
    return str(fib)


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
