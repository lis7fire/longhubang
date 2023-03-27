# longhubang
远程的master
抓取龙虎榜数据并存储到MySQL中

本项目需要的工具
Python3.6&Sublime3&pyquery&lxml(pyquery的依赖)&pymysql代替了mysql-connector-python;
&python3.6自带了pip，所以无需安装

本程序最终返回值：每个股票信息是一个字典格式，然后存入MySQL数据库，K-V例子如下：
{
  'stock_code': '300654',
  'rid': '300654_8',
  'name': '世纪天鸿',
  'reason': '连续三个交易日内,     跌幅偏离值累计达20%的证券',
  'totall_buy_in': '6694.69',
  'totall_sell_out': '8902.69',
  'buyers': [
    {
      'bs_name': '东吴证券股份有限公司昆山前进中路证券营业部',
      'buy_value': '2206.95',
      'sell_value': '40.20'
    },
    {
      'bs_name': '东兴证券股份有限公司厦门鹭江道证券营业部',
      'buy_value': '1843.03',
      'sell_value': '2503.24'
    },
    {
      'bs_name': '长江证券股份有限公司武汉鹦鹉大道证券营业部',
      'buy_value': '853.01',
      'sell_value': '863.08'
    },
    {
      'bs_name': '华福证券有限责任公司厦门湖滨南路证券营业部',
      'buy_value': '764.26',
      'sell_value': '947.76'
    },
    {
      'bs_name': '国金证券股份有限公司上海奉贤区金碧路证券营业部',
      'buy_value': '722.85',
      'sell_value': '789.76'
    }
  ],
  'sellers': [
    {
      'bs_name': '东兴证券股份有限公司厦门鹭江道证券营业部',
      'buy_value': '1843.03',
      'sell_value': '2503.24'
    },
    {
      'bs_name': '华泰证券股份有限公司无锡解放西路证券营业部',
      'buy_value': '267.84',
      'sell_value': '1415.69'
    },
    {
      'bs_name': '长城证券股份有限公司仙桃钱沟路证券营业部',
      'buy_value': '8.28',
      'sell_value': '1257.87'
    },
    {
      'bs_name': '华泰证券股份有限公司上海澳门路证券营业部',
      'buy_value': '28.47',
      'sell_value': '1085.09'
    },
    {
      'bs_name': '华福证券有限责任公司厦门湖滨南路证券营业部',
      'buy_value': '764.26',
      'sell_value': '947.76'
    }
  ]
}