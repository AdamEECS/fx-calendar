# 市场日历

## 系统简介

todo
1，市场大事
2，各国利率

市场日历系统

版本控制

## proxy 服务器配置

1，新开一台带 ssh-key 的 debian 8 服务器

2，安装 tinyproxy

```
apt-get install tinyproxy
```

3,修改配置文件`/etc/tinyproxy.conf`

a, Port

b, Allow

4,重启服务

```
service tinyproxy start

$sudo service tinyproxy restart

$sudo service tinyproxy stop
```

5，ufw 开启相应端口

### 客户端的使用方法
```
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}

requests.get("http://example.org", proxies=proxies)

```
