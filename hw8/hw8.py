'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 5
'''

'''
In some functions below, the keyword "pass" is used to
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

import os
import flask
from flask import Flask, flash, request, redirect, url_for, send_file, render_template
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'    # this is where we will save uploaded files
app.secret_key = 'ax9o4klasi-0oakdn'        # random secret key (needed for flashing)
WIDTH = 1000
cache = (0, 0)


'''Note: it is typically *not* a good idea to keep a global variable like cache to handle
the state of your website. That will most certainly break if you will receive concurrent
requests. However, since we do not expect to handle concurrent requests in this assignment,
it will do just fine'''


def allowed_file(filename):
    '''
    Check whether the extension is a valid image extension
    args:
        filename: a single string with the name of the file
    ret:
        valid: True if the extension is valid, False otherwise
    '''
    if not isinstance(filename, str) or not filename:
        return False

    filename = filename.lower()
    ext_1 = filename[-4:]
    ext_2 = filename[-5:]

    return ext_1 == '.png' or ext_1 == '.jpg' or ext_2 == '.jpeg'


def append_to_collage(filename):
    '''
    Appends the image in filename to the collage. Assume
    the current collage is stored in the static directory
    and the filename corresponds to a valid image file in
    app.config['UPLOAD_FOLDER'].
    args:
        filename: the image filename (without the path)
    ret: None
    Outcome: the new image is appended to the collage and
    the collage is saved back to the static directory.
    Hint 1: Use os.path.join to concatenate directory and
    filenames into a valid path for any OS
    Hint 2: Use the cache variable to figure out the
    current position in the collage.
    Hint 3: Pillow does not automatically increase the size
    of images you paste together. You will have to do this
    manually (e.g., by creating a new, larger image)
    '''
    if not allowed_file(filename):
        return

    im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)).resize((100, 100))

    collage = None
    global cache
    try:
        collage = Image.open(os.path.join('static', 'collage.png'))
    except FileNotFoundError:
        collage = Image.new('RGB', (WIDTH, 100))
        cache = (0, 0)

    cachelist = list(cache)

    if cache[0] == WIDTH:
        cachelist[0] = 0
        cachelist[1] = cache[1] + 100
        temp = collage
        collage = Image.new('RGB', (WIDTH, cachelist[1]+100))
        collage.paste(temp, (0, 0))
        cache = tuple(cachelist)

    collage.paste(im, tuple(cachelist))

    cachelist[0] = cachelist[0] + 100

    cache = tuple(cachelist)

    collage.save(os.path.join('static', 'collage.png'))


@app.route('/')
def home():
    '''
    Redirect the user from the root URL to the /uploads URL
    args: None
    ret:
        The required return by Flask so the user is
        redirected to the /uploads URL
    '''
    return flask.redirect('uploads')


@app.route('/uploads', methods=['GET', 'POST'])
def handle_uploads():
    '''
    Handle GET and POST requests for the /uploads URL.
    GET requests should display the upload_template
    provided to you. POST requests should check the
    validity of the request (this has been filled in
    for you) and save the file to the app.config['UPLOAD_FOLDER']
    directory. If the file is correctly uploaded,
    the collage should be updated and the user should
    be re-directed to the /collage URL.
    args: None
    ret:
        The required return by Flask so the user is
    Note: use secure_filename() to ensure the
    filename to save is safe.
    Hint: You can initialize the relevant cached variables
    here (e.g., if key not in cache...)
    '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')     # a better template
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not (file and allowed_file(file.filename)):
            flash('Invalid file type')
            return redirect(request.url)

        # actually perform POST request:
        # check validity of input                       (X)
        # save new image to app.config['UPLOAD_FOLDER'] (X)
        # call append_to_collage()                      (X)
        # redirect to collage                           (X)
        
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))
        append_to_collage(f.filename)
        return redirect('/collage')
    else:
        # GET html page
        return render_template(secure_filename('uploads.html'))


@app.route('/collage')
def collage():
    '''
    Handle GET requests for the /collage URL.
    args: None
    ret:
        The required return by Flask to display the collage
    Hint: You can use send_file() and specify the mimetype
    as the required image type so your browser displays the
    updated collage
    '''
    return app.send_static_file('collage.png')
