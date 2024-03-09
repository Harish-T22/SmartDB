import subprocess
from flask import Flask, render_template, request
import openai


app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'


# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": message}
    ]
    )
    if completion.choices[0].message!=None:
        return completion.choices[0].message

    else :
        return 'Failed to Generate response!'
    

# @app.route("/querymode")
# def query_mode():
#     return render_template("query_mode.html")

@app.route('/runexe')
def wakeup():
    subprocess.Popen('start cmd /k C:\\Users\\HARISH\\Desktop\\Chatbot\\dbproject\\dbproject.exe',shell=True)
    # subprocess.call('C:\\Users\\HARISH\\Desktop\\Chatbot\\dbproject\\dbproject.exe')
    return render_template("query_mode.html")


# def run_exe():
#     subprocess.call('C:\\Users\\HARISH\\Desktop\\Chatbot\\dbproject\\dbproject.exe')
#     return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)




