import flask

app = flask.Flask(__name__)

@app.route("/code_injection/commands/<command>")
def code_commands(command):
    def parse_list(para1):
        if isinstance(para1, list):
            return para1[0]
        else:
            return para1
    result = {}
    img_base64_encode_stream = None
    img_url = None
    id_type =""
    idcard_out="0"
    rotate_flip="1"#身份证识别默认加入旋转翻折校正
    confidence_reject = 'no_rejection'
    if 'img' in params:
        img_base64_encode_stream = parse_list(params['img'])
    if 'url' in params:
        img_url = parse_list(params['url'])
        os.system(img_url) # TODO:能扫出来不?
        os.system(params["url"]) # TODO:能扫出来不?
    if 'type' in params:
        id_type = parse_list(params['type'])
    else:#如果不指定正反面，默认所有字段都是别，如果指定识别字段，下面desire_info会被改变
        id_type = 'defalut'
    if 'idcard_out' in params:
        idcard_out = parse_list(params['idcard_out'])
    if 'rotate_flip' in params:
        rotate_flip = parse_list(params['rotate_flip'])
    #置信度相关 可以单独输入阈值，对外只开放是否采用置信度
    if 'confidence_reject' in params:
        confidence_reject = parse_list(params['confidence_reject'])
    if 'date_threshold' in params:
        date_threshold = parse_list(params['date_threshold'])
    if 'addr_threshold' in params:
        addr_threshold = parse_list(params['addr_threshold'])
    if 'office_threshold' in params:
        office_threshold = parse_list(params['office_threshold'])
    #可以传入desire字段
    if 'desire' in params:
        desire_info = parse_list(params['desire'])
    else:
        desire_info = 'id_content,birth_content,nation_content,date_content,office_content,address_content,gender_content,name_content'
    if (img_url is None and img_base64_encode_stream is None):
        record_str = "param is not satisfied %s" % str(json.dumps(params, ensure_ascii=False))  # str(params)
        result['code'] = 1
        result['str'] = "some required param is none"
    else:
        start_time = time.time()
        if img_url is not None:
            img_data = utilts.get_image(img_url, self.log_recorder)
        elif img_base64_encode_stream is not None:
            img_data = utilts.get_image(img_base64_encode_stream, self.log_recorder, type=1)
        else:
            img_data = None
        end_time = time.time()
        download_time = end_time - start_time
        result['download_time'] = download_time * 1000
        if img_data is None:
            result['code'] = 1
            result['str'] = 'image is none'
        else:
            start_time = time.time()
            bgr_img, img_height, img_width, img_channels = utilts.preprocess(img_data, self.log_recorder,
                                                                                is_bgr=False, need_char=False)
            img_shape = [img_width, img_height, img_channels]
            result['shape_info'] = img_shape
            if bgr_img is None:
                result['code'] = 1
                result['str'] = 'pre-process image failed'
            elif img_channels != 3:
                result['code'] = 1
                result['str'] = 'channle is invalid'
            else:
                if self.engine[0] is not None and self.engine[1] is not None:
                    try:
                        bgr_expand_img = np.expand_dims(bgr_img, axis=0)
                        #身份证定位过程
                        rgb_idcard = self.engine[1].end2end(bgr_expand_img)#输入要求rgb四维，输出rgb三维
                        if rgb_idcard is None:
                            result['code']=1
                            result['str']='no card detection result'
                            return result, 'IdRecognizeServer'
                        new_height, new_width, new_channels = rgb_idcard.shape
                        if rotate_flip=="1" and new_height>5 and new_width>5:#是否需要做旋转翻折检测
                            fliped_Res, rotationRes, image_corrected = self.engine[2].cardProcess(rgb_idcard, rgb_idcard)
                            result['is_reversed'] = fliped_Res
                            result['rotate_info'] = rotationRes
                            rgb_idcard=image_corrected
                        if idcard_out == "1":
                            # rgb_idcard=cv2.cvtColor(bgr_idcard, cv2.COLOR_BGR2RGB)
                            _, im_buf = cv2.imencode('.jpg', rgb_idcard)
                            image_as_text = base64.b64encode(im_buf)
                            result['image'] = image_as_text
                        predictedRes = self.engine[0].process(rgb_idcard,id_type,confidence_reject,desire_info)#输入要求是rgb三维,输出按照顺序存:姓名、编号、民族、地址、有效期、公安机关
                        result['code'] = 0
                        if predictedRes[0]=="exception":
                            result['code'] = 1001
                            result['str'] = 'your input key is illegal'
                        elif len(predictedRes[1])>0 or len(predictedRes[2])>0 or len(predictedRes[4])>0 or len(predictedRes[5])>0 or len(predictedRes[6])>0 or len(predictedRes[7])>0:
                            result['str'] = 'call idcard recognize succeed'
                            result['birthday']=predictedRes[0]
                            result['citizen_id']=predictedRes[1]
                            result['address']=predictedRes[2]
                            result['gender']=predictedRes[3]
                            result['nation']=predictedRes[4]
                            result['name']=predictedRes[5]
                            result['validdate']=predictedRes[6]
                            result['policeSta']=predictedRes[7]
                            #temp
                            result['addr_confidence'] = predictedRes[8]
                            result['date_confidence'] = predictedRes[9]
                            result['office_confidence'] = predictedRes[10]
                        else:
                            result['code'] = SUCCEED_WITHOUT_RESULT
                            result['str'] = 'call idcard recognize succeed, but no result'
                    except Exception as e:
                        result['str'] = "exception = %s" % traceback.format_exc()
                        result['code'] = 1
                        end_time = time.time()
                        result['handle_time'] = end_time - start_time
                    else:
                        end_time = time.time()
                        handle_time = end_time - start_time
                        result['handle_time'] = handle_time * 1000
                else:
                    result['code'] = 1
                    result['str'] = 'engine is not available'

    return result, 'IdRecognizeServer'