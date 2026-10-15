import tornado.web, tornado.ioloop
import tornado.gen
import tornado.ioloop
import tornado.web
import tornado.escape
import os
import shutil
import unicodedata
import re
import datetime

# ROOT_DIR = '/Users/d3v3l0p3r90/work/dopune/'
# PDF_DIR = ROOT_DIR + 'events-pdf/'
ROOT_DIR = '/home/admin/events-pdf-service/'
PDF_DIR = ROOT_DIR + 'files/'

USERNAME = 'dopune'
PASSWORD = 'kmNB696'


# return timestamp)
def finfo(file_path):
    def convert_bytes(num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size), str(datetime.datetime.fromtimestamp(os.path.getctime(file_path)).replace(microsecond=0))
    return None, None


def get_pdf_list():
    pdfs = []
    for i in os.listdir(PDF_DIR):
        size, created = finfo(PDF_DIR + i)
        if size and created:
            pdfs.append({
                'name'   : i,
                'size'   : size,
                'created': created,
            })
    return pdfs


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '-', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


class EventsDPF(tornado.web.RequestHandler):

    async def get(self):
        await self.render("pdf.html", title="PREMIERBET DOPUNE / LISTE", pdf_list=get_pdf_list())


class EventsUpload(tornado.web.RequestHandler):

    def as_dict(self):
        response = {}
        for val in self.request.body_arguments.items():
            if len(val[1]) > 1:
                response[val[0]] = []
                for item in val[1]:
                    response[val[0]].append(item.decode('utf8'))
            else:
                response[val[0]] = val[1][0].decode('utf8')
        return response

    async def get(self):
        await self.render("uploader.html", title="PREMIERBET DOPUNE / LISTE", pdf_list=get_pdf_list())

    async def post(self):
        body = self.as_dict()

        if body.get('action') == 'delete':
            files = body.get('filesForDeletion', [])

            if isinstance(files, str):
                try:
                    os.remove(PDF_DIR + files)
                except Exception as e:
                    pass
            else:
                for fn in files:
                    try:
                        os.remove(PDF_DIR + fn)
                    except Exception as e:
                        pass

        elif body.get('action') == 'upload':
            for xfile in self.request.files.get('uploadedFile', []):
                fn, ex = os.path.splitext(xfile['filename'])
                filename = slugify(fn) + ex

                TMP_FILE = '/tmp/' + filename
                with open(TMP_FILE, 'wb') as fh:
                    fh.write(xfile['body'])

                    if not os.path.exists(PDF_DIR):
                        os.system('mkdir %s -p ' % PDF_DIR)

                    if os.path.exists(PDF_DIR + filename):
                        os.remove(PDF_DIR + filename)
                    shutil.move(TMP_FILE, PDF_DIR)

        await self.render("uploader.html", title="PREMIERBET DOPUNE / LISTE", pdf_list=get_pdf_list())


class NotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        raise tornado.web.HTTPError(
            status_code=404,
            reason='NOT_FOUND'
        )


def make_app():
    return tornado.web.Application([
        (r"/", EventsDPF),
        (r"/upload", EventsUpload),
    ], debug=False, default_handler_class=NotFoundHandler)


if __name__ == "__main__":
    app = make_app()
    app.listen(7626)
    tornado.ioloop.IOLoop.current().start()

