import os


def upload_avatar(file, object, type):
    if file is not None:
        id = object.id
        mimetype = file.mimetype.split('/')[1]
        file.save('file/avatar/' + type + '/' + str(id) + '.' + mimetype)
        object.avatar = mimetype


def delete_avatar(object, type):
    if object.avatar is not None:
        id = object.id
        if os.path.exists('file/avatar/' + type + '/' + str(id) + '.' + object.avatar):
            os.remove('file/avatar/' + type + '/' + str(id) + '.' + object.avatar)
