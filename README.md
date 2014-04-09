Spinne
======
Spinne is a python 3.x micro web framework. This web framework was built only by python standard libraries and doesn't require the installation of any other library.
Installation
======
You can download the project directly from this repository.
Usage
======
Spinne is easy to use.
You first create a folder where you're going to store your web app files.

    app.py
    /files
        index.html
        template.stmp
        send.stmp
        /st
            image.png
            video.mp4

`app.py` should include the main code of the website:

    from Spinne import *
    root = './files'
    index = 'index.html'
    POST = ['send.stmp']

The code is simple, you first import the Spinne module, then you store the root of your web app in the variable `root`, the index of your web app (which will show when you visit host:port/) in `index` and the files where the method is post in `POST`.

`index.html` has been set to the index of your website in `app.py`.
