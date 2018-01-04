# -*- coding:utf-8 -*-
# 文件存储

ACCESS_KEY = 'G5HznIKg453JgBax'
ACCESS_SECRET = 'Ieht0XsilSHv3rQg4fVZIF3R2UgsfK'

MAIN_BUCKET = 'mmarker'
IMG_ENDPOINT = 'img-cn-shanghai.aliyuncs.com'
OUTER_ENDPOINT = 'oss-cn-shanghai.aliyuncs.com'
INNER_ENDPOINT = 'oss-cn-shanghai-internal.aliyuncs.com'

__USE_ENDPOINT = OUTER_ENDPOINT
BUCKET_CONF = {
    MAIN_BUCKET: {
        'outer_host': '%s.%s' % (MAIN_BUCKET, OUTER_ENDPOINT),
        'img_outer_host': '%s.%s' % (MAIN_BUCKET, IMG_ENDPOINT),
        'img_inner_host': '%s.%s' % (MAIN_BUCKET, __USE_ENDPOINT),
        'inner_host': '%s.%s' % (MAIN_BUCKET, __USE_ENDPOINT),
        'inner_endpoint': __USE_ENDPOINT
    }
}

PRE_HTTP = 'http://'
MAIN_OUTER_HOST = BUCKET_CONF[MAIN_BUCKET]['outer_host']
IMG_OUTER_NOSLASH = PRE_HTTP + BUCKET_CONF[MAIN_BUCKET]['img_outer_host']
IMG_OUTER = IMG_OUTER_NOSLASH + '/'
HOST_INNER = PRE_HTTP + BUCKET_CONF[MAIN_BUCKET]['inner_host'] + '/'
HOST_OUTER = PRE_HTTP + MAIN_OUTER_HOST + '/'
ENDPOINT_INNER_NOSLASH = PRE_HTTP + BUCKET_CONF[MAIN_BUCKET]['inner_endpoint']
