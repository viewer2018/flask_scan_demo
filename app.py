import flask
import subprocess

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

def __random_name(size=6):
    '''
    Generates a random cloud instance name
    '''
    return 'CLOUD-TEST-' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(size)
    )
def setup(app):
    def add_documenter(app, env, docnames):
        app.add_autodocumenter(SaltFunctionDocumenter)
        
app.run(debug=True)