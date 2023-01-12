from flask import Flask, jsonify, request
import ssl
import json
app = Flask(__name__)

@app.route("/", methods=["POST"])
def imprimir():
    response = {"status": 200}
    return jsonify(response)


@app.route("/pix", methods=["POST"])
def imprimirPix():
    imprime = print(request.json)
    data = request.json
    with open('data.txt', 'a') as outfile:
        outfile.write("\n")
        json.dump(data, outfile)
    return jsonify(imprime)

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('apiPIX/chain-pix-prod.crt')
    context.load_cert_chain(
        'caminho-certificados/server_ssl.crt.pem',
        'caminho-certificados/server_ssl.key.pem')
    app.run(ssl_context=context, host='0.0.0.0')
