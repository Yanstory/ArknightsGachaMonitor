# ArknightsGachaMonitor
基于明日方舟客户端本身的抽卡模拟器。
### 当前对应客户端版本：0.7.28
## 使用
### 环境
* Python 2.7(.15)
* Flask

Flask安装：
```bash
pip install flask
```
### 开始运行
```bash
git clone https://github.com/guch8017/ArknightsGachaMonitor.git
cd ArknightsGachaMonitor/src
python app.py
```
### 数据导向更改
通过Charles将游戏封包数据导向抽卡模拟器实现模拟抽卡效果
安装Charles SSL证书并确定能成功解码手机/模拟器的https数据后，进行下列操作：
* 选中 Tools - Map Remote （macOS快捷键 option+command+M）
* 点击Add，添加一条转发规则，如下图填写参数
![map.png](https://github.com/guch8017/ArknightsGachaMonitor/raw/master/images/map.png)
抽卡前需确保合成玉数量>=6000。否则请进行以下操作修改本地的合成玉数量。
* 再次点击Add，添加以下规则。
![syncData.png](https://github.com/guch8017/ArknightsGachaMonitor/raw/master/images/syncData.png)
最后确保将Enable Map Remote开关选中，重新登陆游戏即可。

### 指定抽取概率
通过notepad++，sublime text或类似软件打开python文件，将常量部分下
```python
# 保底数量(修改为0时无保底)
startAdd = 50
# 抽出概率，依次为：六星，六星保底概率增加，五星，四星
percentageSSSR = 2
percentageSSSRAdd = 2
percentageSSR = 8
percentageSR = 50
# 特殊UP活动,分别对应3、4、5、6
chanceUp = [[], [], [], []]
```
分别按注释改为需要的值。UP出率默认为占同星级中的50%

### 指定抽取列表
通过notepad++，sublime text或类似软件打开python文件，将常量部分下
```python
selfDefined = False
selfDefinedList = []
```
改为
```python
selfDefined = True
selfDefinedList = ['charid']
```
注意：charid为角色ID，具体对应可启动程序后通过浏览器访问['http://127.0.0.1:5000/showDb](http://127.0.0.1:5000/showDb)页面查看，一定要填满十个ID否则程序将出错。

### 抽取限定干员

**注意：**由于限定干员不可能抽取，因此正常情况下出现在十连界面是不可能的！

通过notepad++，sublime text或类似软件打开python文件，将常量部分下

```python
allowLimitOp = False
```

改为

```python
allowLimitOp = True
```

即可在寻访模拟器中抽取到下方 ``limitOpList`` 中的干员（包括：公招限定，活动限定，特殊获取的干员）

## 样例
以下是模拟全六星的截图
![example1](https://github.com/guch8017/ArknightsGachaMonitor/raw/master/images/example1.png)
![example2](https://github.com/guch8017/ArknightsGachaMonitor/raw/master/images/example2.png)

## 更新日志
### 0.0.1
~~部分角色皮肤出现问题，已知原因为部分角色皮肤非常规命名（干员名#1），待修复。~~ 

修正偶尔出现空白人物的bug。确认到为部分召唤物与人物数据共同存储导致问题，已修复。
### 0.0.2
~~计划添加指定抽取人物功能，你也可以去豹跳了（误）。~~

已经添加指定出货列表
### 0.0.3
~~貌似可以抽出暴行，阿米娅。。。~~

~~已经加入后缀检测，去除不能在寻访中出现的干员~~

加入了一个开关，可以自定义是否能够抽取了

## Bugs&Todos

1. 信物获取数据暂未添加，故不会出现信物/黄票获取界面。
2. 添加抽取统计，是欧是非一看便知。


## 感谢
角色数据来源：[ArknightsGameData](https://github.com/Perfare/ArknightsGameData)

