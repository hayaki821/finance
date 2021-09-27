import yfinance as yf
import time
start = time.time()

#ticker = yf.Ticker("7203.T")
ticker = yf.Ticker("3092.T")
#ticker = yf.Ticker("9433.T")
hist = ticker.history(period="max")
# 価格ヒストリカルデータを取得
print('価格ヒストリカルデータ')
print(hist)

# 損益計算書 直近3~4年分？
# 特に重要なのは、Total Revenue(売上高)、Operating Income(営業利益)、Net Income(当期純利益)あたり
financials = ticker.financials
print('損益計算書')
print(financials)
""""
                        
Research Development                 研究開発費   
Effect Of Accounting Charges         会計費用の影響   
Income Before Tax                    税引前利益      
Minority Interest                    少数株主持分    
Net Income                           当期純利益(純利益) 
Selling General Administrative       売上高 一般管理費  (販売 一般管理費)
Gross Profit                         売上総利益
Ebit                                 エビット   
Operating Income                     営業利益   
Other Operating Expenses             その他の営業費用   
Interest Expense                     支払利息   
Extraordinary Items                  特別項目  (特別損益)  
Non Recurring                        非継続的    
Other Items                          その他の項目   
Income Tax Expense                   法人税等    
Total Revenue                        売上高   
Total Operating Expenses             営業費用合計    
Cost Of Revenue                      売上原価(コストオブレベニュー)   
Total Other Income Expense Net       その他の収入と支出の合計    
Discontinued Operations              非継続事業        
Net Income From Continuing Ops       継続事業からの純利益   
Net Income Applicable To Common Shares  普通株式に帰属する純利益


"""


# 貸借対照表（バランスシート）直近3~4年分？
# Total Assets(総資産)、Total Liab(総負債)、Total Stockholder Equity(自己資本)あたり
balance_sheet = ticker.balance_sheet
print('貸借対照表（バランスシート）')
print(balance_sheet)
"""

Intangible Assets                 無形固定資産   
Capital Surplus                   資本剰余金 
Total Liab                        負債合計  
Total Stockholder Equity          株主資本合計
Minority Interest                 少数株主持分 
Deferred Long Term Liab           繰延長期負債 
Other Current Liab                その他の流動負債  
Total Assets                      総資産   
Common Stock                      普通株式      
Other Current Assets              その他の流動資産 
Retained Earnings                 利益剰余金    
Other Liab                        その他の負債    
Treasury Stock                    自己株式  
Other Assets                      その他の資産      
Cash                              キャッシュ
Total Current Liabilities         流動負債合計    
Deferred Long Term Asset Charges  繰延長期資産料
Short Long Term Debt              短期 長期債務 (短期 長期借入金)
Other Stockholder Equity          その他の株主資本
Property Plant Equipment          有形固定資産 
Total Current Assets              流動資産合計    
Long Term Investments             長期投資  
Net Tangible Assets               正味有形固定資産   
Short Term Investments            短期投資   
Net Receivables                   純債権(純受取額)
Long Term Debt                    長期借入金
Inventory                         在庫(棚卸し)
Accounts Payable                  買掛金



"""

# キャッシュフロー計算書 直近3~4年分？
# Total Cashflows From Operating Activities(営業キャッシュフロー)、
# Total Cashflows From Financing Activities(財務キャッシュフロー)、
# Total Cashflows From Investing Activities(投資キャッシュフロー)あたり
cashflow = ticker.cashflow
print('キャッシュフロー計算書')
print(cashflow)
"""

Investments                               投資(出資金)
Change To Liabilities                     負債の増減 
Total Cashflows From Investing Activities 投資活動によるキャッシュフロー合計
Net Borrowings                            純借入額            
Total Cash From Financing Activities      財務活動によるキャッシュ・フロー 合計
Change To Operating Activities            営業活動によるキャッシュ・フロー 増減    
Issuance Of Stock                         株式の発行           
Net Income                                純利益  
Change In Cash                            現金の増減 
Effect Of Exchange Rate                   為替レートの影響   
Total Cash From Operating Activities      営業活動によるキャッシュ・フロー合計
Depreciation                              減価償却費      
Other Cashflows From Investing Activities 投資活動によるその他のキャッシュフロー 
Dividends Paid                            配当金    
Change To Inventory                       在庫の変更  
Change To Account Receivables             売上債権の増減 
Other Cashflows From Financing Activities 財務活動によるその他のキャッシュフロー 
Change To Netincome                       当期純利益への変化 (当期純利益への影響)
Capital Expenditures                      設備投資額 
Repurchase Of Stock                       自己株式の取得   (自己株式の購入) 

"""

