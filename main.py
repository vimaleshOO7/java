# It is a flask application for DC2
from flask import Flask, request, render_template, jsonify
import requests
import re
import time
import datetime
import usecase.dctwousecaseone
import subprocess

app = Flask(__name__)

uploaded_file_path = ""


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == 'GET':
        return render_template('index1.html')
    elif request.method == 'POST':
        request_data = request.data.decode("UTF-8")

        # ========== file upload ==========
        #if "github.com" in request_data:
        #    time.sleep(60)
        #    return jsonify(output="Repo is cloned into path usecase/sampleJavaCode. Converted python code is placed in path "
        #                          "/usecase/convertedCode.")
        if "test script for java" in request_data:
            usecase.dctwousecaseone.generate_test_script_for_java()
            return jsonify(output="Test script for java is created in path usecase/sampleJavaCode/test.")
        if "test script for python" in request_data:
            usecase.dctwousecaseone.generate_test_script_for_python()
            return jsonify(output="Test script for python is created in path usecase/convertedCode/test.")
        if "migrate" in request_data:
            time.sleep(60)
            return jsonify(output="Code migrated successfully into git repo https://github.com/adbahsijit/convertedCode.git")
        if 'file' in request.files.keys():
            print('chat(): received a file')
            uploadedFile = request.files['file']
            print('chat(): uploaded file name is ' + uploadedFile.filename)
            uploadedFile.save("storage/" + uploadedFile.filename)
            print('chat(): ' + uploadedFile.filename + ' is saved successfully.')
            global uploaded_file_path
            uploaded_file_path = 'storage/' + uploadedFile.filename
            return jsonify(output='File ' + uploadedFile.filename + ' uploaded successfully.')
        if 'Analyze' in request_data:
            content_of_uploaded_file = open(uploaded_file_path).read()
            print('chat(): content of the file ' + content_of_uploaded_file)
            chat_response = usecase.dctwousecaseone.help_me_to('Analyse the following content ' + content_of_uploaded_file)
            print('chat(): response from DigiCon is ' + chat_response)
            return jsonify(output=chat_response)
        else:
            # if isFileUploaded and re.search(".*analyze|.*Analyze.*file.*",request_data):
            #    with open("storage/input.txt", 'r') as file:
            #        filecontent = file.read()
            #    ollama_data = {"prompt": "Analyze " + filecontent, "model": "llama3"}
            # ========== Call Ollama with the requested data ==========
            ollama_url = 'http://localhost:11434/api/generate'
            ollama_data = {"prompt": request_data, "model": "llama3"}
            session = requests.Session()
            session.headers.update({'Content-Type': 'application/json'})
            response = session.post(ollama_url, json=ollama_data)
            raw_content_of_response = response.content.decode("UTF-8")
            consolidated_array_of_words_from_chunked_response = re.findall("\"response\":\"\",|\"response\":\"(.+)\",",
                                                                     raw_content_of_response)
            consolidated_response = "".join(consolidated_array_of_words_from_chunked_response)
            # resp = consolidated_response.replace("\\\"", "").replace("  ", " ").replace(" .", ".")
            resp = consolidated_response
            resp = resp.replace(r'\n', '\n')
            open("output/" + str(round(datetime.datetime.now().timestamp()*1000)) + ".md", 'w').write("REQUEST: " + request_data + ";\n\nRESPONSE: " + resp)
            return jsonify(output=resp)
    else:
        return "<p>Method not allowed.</p>"


if __name__ == "__main__":
    app.run(port=8080)
    #usecase.dctwousecaseone.clone_repository()
    #usecase.dctwousecaseone.convert_code()
    #usecase.dctwousecaseone.generate_test_script_for_java()
    print('done')


