#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import flask
import utils
import json
from hanzi import Hanzi
from flask import current_app
import redis
import HanziMatcher
import sys

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_pyfile('config.py')
print app.config
app.redis = redis.StrictRedis(host=app.config['REDIS_HOST'],port=app.config['REDIS_PORT'], db=0)

#print app.hanzi_list
#app.config['LABELED_DATASET_PATH'] = LABELED_DATASET_PATH

 #=  set(map(lambda x:x.decode('utf-8'), os.listdir(app.config['LABELED_DATASET_PATH']) ))
#app.hanzi_list = utils.read_handwriting(os.path.join("./","handwriting.txt"))

#if not app.debug:
#app.debug = True
import logging
from logging import FileHandler


file_handler = FileHandler(app.config['LOG_FILE_PATH'],encoding='utf-8')
#file_handler.setLevel(logging.ERROR)
#file_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.DEBUG)   #INFO
# create formatter{'format': }
formatter = logging.Formatter('%(asctime)s %(process)d %(filename)s %(lineno)d %(funcName)s %(levelname)s %(message)s')
# add formatter to ch
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)


# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(stdout_handler)

# def trace_log(logger=app.logger, lvl=logging.DEBUG):
#     def wrapper(func):
#         def wrappered_func(*args, **kwargs):
#             func_name = getattr(func, '__name__')
#             logger.log(lvl, '[{func_name}] enter'.format(func_name=func_name))
#             res = func(*args, **kwargs)
#             logger.log(lvl, '[{func_name}] exit'.format(func_name=func_name))
#             return res
#         return wrappered_func
#     return wrapper

#@trace_log()
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def check_valid_strokes(strokes):
    ret = "ok"
    if len(strokes) < 1:
        ret = "at least has one stroke."
    for stroke in strokes:
        if len(stroke) < 2:
            ret = "some stroke has less than two points."
        for i, point in enumerate(stroke):
            if len(point)!=2:
                ret = "some stroke point does not has tow component."
            app.logger.debug(point)
            if i>0 and stroke[i-1]==point:
                ret = "continuous same point in a stroke."
    app.logger.debug("return:"+ret)
    return ret

@app.route('/stroke_images', methods=['GET', 'POST'])
def stroke_images():
    if request.method == 'POST':
        print "======================================="
        app.logger.debug(dir(request.form))
        #print request.form['tag'].encode('utf-8')
        app.logger.debug(request.form.keys())
        tag =  request.form['tag']
        imei =  request.form['imei']
        strokes = request.form['strokes']
        strokes = json.loads(strokes)
        width = int(request.form['width'])
        height = int(request.form['height'])
        app.logger.debug(type(tag))
        app.logger.debug(tag)
        app.logger.debug("%s %s %s %s %s" % (strokes, "num of strokes:", len(strokes), width, height) )
        # check width, height valid.
        if width != height:
            return "image must be square", 500
        if width < app.config['IMAGE_WIDTH']:
            return "the size of image is too small", 500

        # check strokes valid
        msg = check_valid_strokes(strokes)
        if msg!="ok":
            return msg, 500
        # save png
        png_file = request.files['file']
        if png_file and allowed_file(png_file.filename):
            filename = secure_filename(png_file.filename)
            savedir = os.path.join(app.config['LABELED_DATASET_PATH'],tag)
            utils.mkdir(savedir)
            
            png_filepath = os.path.join(savedir, filename)
            png_file.save(png_filepath)

            # append filename  to desc.txt
            assert(app.redis.rpush(tag.encode("utf-8")+"_pathlist", png_filepath))

            # with open(os.path.join(savedir, "desc.txt"), "a") as myfile:
            #     myfile.write(png_filepath.encode('utf-8')+os.linesep)
            #     t = current_app.filename_dict.setdefault(savedir, [])
            #     t.append(png_filepath)
            #return redirect(url_for('uploaded_file',tag=tag, filename=filename))

            svg_filepath = png_filepath[:-3]+"svg"
            # with open(svg_filepath, "w") as svg_file:
            #     svg_file.write(svg.to_xml())
            # convert the points
            ch = Hanzi(tag, strokes,width,height)
            ch.save(svg_filepath)

            # append filename  to desc.txt
            #assert(app.redis.rpush(tag.encode("utf-8")+"_pathlist", svg_filepath)) 
            # with open(os.path.join(savedir, "desc.txt"), "a") as myfile:
            #     myfile.write(svg_filepath.encode('utf-8')+os.linesep)
            #     t = current_app.filename_dict.setdefault(savedir, [])
            #     t.append(svg_filepath)
            assert(app.redis.incr(tag.encode('utf-8')+"_count"))
            assert(app.redis.incr(imei.encode('utf-8')+"_count"))
            assert(app.redis.incr("total_count"))
            return "ok"
        else:
            return "png filename error.", 500
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/stroke_images" method=post enctype=multipart/form-data>
    tag:<input type="text" name="tag" placeholder="学">
    </br>
    file:<input type=file name="file">
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<tag>/<filename>')
def uploaded_file(tag,filename):
    return flask.send_from_directory(os.path.join(app.config['LABELED_DATASET_PATH'],tag),filename)


