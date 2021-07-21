#!/usr/local/bin/python
# -*- coding:utf-8 -*-

###################
#プログラム未完成
# 全く動かないので下記URLより主導で取得する
# https://www.systemtrade-kabu.com/stock-list-csv/
###################


from BeautifulSoup import BeautifulSoup
import urllib2,re

class Nikkei225Profile(object):
    def __init__(self):
        '''
        日経新聞のサイトから日経225の構成銘柄の証券コードと証券名称を取得
        '''
        self.url = 'http://www3.nikkei.co.jp/nkave/about/225_list.cfm'
        self.profile = dict()
        soup = BeautifulSoup(urllib2.urlopen(self.url))
        tablesoup = soup.find("table")
        rows = tablesoup.findAll('tr',{'bgcolor':'#FFF5DE'})
        rows += tablesoup.findAll('tr',{'bgcolor':'#F0E7D1'})
        for row in rows:
            row_list = [cell.find(text=True) for cell in row.findAll('td')]
            self.profile[row_list[0]] = row_list[1]
    def getprofile(self,googlestyle=False):
        '''
        日経225の証券コードと証券名称をdict()で返す
        引数:googlestyleでGoogleFinanceの書式か否かを判定
        GoogleFinance書式は証券市場コード'TYO:'を証券コードの先頭に付加
        '''
        out = dict()
        if googlestyle==True:
            for k,v in self.profile.items():
                out[u'TYO:'+k] = v
            return out
        else:
            return self.profile
    def gettickers(self,googlestyle=False):
        '''
        日経225の証券コードをlist()で返す
        引数:googlestyleでGoogleFinanceの書式か否かを判定
        GoogleFinance書式は証券市場コード'TYO:'を証券コードの先頭に付加
        '''
        if googlestyle==True:
            return [u'TYO:'+ticker for ticker in self.profile.keys()]
        else:
            return self.profile.keys()

if __name__ == '__main__':
    n = Nikkei225Profile()
    print n.getprofile(googlestyle=True)
    print n.getprofile(googlestyle=False)
    print n.gettickers(googlestyle=True)
    print n.gettickers(googlestyle=False)