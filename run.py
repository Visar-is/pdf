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
    
    if raw_html:
        html = file('public/index.html').read()
        pdf_file = generate_pdf(html=html)
        print 'HTML Length: '+str(len(html))
        print 'PDF Size: '+str(pdf_file.tell())
        #pdf_file.seek(0)
        
        '''
        template = get_template('my_awesome_template.html')
        html = template.render(RequestContext(request))
        pdf_file = generate_pdf(html=html)
        response = HttpResponse(FileWrapper(pdf_file), content_type='application/pdf')
        response['Content-Disposition'] = 
        response['Content-Length'] = pdf_file.tell()
        pdf_file.seek(0)
        return response
        '''
        
        
        resp = flask.Response(response=pdf_file,
                                  status=200,
                                  mimetype='application/pdf')
        #resp.headers['Content-Disposition'] = 'attachment; filename=%s.pdf' % basename(pdf_file.name)
        #resp.headers['Content-Length'] = pdf_file.tell()
        #pdf_file.seek(0)
        return resp
    else:
        flask.abort(400)


if __name__ == '__main__':

    # Set up logging to stdout, which ends up in Heroku logs
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    app.logger.addHandler(stream_handler)

    app.debug = flask_config.debug
    app.run(host='0.0.0.0', port=flask_config.port)