@app.route('/stroke_sequences', methods=["GET","PUT", "POST"])
def stroke_sequences():
    if request.method == 'GET':
        return 'require post josn:  {"tag":"test","strokes":[[(1,2),[2,3],[4,2] ],[]], "width":333,"height":666}'
    else:    
        d = request.get_json(force=True)
        #return flask.jsonify(d)
        return "ok"

@app.route('/')
def home():
    url_list = []
    hanzi_list = [ch.decode('utf-8') for ch in app.redis.lrange("hanzi_list", 0, -1)]
    total_count = app.redis.get("total_count")
    for idx,tag in enumerate(hanzi_list):
        tag_count = app.redis.get(tag.encode('utf-8')+"_count")
        if tag_count is None:
            tag_count = 0
        url = url_for('browse',tag=tag,page_id=1,page_size=2)
        url_list.append((idx+1,tag,tag_count,url))
    #lines = os.listdir("/home/xucb/projects/test_platform/")
    #print current_app.name
    app.logger.info('access home page')

    #print current_app.hanzi_list, 
    print "total category:",len(hanzi_list)
    return flask.render_template('home.html', url_list=url_list, total_count=total_count)



@app.route('/delete_image/<tag>/<filename>', methods=["GET", "POST"])
def delete_image(tag,filename):
    #print tag, type(tag)
    #print request.form['tag'].encode('utf-8')
    app.logger.debug("request.referrer: %s" % request.referrer)
    #app.logger.debug(request.form.keys())
    filename = secure_filename(filename)[:-3]
    savedir = os.path.join(app.config['LABELED_DATASET_PATH'],tag)
    png_filepath = os.path.join(savedir, filename)+"png"
    svg_filepath = os.path.join(savedir, filename)+"svg"
    app.logger.debug(png_filepath)
    assert(app.redis.lrem(tag.encode("utf-8")+"_pathlist",0, png_filepath))
    assert(app.redis.decr(tag.encode('utf-8')+"_count")>=0)
    assert(app.redis.decr("total_count")>=0)
    os.remove(png_filepath)
    os.remove(svg_filepath)
    #return redirect("##")
    return redirect(request.referrer)
    #return "^_^"
    # filepath = os.path.join(app.config['LABELED_DATASET_PATH'],tag,filename)
    # print filepath,type(filepath)
    # hanzi = Hanzi.parse_from_file(filepath.encode("utf-8"))
    # if HanziMatcher.check_the_tag(hanzi):
    #     return "yes"
    # else:
    #     return "no"

