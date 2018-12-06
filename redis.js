var express = require('express');
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }))
const redis = require('redis')

const client = redis.createClient(6379, 'hiiboy.com');

client.auth('810302',function(err, reply) {
 console.log(reply);
});

app.post('/mt5', function (req, res) {
	var str = Object.getOwnPropertyNames(req.body)[0];
	var obj = JSON.parse(str);
	client.sadd("mt5",str);
//	client.keys('mt*',function(err, reply) {
//	    console.log('mt'+reply.length);
//		num = reply.length+1;
//		client.set('mt'+num,str);
//	});
	res.end("i am express mt5");
})

app.get('/redis', function (req, res) {
	client.hgetall("user", function (err, obj) {	
		res.end(JSON.stringify(obj));
	});
})
 app.get('/', function (req, res) {
	res.end("hello world");
})
var server = app.listen(80, function () {
 
  var host = server.address().address
  var port = server.address().port
 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
 
})