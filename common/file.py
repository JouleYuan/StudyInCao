import os


def upload_avatar(file, object, type):
    if file is not None:
        if object.file is not None:
            delete_avatar(object, type)
        id = object.id
        mimetype = file.mimetype.split('/')[1]
        file.save('file/avatar/' + type + '/' + str(id) + '.' + mimetype)
        object.avatar = mimetype


def delete_avatar(object, type):
    if object.avatar is not None:
        id = object.id
        if os.path.exists('file/avatar/' + type + '/' + str(id) + '.' + object.avatar):
            os.remove('file/avatar/' + type + '/' + str(id) + '.' + object.avatar)


def upload_resource(file, object):
    if file is not None:
        if object.file is not None:
            delete_resource(object)
        id = object.id
        mimetype = file.mimetype.split('/')[1]
        file.save('file/resource/' + str(id) + '.' + mimetype)
        object.file = mimetype


def delete_resource(object):
    if object.file is not None:
        id = object.id
        if os.path.exists('file/resource/' + str(id) + '.' + object.file):
            os.remove('file/resource/' + str(id) + '.' + object.file)
