import wencai as wc





if __name__ == '__main__':
    wc.set_variable(cn_col=True, execute_path='/Users/allen/Downloads/chromedriver')

    # r = wc.get_backtest(query='上证指数上穿10日均线', start_date='2019-10-01', end_date='2019-10-19', period='1,2,3,4',
    #                     benchmark='hs000300')
    # print(r.history_detail(period='1'))

    # r = wc.get_yieldbacktest(query='非停牌；非st；今日振幅小于5%；量比小于1；涨跌幅大于-5%小于1%；流通市值小于20亿；市盈率大于25小于80；主力控盘比例从大到小',
    #                          start_date='2018-10-09', end_date='2019-07-16',
    #                          period='1',fall_income=1,lower_income=5,upper_income=9,day_buy_stock_num=1,
    #                          stock_hold=2
    #                          ).history_detail(period='3')

    r = wc.get_eventbacktest(end_date='2019-07-16',index_code="1a0001",period='1',query="上证指数上穿10日均线",
                         start_date="2016-05-16").report_data()
    print(r)



