# coding=utf-8
from application import app, db
import hashlib, requests, uuid  #python中的uuid模块基于信息如MAC地址、时间戳、命名空间、随机数、伪随机数来uuid
import xml.etree.ElementTree as ET


class WeChatService():
    def __init__(self, merchant_key = None):
        self.merchant_key = merchant_key


    def create_sign(self, pay_data):
        '''
        生产签名
        :param pay_data:
        :return:
        '''
        stringA = "&".join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTmep = "{0}&key={1}".format(stringA, self.merchant_key)

        sign = hashlib.md5(stringSignTmep.encode('utf-8')).hexdigest()
        return sign.upper()
    '''
    获取支付信息
    '''
    def get_pay_info(self, pay_data=None):
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        xml_data = self.dict_to_xml(pay_data)
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        headers = {
            'Content-Type': 'application/xml'
        }
        r = requests.post(url=url, data=xml_data.encode('utf-8'), headers=headers)
        r.encoding = "utf-8"
        app.logger.info(r.text)
        if r.status_code == 200:
            prepay_id = self.xml_to_dict(r.text).get("prepay_id") or '123'
            pay_sign_data = {
                'appId': pay_data.get('appid'),
                'timeStamp': pay_data.get('out_trade_no'),
                'nonceStr': pay_data.get('nonce_str'),
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD',
                'paySign': ''
            }
            #  返回的pay_sign 也是需要特殊的签名的
            pay_sign = self.create_sign(pay_sign_data)
            # 添加完签名后不需要appId
            pay_sign_data.pop('appId')
            pay_sign_data['paySign'] = pay_sign
            pay_sign_data['prepay_id'] = prepay_id
            return pay_sign_data

        return False


    def dict_to_xml(self, dict_data):
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")

        return "".join(xml)

    def xml_to_dict(self, xml_data):
        xml_dict = {}
        # fromstring() 可以在解析xml格式时，将字符串转换为Element对象，解析树的根节点
        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text

        return xml_dict

    def get_nonce_str(self):
        return str(uuid.uuid4()).replace("-", "")