@app.route('/identify', methods=['POST'])
def identify():
    print dir(request.form)
    #print request.form['tag'].encode('utf-8')
    app.logger.info(request.form.keys())
    tag =  request.form['tag']
    imei =  request.form['imei']
    strokes = request.form['strokes']
    strokes = json.loads(strokes)
    width = int(request.form['width'])
    height = int(request.form['height'])
    #print type(tag)
    app.logger.info(tag)
    #print 
    app.logger.info("%s %s %s %s %s " % (strokes, "num of strokes:", len(strokes), width, height))
    # check valid
    if len(strokes) <= 0 or len(strokes[0])<=0 or len(strokes[0][0])<=0:
        return "num of strokes must be positive", 500
    if width != height:
        return "image must be square", 500
    if width < app.config['IMAGE_WIDTH']:
        return "the size of image is too small", 500

    png_file = request.files['file']
    if png_file and allowed_file(png_file.filename):
        filename = secure_filename(png_file.filename)
        savedir = os.path.join(app.config['UNLABELED_DATASET_PATH'],tag)
        utils.mkdir(savedir)
        png_filepath = os.path.join(savedir, filename)
        # save png
        png_file.save(png_filepath)
        svg_filepath = png_filepath[:-3]+"svg"
        hanzi = Hanzi(tag, strokes,width,height)
        # save svg
        hanzi.save(svg_filepath)
        # do match
        isOK, score = HanziMatcher.check_the_tag(hanzi)
        return flask.jsonify({"result": 1 if isOK else 0})
        #return "%s %s" % ("对" if isOK else "错", score)
    else:
        return "png filename error.", 500

@app.route('/get_count', methods=['GET', 'POST'])
def get_count():
    if request.method == 'POST':
        print dir(request.form)
        #print request.form['tag'].encode('utf-8')
    tag = request.form['tag']
    imei =  request.form['imei']
    tag_count = app.redis.get(tag.encode('utf-8')+"_count")
    if tag_count is None:
        tag_count = 0
    imei_count = app.redis.get(imei.encode('utf-8')+"_count")
    if imei_count is None:
        imei_count = 0
    total_count = app.redis.get("total_count")
    return flask.jsonify({"total_count":total_count,"tag_count":tag_count, "imei_count":imei_count})


@app.route('/browse/<tag>/<page_id>/<page_size>')
def browse(tag,page_id,page_size):
    #app.logger.debug(dir(request))
    app.logger.debug(request.url)
    app.logger.debug(request.full_path)
    page_id = int(page_id)
    page_size = int(page_size)
    assert(page_id>0 and page_size>0)
    url_list = []
    tag_basedir = os.path.join(app.config['LABELED_DATASET_PATH'],tag)
    next_page_url = url_for('browse',tag=tag,page_id=page_id+1,page_size=page_size)

    # lines = current_app.filename_dict.get(tag_basedir)
    # if not lines:
    #     lines = utils.category_desc(tag_basedir)
    #     current_app.filename_dict[tag_basedir] = lines
    lines = app.redis.lrange(tag.encode("utf-8")+"_pathlist", 0, -1)
    print "in browse total", len(lines)
    lines = lines[(page_id-1)*page_size:page_id*page_size]
    print lines
    for line in lines:
        png_filepath = os.path.basename(line.strip())
        svg_filepath = png_filepath[:-3]+"svg"
        url_list.append( (png_filepath,url_for('uploaded_file',tag=tag, filename=png_filepath),url_for("delete_image",tag=tag,filename=png_filepath)) )
        url_list.append( (svg_filepath,url_for('uploaded_file',tag=tag, filename=svg_filepath),url_for("delete_image",tag=tag,filename=svg_filepath)) )
    return flask.render_template('images.html',url_list=url_list,next_page_url=next_page_url, page_url=request.full_path)

if __name__ == '__main__':
    #app.run(host='192.168.100.22',port=7000)
    app.run(host='0.0.0.0',port=80,debug=True)
    #app.run(host='192.168.100.22',port=7001,debug=True)

