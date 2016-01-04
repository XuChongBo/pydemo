@app.route('/image', methods=['GET'])
def show_image():
    from PIL import Image
    s = "/home/xucb/projects/pydemo/my_opencv_demo/demo2.jpg"
    img = Image.open(s)
    string_buf = cStringIO.StringIO()
    img.save(string_buf, format='png')
    string_buf.seek(0)
    return flask.send_file(string_buf, mimetype='image/png')
