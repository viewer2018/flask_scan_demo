from lxml import etree
from io import StringIO
from flask import Flask, request

app = Flask(__name__)


# xslt
@app.route("/xslt")
def bad():
    xsltQuery = request.args.get('xml', '')
    xslt_root = etree.XML(xsltQuery)
    f = StringIO('<foo><bar></bar></foo>')
    tree = etree.parse(f)
    result_tree = tree.xslt(xslt_root)  # Not OK

# xpathBad
from io import StringIO
from lxml import etree
@app.route("/xpathBad")
def xpathBad(request):
    value = request.GET['xpath']
    f = StringIO('<foo><bar></bar></foo>')
    tree = etree.parse(f)
    r = tree.xpath("/tag[@id='%s']" % value)

# xpathGood
def xpathGood(request):
    value = request.GET['xpath']
    f = StringIO('<foo><bar></bar></foo>')
    tree = etree.parse(f)
    r = tree.xpath("/tag[@id=$tagid]", tagid=value)

app.run(debug=True)