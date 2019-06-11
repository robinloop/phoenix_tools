# Tips

python脚本，用来做一些数据处理

## 使用方式

* 1.首先安装依赖， 解压后，在tips目录下执行 pip install -r requirements.txt(如果没有配置国内源，使用阿里云的镜像：pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/)
   
* 2.安装成功后，执行python main.py即可，观察控制台输出信息（有错误截图告诉我）
* 3.目录说明：
    * data：放置指数csv文件：temp_pb.csv
    * output：指数温度html输出目录
    * 其他目录是程序代码使用目录，不用管，也不要动
    
## 2019-03-24更新
* 增加执行参数 python main.py 2019-03-24 
* 增加日期参数，注意日期格式（月和日1-9需要前面补0）
* 不添加参数时生成图表日期为指数最新日期（比如周末生成时，日期为周五的，因为周末没有指数信息）

## 2019-03-31更新
* 新增各指数温度历史趋势图 python main.py 2019-03-24 执行时可在output目录下查看趋势HTML文件
* 可输出任意指定日期的温度 python main.py -h 2019-03-27 (如果输入日期无相关数据，会报错)

## 2019-06-11更新
* 新增温度值显示参数，使用方式python main.py -s 执行时增加-s参数生成带温度值的chart图，不带-s默认生成不带温度值的chart图，







