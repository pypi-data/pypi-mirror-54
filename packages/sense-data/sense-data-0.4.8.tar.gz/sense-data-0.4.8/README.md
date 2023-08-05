# 1。该文件夹下主要是rpc相关项目和一些表的数据处理


# stock_grpc

股票rpc服务接口主要包括四大模块

# 数据准备阶段，在文件夹data_process中，具体实现功能如下：

1）从原始数据库db_choice中整合计算有用的模块信息，将其写入云端52.82.6.78的docker数据库中，
在文件夹read_write_db/sqlalchemy_to_sql/local_mysql_remote中，启动程序为data_process_remote.py
数据库的docker配置在文件夹deploy中，数据库的信息如下：
host = 52.82.6.78，port = 5002，user = root，passwd = sensedeal

2）在文件夹read_write_db/sqlalchemy_to_sql/中还包括了股票历史价格（前、后复权）计算用到的原始表的每天数据更新，启动程序为update_db_choice.py。

3）文件夹stock_price_cal中是对股票历史价格计算的程序，其计算部署在了52.82.6.78的docker中，每天计算一次同时将计算结果写入52.82.6.78的docker数据库中，
启动程序为wc_cal/cal_main.py。

4) 往redis里写入实时股价数据，write_rpc_redis和write_to_redis，rpc服务用到的是write_rpc_redis中的redis

5）copy_table_to193文件夹中程序将db_company中的部分表更新到193数据库中，子龙使用，运行copy_table_to193/copy_table_to193.py

# rpc服务端在service中

服务程序为sense_data_server.py，其可以用server_dockerfile207文件夹下的docker配置直接启动。

# rpc客户端在sense_data文件夹下

可以用setup.py制作python包，然后直接pip install sense-data调用，其具体使用方法见sense_data文件夹中的说明

# 部分docker的配置文件在deploy中，有的docker配置直接放到了模块的目录中


# stock_grpc目前实现的接口有12个

## 客户端安装方式
    pip install sense-data

## 配置settings.ini文件，用于配置rpc的IP地址和端口，比如：

[data_rpc]

host = localhost

port = 5001

## 使用方法，初始化一个实例，调用方法
    from sense_data import *
    sen = SenseDataService()
    
    ## 1-实时股价，输入股票代码字符串，输出最新的股票数据，数据形式为model
    sen.get_stock_price_tick(stock_code)
    
    ## 2-公司基本信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司基本信息，输出形式为model，或model组成的列表
    sen.get_company_info(stock_code)
    
    ## 3-公司别名，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司的别名，输出形式为model，或model组成的列表
    sen.get_company_alias(stock_code)
    比如：
    sen.get_company_alias('000045')
    sen.get_company_alias([])
    sen.get_company_alias(['000045','000046'])
    
    ## 4-每日股价，输入股票代码字符串，输出该股票历史信息
    sen.get_stock_price_day(*args)
    有三种查询方式，sen.get_stock_price_day('000020')，输出有史以来的所有数据，数据形式为model列表；
    sen.get_stock_price_day('000020', '2018-12-2')，输出指定某一天的数据，数据形式为model；
    sen.get_stock_price_day('000020', '2018-12-2', '2019-1-4')，输出指定时间段的数据，数据形式为model列表；

    ## 5-子公司，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到子公司信息，输出形式为model，或model组成的列表
    sen.get_subcompany(stock_code)

    ## 6-行业概念信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到股票对应的行业概念信息，输出形式为model，或model组成的列表
    sen.get_industry_concept(stock_code)
    
    ## 7-董监高信息，输入股票代码，允许的输入形式为股票字符串，或股票字符串+职位，输出懂事和监事的信息，每个人的数据形式是model，然后将对象存入列表中
    sen.get_chairman_supervisor(*args)
    比如：
    sen.get_chairman_supervisor('000045') 输出该公司所有的董监高人员信息
    sen.get_chairman_supervisor('000045', '懂事') 输出该公司所有的懂事人员信息

    ## 8-股东信息，输入股票代码，输出十大股东信息，每个股东的数据形式是model，然后将对象存入列表中
    sen.get_stockholder('000045')

    ## 9-返回前一个交易收盘日期，无参数，返回值形如'2019-1-28 03:00:00'的时间戳，是int型数据，李军用
    sen.get_trade_date()

    ## 10-返回四大板块（深市主板、沪市主板、创业板和中小板）的股票涨跌幅，无参数，输出板块涨跌幅model，暂时不用了
    sen.get_market_rise_fall()

    ## 11-返回60左右个行业的股票涨跌幅数据，无参数，输出涨跌幅model，暂时不用了
    sen.get_industry_rise_fall()

    ## 12-返回股市中概念板块的涨跌幅数据，无参数，输出涨跌幅model，暂时不用了
    sen.get_concept_rise_fall()

    ## 13-给个实体名字（人名，子公司名）查询其在相关上市公司扮演的角色信息，输出形式为model组成的列表
    sen.get_entity_role('重庆富桂电子有限公司')
    
    ## 14-输入股票代码，返回风觅个股质押财务信息
    sen.get_financial_info(stock_code)
    
    ## 15-输入股票代码，返回总股本，子龙用
    sen.total_shares(stock_code)
    
    ## 16-返回stock_codes中所有公司名，子龙用
    sen.get_company_name(stock_code)
    
    ## 17-输入文章标题，通过正则（新大洲控股|000571|新大洲A|新大洲），找到股票代码，广彬用
    sen.get_title_code(stock_code)
    
    ## 18-输入股票代码，返回实控人信息，子龙用
    sen.get_actual_control_person(stock_code)
    

# 所有数据的model内容见sense_data/dictobj.py中的定义










