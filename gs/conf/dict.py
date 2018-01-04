# -*- coding:utf-8 -*-
import logging

logger = logging.getLogger('dict')

SEX = 'SEX'

STUDY_STATUS = 'STUDY_STATUS'

__MYDICT = {
    SEX: {
        1: u'男',
        2: u'女'
    },
    STUDY_STATUS: {
        0: u'未预审',
        1: u'已预审',
        2: u'报告待书写',
        3: u'报告已书写',
        4: u'报告已审核'
    }
}

CONST_DICT = {
    1: u'否',
    2: u'是'
}

ICLASS_TEXTURE = {
    1: [5],
    2: [5],
    3: [1],
    4: [2, 3, 4],
    5: [5]
}

ROLES_DICT = {
    'admin': u'管理',
    'write': u'书写',
    'review': u'审核',
    'pview': u'预审'
}
NODULE_DICT = {
    'texture': {
        0: u'磨玻璃影',
        1: u'磨玻璃',
        2: u'半实性',
        3: u'实性',
        4: u'部分钙化',
        5: u'钙化'
    },
    'iclass': {
        1: u'完全钙化',
        2: u'部分钙化',
        3: u'磨玻璃',
        4: u'半实性',
        5: u'实性'
    },
    'part': {
        1: u'右上叶',
        2: u'右中叶',
        3: u'右下叶',
        4: u'左上叶',
        5: u'左下叶',
        6: u'气管内结节',
        7: u'全肺',
        8: u'左肺',
        9: u'右肺'
    },
    'ntype': {
        1: u'结节',
        2: u'肺癌',
        3: u'结核',
        4: u'良性疾病',
        5: u'气胸',
        6: u'肿瘤',
        7: u'其他'
    },
    'typecodes': {
        'MASS': u'肿块',
        'NODULE': u'结节',
        'OTHER': u'其它',
        'BENIGN': u'良性',
        'LYMPH': u'肺内淋巴结',
        'TUBERCULOSIS': u'结核',
        'INFLAMMATION': u'炎症',
        'CRYPTOCOCCUS': u'隐球菌',
        'MALIGNANCY': u'恶性',
        'AAH': u'AAH（非典型腺瘤样增生）',
        'AIS': u'AIS（原位腺癌）',
        'MIA': u'MIA（微侵袭腺癌）',
        'AB': u'AB（侵润性肺癌）'
    }
}

TYPE_OPTION = [
    {
        'value': 'NODULE',
        'label': u'结节',
        'children': [
            {
                'value': 'BENIGN',
                'label': u'良性',
                'children': [
                    {
                        'value': 'LYMPH',
                        'label': u'肺内淋巴结',
                    },
                    {
                        'value': 'TUBERCULOSIS',
                        'label': u'结核',
                    },
                    {
                        'value': 'INFLAMMATION',
                        'label': u'炎症',
                    },
                    {
                        'value': 'CRYPTOCOCCUS',
                        'label': u'隐球菌',
                    },
                    {
                        'value': 'OTHER',
                        'label': u'其它',
                    }
                ]
            },
            {
                'value': 'MALIGNANCY',
                'label': u'恶性',
                'children': [
                    {
                        'value': 'AAH',
                        'label': u'AAH（非典型腺瘤样增生）'
                    },
                    {
                        'value': 'AIS',
                        'label': u'AIS（原位腺癌）'
                    },
                    {
                        'value': 'MIA',
                        'label': u'MIA（微侵袭腺癌）'
                    },
                    {
                        'value': 'AB',
                        'label': u'AB（侵润性肺癌）'
                    },
                    {
                        'value': 'OTHER',
                        'label': u'其它',
                    }
                ]
            }
        ]
    },
    {
        'value': 'MASS',
        'label': u'肿块'
    },
    {
        'value': 'OTHER',
        'label': u'其它'
    }
]


def get_dict_text(d_type, d_key):
    try:
        return __MYDICT[d_type][d_key]
    except Exception, e:
        logger.error(e)
        return None


def text_value_list(d_type, reverse=False):
    try:
        items = []
        type_dict = __MYDICT[d_type]
        for k, v in type_dict.iteritems():
            items.append({'text': v, 'value': k})
        items.sort(key=lambda x: x['value'], reverse=reverse)
        return items
    except Exception, e:
        logger.error(e)
        return None
