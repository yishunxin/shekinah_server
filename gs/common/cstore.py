# -*- coding:utf-8 -*-
import base64
import datetime
import hashlib
import hmac
import json
import time
import urllib

from gs.conf import store as sconf

from gs.util import mytime


def make_sign_policy(key, policy):
    return base64.b64encode(hmac.new(key, policy, hashlib.sha1).digest())


def get_store_signature(bucket):
    utcend = mytime.add_delta(datetime.datetime.utcnow(), seconds=120)
    end = mytime.add_delta(datetime.datetime.now(), seconds=120)
    expiration = time.strftime("%Y-%m-%dT%H:%M:%SZ", utcend.timetuple())
    timestamp = time.mktime(end.timetuple())
    access_key = sconf.ACCESS_KEY
    access_secret = sconf.ACCESS_SECRET

    policy = {"expiration": expiration,
              "conditions": [["content-length-range", 0, 1048576000], {'bucket': bucket}]}
    base64policy = base64.b64encode(json.dumps(policy))
    signature = make_sign_policy(access_secret, base64policy)
    return {'access_key': access_key,
            'signature': signature,
            'policy': base64policy,
            'expire': timestamp,
            'host': sconf.MAIN_OUTER_HOST,
            'img_outer_host': sconf.IMG_OUTER_NOSLASH
            }


def get_access_signature(bucket, key):
    expire = int(mytime.datetime2num(mytime.add_delta(datetime.datetime.now(), seconds=120)))
    signature = urllib.quote(make_sign_policy(sconf.ACCESS_SECRET, "GET\n\n\n%s\n/%s/%s" % (expire, bucket, key)))
    return 'OSSAccessKeyId=%s&Expires=%s&Signature=%s' % (sconf.ACCESS_KEY, expire, signature)
