import requests
import json
import csv

class Getpage:
    def __init__(self):

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
            'path': '/wechat/getCafe/getreceivegiftpacksactivity?id=9C2I7YItgq5A7fRCc7usMOox4afPggUAR4g97A%2Cry2I7YItWq5U7fRCVF0P9tOWEWWpvCIGY8Gszw&isLook=false',
            'authority': 'm.lyancoffee.com',
            'cookie': 'SESSION=e50cdc8d-1ca7-4fde-b210-8d57b2847582; SERVERID=8daf02eec50c13f6162e7fd15c04a67e|1532334346|1532334346',
            'accept': '*/*',
            'accept-encoding': 'br, gzip, deflate',
            'accept-language': 'zh-cn',
            'referer': 'https://m.lyancoffee.com/wechat/receivecoffeesuccess/giftCafeSuccess?id=9C2I7YItgq5A7fRCc7usMOox4afPggUAR4g97A,ry2I7YItWq5U7fRCVF0P9tOWEWWpvCIGY8Gszw&code=021p4nws1y6eLn0HKLws193kws1p4nwr&state=1'
        }
        self.payload = {
            'topGiftPacksActivityReceiveId': '',
            'giftPacksActivityId': '',
            'page': 2,
            'pagesize': 20
        }
        self.urllist = [
            '1lPxlEVTRddAlNZC0ArTDOPLTJwtikbh9tSzPA%2CjlPxlEVTAteBlNZCswymCJotcyneDr1o8cuFCg',
            '_12D5l5dXqVA5v9CuPh2qATl9rwmtBWvQkkbPw%2CpF2D5l5dIqUP5v9CZx6-oQaT9VEaGXamSx_vBQ',
            '_RvIrRsbG-5Arf1CLFge6a1hYzD8rWAYsQUwng%2CphvIrRsbY-63rf1CQghWHktBxChrvefJdnsd8A'
        ]
    def r_get(self, urlid):
        self.url = 'https://m.lyancoffee.com/wechat/getCafe/getreceivegiftpacksactivity?id=' + urlid + '&isLook=false'
        print(self.url)
        self.r = requests.get(self.url, headers=self.headers, verify=False)
        return self.r.text
        print(self.r.text)

    def r_post(self, orderid, receiveid, page):
        self.payload['topGiftPacksActivityReceiveId'] = receiveid
        self.payload['giftPacksActivityId'] = orderid
        self.payload['page'] = page
        print(self.payload)
        self.r = requests.post('https://m.lyancoffee.com/wechat/getCafe/getgiftPacksreceive', headers=self.headers, data=self.payload, verify=False)
        return self.r.text
class Parser:
    def __init__(self):
        self.giftlist = []
        self.packetlist = []
        self.customername = []
        self.csvdata = []
        self.csvrow = []

    def dataparser(self, pagecode):
        self.pagecode_json = json.loads(pagecode)
        if 'data' in self.pagecode_json:
            print('===============================you')
            self.orderid = self.pagecode_json['data']['shareData']['orderId']
            self.receiveid = self.pagecode_json['data']['giftPacksPageVo']['giftPacksReceiveDtoList'][-1][
                'giftPacksActivityReceiveId']

            self.gift = self.pagecode_json['data']['giftPacksPageVo']['giftPacksReceiveDtoList']
            # print(self.gift)
            self.giftlist.extend(self.gift)

            return self.orderid, self.receiveid
        else:
            print('==============================meiyou')

            self.receiveid = self.pagecode_json['giftPacksReceiveDtoList'][-1]['giftPacksActivityReceiveId']
            self.gift = self.pagecode_json['giftPacksReceiveDtoList']
            self.giftlist.extend(self.gift)
            # print(self.giftlist)
            return self.receiveid

    def end_parser(self, packet):
        # self.firsttime = packet[0]['receiveTime']
        # self.lasttime = packet[-2]['receiveTime']
        self.order = packet.pop()


        for gift in packet:
            self.customerName = gift['customerName']
            self.content = gift['content'][0]
            self.time = gift['receiveTime']
            self.csvrow.append(self.order)
            self.csvrow.append(self.customerName)
            self.csvrow.append(self.content)
            self.csvrow.append(self.time)
            self.csvdata.append(self.csvrow)
            self.csvrow = []
        print(self.csvdata)

        



if __name__ == '__main__':
    getpage = Getpage()
    parser = Parser()
    for urlid in getpage.urllist:
        pagecode = getpage.r_get(urlid)
        orderid, receiveid = parser.dataparser(pagecode)
        for page in range(2, 6):
            print(page)
            pagecode = getpage.r_post(orderid, receiveid, page)
            if len(pagecode) < 10:

                print('*******************************此页为空')
                break
            receiveid = parser.dataparser(pagecode)
            print('----------------------------------',receiveid)
        # print(parser.giftlist)
        parser.giftlist.append(orderid)
        parser.packetlist.append(parser.giftlist)
        parser.giftlist = []

    print('-----------------------红包数量：',len(parser.packetlist))
    for packet in parser.packetlist:
        parser.end_parser(packet)



        


