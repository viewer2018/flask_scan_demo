import flask
import subprocess
import commands

app = flask.Flask(__name__)

@app.route('/')
def index():
    return subprocess.check_output(flask.request.args.get('c', 'ls'))

@app.route("/code_injection/exec/<command>")
def code_execution(command):
    try:
        result_success = subprocess.check_output(
            [command], shell=True)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to fetch task status updates."

    return 'result is %s' % (result_success)

@app.route("/code_injection/commands/<command>")
def code_commands(command):
    try:
        result_success = commands.getstatusoutput(command)
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to fetch task status updates."

    return 'result is %s' % (result_success)
        
app.run(debug=True)