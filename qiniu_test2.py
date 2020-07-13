from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu.compat import is_py2, is_py3

def upload_img(localfile,key):
    access_key = 'fhYU85ZZoTdYf7hRhaeREhHUXsDw8g-z0it44CAO'
    secret_key = 'wNd5OMCtp5alRFLg5IvPjq-LKYtONPtbR2ztBUJI'
    bucket_name = 'oldperson'

    q = Auth(access_key, secret_key)
    #key = 'test.jpg'
    #localfile = 'plots/mysql-1.jpg'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_file(token, key, localfile)
    print(ret)
    print(info)

    if is_py2:
        assert ret['key'].encode('utf-8') == key
    elif is_py3:
        assert ret['key'] == key

    assert ret['hash'] == etag(localfile)