from rest_framework.response import Response
from rest_framework.views import APIView
from .deal_data.main import Crawler

craw = Crawler()


class GoodsView(APIView):
    def post(self, request):
        if request.method == 'POST':
            data_str = request.data['cookies']
            if data_str[-1] == ',':
                data_str = data_str[:-1]

            data_dict = {
                'wk_cookie2': '104037f63fd4770828314b26ac4512db',
                'wk_unb': 'UNaDvietjA2gwA%3D%3D',
                'cna': 'cd12Hu0bljECAYx28/cgf4Nv',
                'cookie2': '2582e6a6dddbc238a8606c08a0a70343',
                'sgcookie': 'E1007O3YTdPNTqaf%2B7nqrkKqO3ZuHSdrNIW3VYz6crm5wbHLoDkBrZL3zw1r47xb5cqVAwi3N%2FpQJntkXCcG82NiY0rFxeQiiftaEh5Elh2agd0%3D',
                'uc3': 'nk2=Dl9YHNRFRNE%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dD3eMy0a0lhAIhwEQ%3D&id2=UNaDvietjA2gwA%3D%3D',
                'mtop_partitioned_detect': '1',
                '_m_h5_tk': 'd7811d60f27cc989877bd6ce90537a05_1715691119747',
                '_m_h5_tk_enc': '8bf5840cfc044431801eda20944449a2',
            }

            try:
                items = data_str.split(',')
                for item in items:
                    if item:
                        item = item.replace("'", "").strip().replace(" ", "")
                        key, value = item.strip().split(':')
                        if key in data_dict.keys():
                            data_dict[key] = value

                page = int(request.data['page'])
                key_word = request.data['input']
                craw.send_params(data_dict, key_word)
                goods = craw.start(page)
                return Response({'goods': goods})

            except Exception as e:
                print(e)
                return Response({'error': '格式錯誤，請檢查输入。'})
        return Response({'error': '請使用POST方法。'})