# 銘柄のサマリー
# marketCap(時価総額)、sharesOutstanding(発行株数)、forwardPE(予測PER)、
# dividendYield(配当利回り)、profitMargins(純利益比率)など
info = ticker.info
print('銘柄のサマリー')
print(info)
"""
{'zip': '471-8571', 'sector': 'Consumer Cyclical', 'fullTimeEmployees': 372434,
 'longBusinessSummary': 'Toyota Motor Corporation designs, manufactures, assembles, and sells passenger vehicles, minivans and commercial vehicles, and related parts and accessories. It operates in Automotive, Financial Services, and All Other segments. The company offers hybrid cars under the Prius, Prius PHV, C-HR, LC HV, ES HV, Camry, JPN TAXI, Avalon HV, Crown HV, Century HV, UX HV, Corolla SD, Corolla Sport, RAV4 HV, WG HV, RAV4 PHV, Highlander HV, Harrier HV, Sienna HV, UX EV, Corolla Cross HV, and Yaris HV names; fuel cell vehicles under the MIRAI and SORA names; and conventional engine vehicles, including subcompact and compact cars under the Corolla, Yaris, Corolla Sport , Aqua, Passo, Roomy, Tank, Etios, Vios, AGYA, Rush, GLANZA, Urban Cruiser, and Raize names. It also provides mini-vehicles, passenger vehicles, commercial vehicles, and auto parts under the Toyota name; mid-size cars under the Camry name; luxury cars under the Lexus, Avalon, Crown, and Century names; sports cars under the GR Yaris and Supra names; and recreational and sport-utility vehicles under the Sequoia, 4Runner, RAV4, Highlander, and Land Cruiser names. In addition, the company offers pickup trucks under the Tacoma and Tundra names; Minivans, Cabwagons, and Semi-Bonnet Wagon under the Alphard, Vellfire, Noah/Voxy, Esquire, Hiace, Sienta, and Sienna names; and trucks and buses. Further, it provides financial services, such as retail financing and leasing, wholesale financing, insurance, and credit cards; and designs, manufactures, and sells prefabricated housing. Additionally, the company operates GAZOO.com, a web portal for automobile information. It operates in Japan, North America, Europe, Asia, Central and South America, Oceania, Africa, and the Middle East. The company was founded in 1933 and is headquartered in Toyota, Japan.', 
 'city': 'Toyota', 'phone': '81 565 28 2121', 'country': 'Japan', 'companyOfficers': [],
'website': 'http://global.toyota/en', 'maxAge': 1, 'address1': '1 Toyota-cho', 'industry': 'Auto Manufacturers', 
'ebitdaMargins': 0.1492, 'profitMargins': 0.09769, 'grossMargins': 0.1942, 'operatingCashflow': 3012867915776,
 'revenueGrowth': 0.725, 'operatingMargins': 0.10414, 'ebitda': 4558013071360, 'targetLowPrice': None, 
 'recommendationKey': 'none', 'grossProfits': 4832373000000, 'freeCashflow': -667767013376, 'targetMedianPrice': None,
  'currentPrice': 9507, 'earningsGrowth': 4.647, 'currentRatio': 1.091, 'returnOnAssets': 0.03382, 'numberOfAnalystOpinions': None, 
  'targetMeanPrice': None, 'debtToEquity': 97.793, 'returnOnEquity': 0.13152, 'targetHighPrice': None, 'totalCash': 7875179053056,
  'totalDebt': 24464897081344, 'totalRevenue': 30549355790336, 'totalCashPerShare': 2818.857, 'financialCurrency': 'JPY',
  'revenuePerShare': 10926.397, 'quickRatio': 0.888, 'recommendationMean': None, 'exchange': 'JPX', 'shortName': 'TOYOTA MOTOR CORP',
 'longName': 'Toyota Motor Corporation', 'exchangeTimezoneName': 'Asia/Tokyo', 'exchangeTimezoneShortName': 'JST', 
 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '32400000', 'quoteType': 'EQUITY', 'symbol': '7203.T',
  'messageBoardId': 'finmb_319676', 'market': 'jp_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 1.44, 
  'beta3Year': None, 'enterpriseToEbitda': 9.649, '52WeekChange': 0.34087372, 'morningStarRiskRating': None, 'forwardEps': 836.47, 
  'revenueQuarterlyGrowth': None, 'sharesOutstanding': 2786530048, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 
  'totalAssets': None, 'bookValue': 8634.649, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': None, 
  'lastFiscalYearEnd': 1617148800, 'heldPercentInstitutions': 0.23674, 'netIncomeToCommon': 2984249917440, 'trailingEps': 1054.508,
   'lastDividendValue': None, 'SandP52WeekChange': 0.2874632, 'priceToBook': 1.101029, 'heldPercentInsiders': 0.13639,
    'nextFiscalYearEnd': 1680220800, 'yield': None, 'mostRecentQuarter': 1625011200, 'shortRatio': None, 
    'sharesShortPreviousMonthDate': None, 'floatShares': 2093775095, 'beta': 0.63797, 'enterpriseValue': 43979492032512,
     'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': None, 'lastSplitFactor': None, 'legalType': None,
      'lastDividendDate': None, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': 4.652, 
      'priceToSalesTrailing12Months': 0.8671718, 'dateShortInterest': None, 'pegRatio': None, 'ytdReturn': None, 
      'forwardPE': 11.365621, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 
      'impliedSharesOutstanding': None, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 9484, 
      'regularMarketOpen': 9550, 'twoHundredDayAverage': 8965.937, 'trailingAnnualDividendYield': 0.025305778, 'payoutRatio': 0.2219,
       'volume24Hr': None, 'regularMarketDayHigh': 9571, 'navPrice': None, 'averageDailyVolume10Day': 8176000, 
       'regularMarketPreviousClose': 9484, 'fiftyDayAverage': 9745.657, 'trailingAnnualDividendRate': 240, 'open': 9550,
        'toCurrency': None, 'averageVolume10days': 8176000, 'expireDate': None, 'algorithm': None, 'dividendRate': 270,
         'exDividendDate': 1617062400, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 9435, 'currency': 'JPY',
          'trailingPE': 9.015578, 'regularMarketVolume': 4728900, 'lastMarket': None, 'maxSupply': None, 'openInterest': None,
           'marketCap': 26491540733952, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 6022693, 'dayLow': 9435,
            'ask': 9508, 'askSize': 0, 'volume': 4728900, 'fiftyTwoWeekHigh': 10330, 'fromCurrency': None, 
            'fiveYearAvgDividendYield': 3.14, 'fiftyTwoWeekLow': 6780, 'bid': 9501, 'tradeable': False, 'dividendYield': 0.028499998, 
            'bidSize': 0, 'dayHigh': 9571, 'regularMarketPrice': 9507, 'logo_url': 'https://logo.clearbit.com/global.toyota'}


{'zip': '261-7116', 'sector': 'Consumer Cyclical', 'fullTimeEmployees': 1297, 'longBusinessSummary': 'ZOZO, Inc. operates online shopping Websites in Japan and internationally. It operates consignment shop, which includes various brand stores under the ZOZOTOWN name as a tenant; purchased stock shop that purchases and sells fashion merchandise of various brands; ZOZOUSED, which buys and sells used fashion-related merchandise from individual users; PayPay mall, an online shopping mall; and WEAR, a fashion app. The company also sells in-house designed apparel products; and offers various services, such as system and application development, WEB design, CRM, technology development, research and development, logistics contracting, and marketing services. In addition, it engages in the advertisement business. The company was formerly known as Start Today Co., Ltd. and changed its name to ZOZO, Inc. in October 2018. ZOZO, Inc. was founded in 1998 and is headquartered in Chiba, Japan. ZOZO, Inc. is a subsidiary of Z Holdings Corporation.', 'city': 'Chiba', 'country': 'Japan', 'companyOfficers': [], 'website': 'http://corp.zozo.com', 'maxAge': 1, 'address1': 'WBG Maribu West', 'industry': 'Internet Retail', 'address2': '15th Floor Nakase 2-6-1 Mihama-ku', 'ebitdaMargins': 0.31913, 'profitMargins': 0.21195, 'grossMargins': 0.94808, 'operatingCashflow': None, 'revenueGrowth': 0.154, 'operatingMargins': 0.30333, 'ebitda': 48697249792, 'targetLowPrice': None, 'recommendationKey': 'none', 'grossProfits': 140032000000, 'freeCashflow': None, 'targetMedianPrice': None, 'currentPrice': 4175, 'earningsGrowth': 0.206, 'currentRatio': 1.083, 'returnOnAssets': 0.32484, 'numberOfAnalystOpinions': None, 'targetMeanPrice': None, 'debtToEquity': 81.997, 'returnOnEquity': 1.0646701, 'targetHighPrice': None, 'totalCash': 27033999360, 'totalDebt': 20000000000, 'totalRevenue': 152594006016, 'totalCashPerShare': 91.079, 'financialCurrency': 'JPY', 'revenuePerShare': 501.089, 'quickRatio': 0.973, 'recommendationMean': None, 'exchange': 'JPX', 'shortName': 'ZOZO INC', 'longName': 'ZOZO, Inc.', 'exchangeTimezoneName': 'Asia/Tokyo', 'exchangeTimezoneShortName': 'JST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '32400000', 'quoteType': 'EQUITY', 'symbol': '3092.T', 'messageBoardId': 'finmb_31089922', 'market': 'jp_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 8.075, 'beta3Year': None, 'enterpriseToEbitda': 25.305, '52WeekChange': 0.39912868, 'morningStarRiskRating': None, 'forwardEps': 102.28, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 296820000, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'totalAssets': None, 'bookValue': 81.942, 'sharesShort': None, 'sharesPercentSharesOut': None, 'fundFamily': 
None, 'lastFiscalYearEnd': 1617148800, 'heldPercentInstitutions': 0.2101, 'netIncomeToCommon': 32341999616, 'trailingEps': 106.205, 'lastDividendValue': None, 'SandP52WeekChange': 0.28827727, 'priceToBook': 50.950672, 'heldPercentInsiders': 0.60148996, 'nextFiscalYearEnd': 1680220800, 'yield': None, 'mostRecentQuarter': 1625011200, 'shortRatio': None, 'sharesShortPreviousMonthDate': None, 'floatShares': 108659992, 'beta': 1.069555, 'enterpriseValue': 1232259907584, 'priceHint': 2, 'threeYearAverageReturn': None, 'lastSplitDate': None, 'lastSplitFactor': None, 'legalType': None, 'lastDividendDate': None, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': 0.193, 'priceToSalesTrailing12Months': 8.12105, 'dateShortInterest': None, 'pegRatio': None, 'ytdReturn': None, 'forwardPE': 40.81932, 'lastCapGain': None, 'shortPercentOfFloat': None, 'sharesShortPriorMonth': None, 'impliedSharesOutstanding': None, 'category': None, 'fiveYearAverageReturn': None, 'previousClose': 4245, 'regularMarketOpen': 4195, 'twoHundredDayAverage': 3595.528, 'trailingAnnualDividendYield': 0.009658421, 'payoutRatio': 0.3577, 'volume24Hr': None, 'regularMarketDayHigh': 4215, 'navPrice': None, 'averageDailyVolume10Day': 815442, 'regularMarketPreviousClose': 4245, 'fiftyDayAverage': 3784.2646, 'trailingAnnualDividendRate': 41, 'open': 4195, 'toCurrency': None, 'averageVolume10days': 815442, 'expireDate': None, 'algorithm': None, 'dividendRate': 66, 'exDividendDate': 1632873600, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 4165, 'currency': 'JPY', 'trailingPE': 39.31077, 'regularMarketVolume': 815900, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 1239223500800, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 856972, 'dayLow': 4165, 'ask': 4180, 'askSize': 0, 'volume': 815900, 'fiftyTwoWeekHigh': 4245, 'fromCurrency': None, 'fiveYearAvgDividendYield': 1.05, 'fiftyTwoWeekLow': 2424, 'bid': 4175, 'tradeable': False, 'dividendYield': 0.015800001, 'bidSize': 0, 'dayHigh': 4215, 'regularMarketPrice': 4175, 'logo_url': 'https://logo.clearbit.com/corp.zozo.com'}
## TODO 発行株数がサイトのものと一致しない

"""


# 複数銘柄を同時に取得する場合はTickersクラスを使い、引数はスペースで区切ります
tickers = yf.Tickers("7203.T 9984.T 6861.T")
hists = []
for key in tickers.tickers.keys():
    #print(tickers.tickers)
    hists.append(tickers.tickers[key].history())
print(hists[0])

# 株価以外のデータ取得（為替）
import pandas as pd
# 株海外に取れる為替データの一部
#indices = ["^N225", "^DJI", "^GSPC", "^IXIC", "^GDAXI", "^FTSE", "^FCHI", "^HSI", 
# "^SSEC", "^BVSP", "^KOSPI"]
fxs = ["JPY=X", "EURUSD=X", "GBPUSD=X"]
tickers = yf.Tickers(" ".join(fxs))

closes = []
for key in tickers.tickers.keys():
    closes.append(tickers.tickers[key].history(period="max").Close)

df = pd.DataFrame(closes).T
df.columns = fxs
print('株価以外のデータ取得（為替）')
print(df)


elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
