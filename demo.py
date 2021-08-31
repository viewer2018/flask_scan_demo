from flask import Flask, request
import os
app = Flask(__name__)
import utilts
import requests

# xsltQuery = request.args.get('xml', '')
@app.route("/code_injection/commands/<command>")
def code_commands(command):
    import commands
    try:
        result_success = commands.getstatusoutput(command)
        result_success = commands.getoutput(command)
        # command = 'bash -c "whoami" > /Users/hwf/Desktop/aaa'
        result=map(__import__('os').system,[command])
        import os
        # command = 'bash -c "whoami" > /Users/hwf/Desktop/aaa'
        result=map(os.system,[command])
    except subprocess.CalledProcessError as e:
        return "An error occurred while trying to fetch task status updates."

    return 'result is %s' % (result_success)

@app.route("/code_injection/commands1")
def code_commands(command):
    url = request.args.getlist("url")
    def parse_list(para1):
        if isinstance(para1, list):
            return para1[0]
        else:
            return para1
    img_url = parse_list(url)
    os.system(img_url) # TODO:能扫出来不?y
    os.system(url) # TODO:能扫出来不?y
    get_os_system(url)# TODO:能扫出来不? y
    utilts.get_os_system(url)# TODO:能扫出来不?
    if img_url is not None:
        img_data = utilts.get_image(img_url)
        res = requests.get(url=img_url, timeout=5)

def get_os_system(param, logger=None, type=0):
    """
    获取图像原始数据
    :param param: 图像的url 或者 base64 码流
    :param type: type=0, param 作为 图像的url, type=1, param 作为 base64 码流
    :return:
    """
    try:
        if 0 == type:
            return os.system(param, logger)
        elif 1 == type:
            return base64.b64decode(param)
        else:
            return None
    except Exception as e:
        if logger:
            logger.info("except occur in get_image: %s" % (traceback.format_exc()))
        else:
            print("except occur in get_image: %s" % (traceback.format_exc()))
        return None