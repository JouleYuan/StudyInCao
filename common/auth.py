from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

SECRET_KEY = 'yuanhaoran0318'

login_serializer = Serializer(SECRET_KEY, expires_in=60000)  # 60000 sec
modify_password_serializer = Serializer(SECRET_KEY, expires_in=600)  # 600 sec


def create_login_token(data):
    return login_serializer.dumps(data)


def create_modify_password_token(data):
    return modify_password_serializer.dumps(data)


def verify_login_token(parser):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if 'status' in token and token['status'] == 'login':
        return True
    return False


def verify_student_token(parser):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'login') and \
       ('identity' in token and token['identity'] == 'student'):
        return True
    return False


def verify_teacher_token(parser):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'login') and \
       ('identity' in token and token['identity'] == 'teacher'):
        return True
    return False


def verify_assistant_token(parser):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'login') and \
       ('identity' in token and token['identity'] == 'assistant'):
        return True
    return False


def verify_admin_token(parser):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'login') and \
       ('identity' in token and token['identity'] == 'admin'):
        return True
    return False


def verify_id_token(parser, id):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = login_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'login') and \
       ('id' in token and token['id'] == id):
        return True
    return False


def verify_modify_password_token(parser, id):
    parser.add_argument('Token', location='headers')
    headers = parser.parse_args()
    try:
        token = modify_password_serializer.loads(headers['Token'])
    except:
        return False
    if ('status' in token and token['status'] == 'modify_password') and \
       ('id' in token and token['id'] == id):
        return True
    return False
