import requests
import execjs
import os


class Crawler:
    def __init__(self):
        self.count = 0
        self.goods = []
        self.key_word = ''
        self.cookies = {}
        self._m_h5_tk = ''
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'}
        self.params = {'jsv': '2.6.2', 'appKey': '12574478', 't': '', 'sign': '',
                       'api': 'mtop.relationrecommend.wirelessrecommend.recommend', 'v': '2.0', 'type': 'json',
                       'dataType': 'json',
                       'callback': 'mtopjsonp3',
                       'data': ''}

    def _get_sign(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'main.js')
        with open(file_path, 'r') as f:
            content = f.read()
        js_content = execjs.compile(content)
        result = js_content.call('main', self.params['data'], self._m_h5_tk)

        self.params['sign'] = result['sign']
        self.params['t'] = result['t']

    def _get_data(self, page=1):
        data = '{"appId":"34385","params":"{\\"device\\":\\"HMA-AL00\\",\\"isBeta\\":\\"false\\",\\"grayHair\\":\\"false\\",\\"from\\":\\"nt_history\\",\\"brand\\":\\"HUAWEI\\",\\"info\\":\\"wifi\\",\\"index\\":\\"4\\",\\"rainbow\\":\\"\\",\\"schemaType\\":\\"auction\\",\\"elderHome\\":\\"false\\",\\"isEnterSrpSearch\\":\\"true\\",\\"newSearch\\":\\"false\\",\\"network\\":\\"wifi\\",\\"subtype\\":\\"\\",\\"hasPreposeFilter\\":\\"false\\",\\"prepositionVersion\\":\\"v2\\",\\"client_os\\":\\"Android\\",\\"gpsEnabled\\":\\"false\\",\\"searchDoorFrom\\":\\"srp\\",\\"debug_rerankNewOpenCard\\":\\"false\\",\\"homePageVersion\\":\\"v7\\",\\"searchElderHomeOpen\\":\\"false\\",\\"search_action\\":\\"initiative\\",\\"sugg\\":\\"_4_1\\",\\"sversion\\":\\"13.6\\",\\"style\\":\\"list\\",\\"ttid\\":\\"600000@taobao_pc_10.7.0\\",\\"needTabs\\":\\"true\\",\\"areaCode\\":\\"CN\\",\\"vm\\":\\"nw\\",\\"countryNum\\":\\"156\\",\\"m\\":\\"pc\\",\\"page\\":\\"'
        data_suffix_page = '\\",\\"n\\":48,\\"q\\":\\"'
        data_suffix_key_word = '\\",\\"tab\\":\\"all\\",\\"pageSize\\":48,\\"totalPage\\":100,\\"totalResults\\":4800,\\"sourceS\\":\\"0\\",\\"sort\\":\\"_coefp\\",\\"bcoffset\\":\\"\\",\\"ntoffset\\":\\"\\",\\"filterTag\\":\\"\\",\\"service\\":\\"\\",\\"prop\\":\\"\\",\\"loc\\":\\"\\",\\"start_price\\":null,\\"end_price\\":null,\\"startPrice\\":null,\\"endPrice\\":null,\\"itemIds\\":null,\\"p4pIds\\":null,\\"categoryp\\":\\"\\"}"}'
        data = data + str(page) + data_suffix_page + self.key_word + data_suffix_key_word
        self.params['data'] = data

    def _get_goods_data(self):
        response = requests.get(
            'https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/',
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
        )

        if response.json()['ret'] == ['SUCCESS::调用成功']:
            self.goods.append(response.json()['data']['itemsArray'])
            return True
        else:
            self.goods = ['請更新cookie']
            return False

    def start(self, page=1):
        self.goods = []
        for i in range(page):
            self._get_data(i + 1)
            self._get_sign()
            goods = self._get_goods_data()
            if not goods:
                return self.goods[0]
        return self.goods

    def send_params(self, data, key_word):
        self.key_word = key_word
        self.cookies = data
        self._m_h5_tk = data['_m_h5_tk']

    def get_item(self, item):
        data = []
        for good in self.goods:
            data.append(good[item])
        return data
