import requests
import json
import csv
import datetime

class Getpage:
    def __init__(self):

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
            'path': '/wechat/getCafe/getreceivegiftpacksactivity?id=9C2I7YItgq5A7fRCc7usMOox4afPggUAR4g97A%2Cry2I7YItWq5U7fRCVF0P9tOWEWWpvCIGY8Gszw&isLook=false',
            'authority': 'm.lyancoffee.com',
            'cookie': 'SESSION=e3c7de73-1485-42d3-93cb-6b92afae870c; SERVERID=854725ca38783d348a5623892a765149|1532420539|1532420538',
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
        self.urllist = []
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
        self.lasttime = packet[0]['receiveTime']
        self.firsttime = packet[-2]['receiveTime']
        self.order = str(packet.pop())
        self.first_dt = datetime.datetime.strptime(self.firsttime, '%Y-%m-%d %H:%M:%S')
        self.last_dt = datetime.datetime.strptime(self.lasttime, '%Y-%m-%d %H:%M:%S')
        print((self.last_dt - self.first_dt).total_seconds()/60)
        self.survival_time = (self.last_dt - self.first_dt).total_seconds()/60
        for gift in packet:
            self.customerName = gift['customerName']
            self.content = gift['content'][0]
            if len(gift['content']) == 2:
                self.content_price = gift['content'][1]
            else:
                self.content_price = ''
            self.time = gift['receiveTime']
            self.csvrow.append(self.order)
            self.csvrow.append(str(self.survival_time))
            self.csvrow.append(self.customerName)
            self.csvrow.append(self.content)
            self.csvrow.append(self.content_price)
            self.csvrow.append(self.time)
            self.csvdata.append(self.csvrow)
            self.csvrow = []
        print(self.csvdata)

class Csvio:
    def __init__(self):
        self.id_list = []

    def csvwrite(self, datapacket):
        with open('coffee.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(datapacket)
            f.close()
        parser.csvdata = []

    def csvread(self, filename):
        with open(filename, 'r') as f:
            rows = csv.reader(f)
            for row in rows:
                self.id_list.extend(row)
            f.close()
        return self.id_list

if __name__ == '__main__':
    getpage = Getpage()
    parser = Parser()
    csvio = Csvio()
    getpage.urllist = csvio.csvread('LinkShareItemscsv.csv')
    print(getpage.urllist)
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
        csvio.csvwrite(parser.csvdata)

        


