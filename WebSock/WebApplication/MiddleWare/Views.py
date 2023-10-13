import os

static_path = r"WebApplication\assets\static"
media_path = r"WebApplication\assets\media"

CONTENT_TYPE_LOCKUP_TABLE = {
    'html': 'text/html',
    'htm': 'text/html',
    'shtml': 'text/html',
    'txt': 'text/plain',
    'xml': 'application/xml',
    'json': 'application/json',
    'pdf': 'application/pdf',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'ico': 'image/x-icon',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'svg': 'image/svg+xml',
    'mp3': 'audio/mpeg',
    'wav': 'audio/wav',
    'mp4': 'video/mp4',
    'avi': 'video/avi',
    'mkv': 'video/x-matroska',
    'css': 'text/css',
    'js': 'application/javascript',
    'zip': 'application/zip',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'jsonld': 'application/ld+json',
    'yaml': 'application/x-yaml',
    'rss': 'application/rss+xml',
    'atom': 'application/atom+xml',
    'csv': 'text/csv',
    'swf': 'application/x-shockwave-flash',
    'mpg': 'video/mpeg',
    'mpeg': 'video/mpeg',
    'php': 'application/x-httpd-php',
    'txt': 'text/plain',
    'rtf': 'text/rtf',
    'ogg': 'audio/ogg',
    'webm': 'video/webm',
    'ogv': 'video/ogg',
    'xhtml': 'application/xhtml+xml',
}

class ApplicationViews:
    def __init__(self):
        pass

class HTTPResponse:
    def generate_response(self):
        response = (
            f"{self.version} {self.status_code} {self.status_text}\n\r".encode('utf-8')+
            f"Content-Type: {self.content_type}\r\n\r\n".encode('utf-8')+
            self.content
                    )
        return response
    def __init__(self, content, status_code=200, status_text='OK', version="HTTP/1.1", content_type="text/html"):
        if isinstance(content, ASSET):
            content_type = CONTENT_TYPE_LOCKUP_TABLE[content.source.split('.')[-1]]
            content = content.content
        elif not isinstance(content, bytes):
            content = content.__str__().encode('utf-8')
        self.version = version
        self.status_code = status_code
        self.status_text = status_text
        self.content_type = content_type
        self.content = content
        self.response = self.generate_response()

class ASSET:
    def __init__(self, source, content):
        self.source = source
        self.content = content

def ImportStatic(path):
    file = open(os.path.join(static_path, path), 'rb')
    template = ASSET(
        source=path, content=file.read()
    ); file.close()
    return template

def ImportMedia(path):
    file = open(os.path.join(media_path, path), 'rb')
    media = ASSET(
        source=path, content=file.read()
    ); file.close()
    return media

def EmbedVars(template, vars=False):
    if not vars:
        return template
