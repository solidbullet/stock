//引入模块
const http =require("http");
var URL = require('url');
const redis = require('redis')

var util = require('util');
const fs= require("fs");
//创建服务器
const server = http.createServer(function(req,res){
	const client = redis.createClient(6379, '127.0.0.1')
	end = req.url.indexOf("?");
	//console.log(req.url.slice(0,end));
	res.writeHead(200,{"Content-Type":"text/html;charset=UTF-8",'Access-Control-Allow-Origin':'hiiboy.com:8888'})
	//请求的路由地址
	if(req.url == "/" || req.url=="/index.html"){
		
		fs.readFile("index.html",function(err,data){
			//加载的数据结束
			res.end(data)
		})
	}else if(req.url == "/auth" || req.url=="/draw.html"){
			fs.readFile("auth.html",function(err,data){
				//设置响应头
				//加载的数据结束
				res.end(data)
			})
	}else if(req.url == "/redis"){
		client.hgetall("user", function (err, obj) {	
			res.end(JSON.stringify(obj));
		});	
	}else if(req.url.slice(0,end) == "/save"){
		var arg = URL.parse(req.url,true).query;  //方法二arg => { account: '001', auth: '1' }
		/*
		client.set('hello', JSON.stringify(arg)) // 注意，value会被转为字符串,所以存的时候要先把value 转为json字符串
		client.get('hello', function(err, value){
			console.log(value)
		})
		*/
		client.hset('user', arg.account,arg.auth, function(data) {
			  console.log(arg.account,"  ",arg.auth)
		})
		//res.writeHead(200,{'Access-Control-Allow-Origin':'hiiboy.com:8888'});
		res.end("save");
				
	}else{
			//加载的数据结束
			res.end('<h1> 所需内容未找到404 </h1>')
	}

}).listen(8888)
