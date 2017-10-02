# 风控时间 API 文档

### 版本：v 1.2

### 更新日期： 2017/09/29


---

## 风控时间接口

### 1 获取事件

API

请求地址：

```
url = '/api/fxtime'
```

请求方法：

```
method = 'GET'
```

请求参数：

```
params = {
	start: <str>,	# 必填：开始时间 格式：yyyy-mm-dd 例：'2017-06-03'
	end: <str>,		# 必填：结束时间 格式：yyyy-mm-dd 例：'2017-06-05'
}
```

返回数据格式：

```
[
	{
		'accurate_flag': <str>,
		'actual': <str>,
		'calendar_type': <str>,
		'category_id': <str>,
		'country': <str>,             # 国家
		'currency': <str>,            # 货币种类
		'description': <str>,
		'event_row_id': <str>,
		'forecast': <str>,
		'importance': <str>,          # 重要性
		'influence': <str>,
		'level': <str>,
		'mark': <str>,
		'previous': <str>,
		'push_status': <str>,
		'related_assets': <str>,
		'remark': <str>,
		'revised': <str>,
		'stars': <str>,
		'subscribe_status': <str>,
		'ticker': <str>,
		'timestamp': <int>,           # 事件时间
		'fx_time_start': <int>,       # 风控开始时间
		'fx_time_end': <int>,         # 风控结束时间
		'timestamp_str': <str>,       # 事件时间:字符串格式
		'fx_time_start_str': <str>,   # 风控开始时间:字符串格式
		'fx_time_end_str': <str>,     # 风控结束时间:字符串格式
		'title': <str>                # 事件名称
	}
]
```

JAVASCRIPT DEMO

```
let params = {
	start: <str>,	# 开始时间
	end: <str>,		# 结束时间
}

let request = {
    url: '/api/fxtime',
    type: 'get',
    timeout: 1000,
    data: params,
    contentType: 'application/json',
    success: function (r) {
        r = JSON.parse(r)
        console.log(r)
    },
    error: function (err) {
        console.log('error', err);
    }
};

$.ajax(request)
```
