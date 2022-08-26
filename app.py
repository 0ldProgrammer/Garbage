#coding:utf-8

import flask
import sys
import os
import re

app = flask.Flask(__name__, template_folder='templates', static_folder='static')

def get_last_number_of_messages():
    """
        :Definition: Retrieve the last file value in the folder and increment value.
        :Function: __get_last_nulber_messages()__
    """
    current_directory_flask_list = []

    for last_message_in_the_directory in os.listdir('/home/gwenael/wsgi_server/messages'):
        last_message = re.findall('([0-9]{0,}\_message\.txt)', last_message_in_the_directory)
        for j in last_message:
            current_directory_flask_list.append(j)

    recover_last_message = int(current_directory_flask_list[0].split("_")[0]) + 1
    return str(recover_last_message) + "_message.txt"

@app.route('/contact_api_json', methods=["GET", "POST"])
def contact_api_json():
    """
        :Definition: You can send confidential data our server, we will look lato, it all.
        :Function: __contact_api_json()__
    """
    if(flask.request.method == "POST"):
        flask_request_json = flask.request.json
        for item_pull_request in flask_request_json.items():
            if('lastname' and 'firstname' and 'message' in item_pull_request):

                try:
                    flask_request_json['message'] = eval(flask_request_json['message'])

                except NameError as exception_error_flask_request:
                    flask_request_json['message'] = flask_request_json['message']

                except SyntaxError as exception_error_flask_request:
                    flask_request_json['message'] = flask_request_json['message']

                with open('/home/gwenael/wsgi_server/messages/' + get_last_number_of_messages(), "w") as write_new_file:
                    write_new_file.write("\nLastname: %s\nFirstname: %s\nMessage: %s\n\n" %(flask_request_json['lastname'], flask_request_json['firstname'], flask_request_json['message']))

                return flask.jsonify(flask_request_json)

    return flask.jsonify({
        "_api_version": "1.0.0.0",
        "Information": {
            "success": "0",
            "message": "Arguments missing"
        }
    })

@app.route('/', methods=["GET"])
def index_page():
    return flask.render_template('index.html')

@app.route('/contact', methods=["GET"])
def contact_page():
    return flask.render_template('contact.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
