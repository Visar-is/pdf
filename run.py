import logging
import flask
import flask_config

from wsgiref.util import FileWrapper
from pywkher import generate_pdf

app = flask.Flask(__name__)
app.static_folder = "public"
app.SEND_FILE_MAX_AGE_DEFAULT = 0

@app.route('/')
def home():
    """Returns html that is useful for understanding, debugging and extending
    the charting API"""

    return file('public/index.html').read()


@app.route('/html-to-pdf', methods=['POST'])
def html_to_pdf():
    """Takes an HTTP POST of html data and returns a pdf.

    Example use with jQuery:

        $.post('/html-to-pdf, {'html': HTML_DATA})

    """
    raw_html = flask.request.form.get('html', '')
    
    print raw_html

    if raw_html:
        pdf_file = generate_pdf(html=raw_html)
        return flask.Response(response=pdf_file,
                                  status=200,
                                  mimetype='application/pdf')
    else:
        flask.abort(400)


if __name__ == '__main__':

    # Set up logging to stdout, which ends up in Heroku logs
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    app.logger.addHandler(stream_handler)

    app.debug = flask_config.debug
    app.run(host='0.0.0.0', port=flask_config.port)
