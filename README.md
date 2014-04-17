Spinne
======
Spinne is a python 3.x micro web framework. This web framework was built only by python standard libraries and doesn't require the installation of any other library.
Installation
======
You can download the project directly from this repository then put the file in C:/PythonXX/Lib/site-packages where XX is your python version.
Basic Usage
======
Spinne is easy to use.
You first create a folder where you're going to store your web app files.

    app.py
    /files
        home.html
        send.stmp
        /st
            image.png
            video.mp4

`app.py` should include the main code of the website, the following example will be using mako template enginge, downloaded from [this link][1].


  [1]: https://pypi.python.org/pypi/Mako/?:

    import Spinne
    from mako.template import Template
    Spinne.root = './files'
    Spinne.home = 'home.html'
    Spinne.POST = ['/send.stmp']
    def temp(tmp):
        return Template(tmp).render()
    Spinne.template = temp
    s = Spinne.Server('localhost', 8888)
    s.run()

**Note**: Don't use `from Spinne import *`.<br>
The code is simple, you first import the Spinne module and mako template engine, then you store the root of your web app in the variable `root`, the home page of your website (which will show when you visit host:port/) in `home` and the files where the method is post in `POST`, then you define a function with any name you want while making one argument `tmp` which will be used by Spinne and put the function without `()` in the variable `template` which will also be used by Spinne. The last two lines is where you specify the host and port using the `Server` class then runn is using the `run` method. You can stop the server by clicking `Ctrl-C`.

`home.html` has been set the home page of your website in `app.py`, you can use basic html, css and javascript, here is an example:

    <html>
    <head>
    <title>Home page</title>
    </head>
    <body>
    What would you like to see?
    <form enctype="multipart/form-data" method="post" action="/send.stmp">
    <input type="radio" name="choice" value="image" required> An image<br/>
    <input type="radio" name="choice" value="video" required> A video<br/>
    <input type="submit" value="Choose">
    </form>
    </body>
    </html>

This is a basic page which is showing the text 'What would you like to see?' and a form which contains two radio buttons, when you submit the form, you will go to `send.smtp` where your input will be used to show content.<br/>
Now you would like to use the inputs to show content on the page, you will need to write this in `send.smtp`:

    <html>
    <head>
    <title>Send</title>
    </head>
    <body>
    <%
    import Spinne
    i = Spinne.request.form('choice')
    %>
    %if i == 'image':
        <img src="/st/image.png">
    %else:
        <video width="320" height="240" controls>
        <source src="/st/movie.mp4" type="video/mp4">
        Your browser does not support the video tag.
        </video>
    %endif
    </body>
    </html>

This is a template, where you can write python code within html, as we mentioned before, we're using make template engine but you're free to use anyother template engine for development, you first get the input by the function `request.form` where you can put the name of the input you want, then according to the input (the radio button chosen), and image or a video will be shown.

Other Functions
======
Some other functions used in Spinne.
Redirection
------
To redirect from one page to another, use the `response.redirect` function.<br>
Example:

    response.redirect('/anotherpage')

Query Strings
------
To parse query strings, use the `request.query_strings` function.<br>
Example:

    request.query_strings()
    
If the path is `'/?a=b&b=c&d=e'`, the output will be `{'a': ['b'], 'b': ['c'], 'd': ['e']}`.
File Input
------
To recieve an input as a file, use the `request.file` function.<br>
Example:

    request.file('name')

The output will be a list containing two values, the first will be the filename, the second will be the file value.
Cookies
------
To make a cookie, use the `response.cookie` function.<br>
Example:

    response.cookie('copyright', 'aTechs', '/', '25-Jan-2011 18:45:20 GMT', 9999999)

The last two arguments (expires and maxage) aren't required.<br>
To get a cookie, use the `request.cookie` function.<br>
Example:

    request.cookie('copyright')

To delete a cookie, use the `response.delete_cookie` function.<br>
Example:

    response.delete_cookie('copyright')

Contact Us
======
If you need any help, would like to make a suggestion or help in development, please contact us through atechsmail@gmail.com.
