//var server=require("http").createServer().listen(12341)


var fs=require("fs")


var express = require('express');
var app = express();
var bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({ extended: false }));

app.use(express.static(__dirname + '/public'));

app.listen(process.env.PORT || 12341);



var list=[]
list.push("raspberry")
list.push("mead")
list.push("plum")

var stuff, website

stuff="<form class=\"form-inline\" id=\"bing\" action=\"\" method=\"post\"><input type=\"hidden\" id=\"hello\" name=\"poo\" value=\"vomit\" />"
list.forEach(function(e) {
	stuff+="<button type=\"submit\" class=\"btn btn-lg btn-primary\" onclick=\"document.getElementById('hello').value=this.value;\" value=\""+e+"\">"+e+"</button>"
})
stuff+="</form>"
website="<!DOCTYPE html><html lang=\"en\"> <head> <meta charset=\"utf-8\"> <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <title>Wine Ticker</title> <link href=\"bootstrap-3.3.5-dist/css/bootstrap.min.css\" rel=\"stylesheet\"> <!--[if lt IE 9]> <script src=\"https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js\"></script> <script src=\"https://oss.maxcdn.com/respond/1.4.2/respond.min.js\"></script> <![endif]--> </head> <body> "+stuff+"  </body></html>"


function donormal(res) {

	res.writeHead(200,{"Content-type":"text/html"});
	res.write(website);
	res.end()
}

app.post("/",function(req,res){

	console.log("hello",req.body)	

	dd=new Date()
	fs.appendFile('bubble-data.txt', JSON.stringify({"ip":req.ip  ,"tag":req.body.poo  , "time":dd.getTime() })+"\n", function (err) {
		//console.log("bah")
	});
	donormal(res)

})

app.get("/",function(req,res){
	console.log("simple get",req.ip)

	donormal(res)
})

/*

var handler;

server.on("request", function(a,b) { handler(a,b) })




var stuff,website;

var handler1=function(req,res) {
	res.writeHead(200,{"Content-Type": "text/html"});
	res.write("hello Gabriel");
	res.end();
}


var handler2 =function(req,res) { res.writeHead(200,{"Content-type":"text/html"}); res.write(stuff); res.end() }


var handler3 =function(req,res) {

	console.log("hello",req.url,req.method);
	if (req.url === undefined) req.url=""
	console.log(req.url,"poop")

	res.writeHead(200,{"Content-type":"text/html"});

	if (req.method=="POST") {
		
		console.log("post detected")

		req.on('data', function(chunk) {
			console.log("Received body data:");
			console.log(chunk.toString());
		});
    
		res.write(website);
		
	
	} else {

		if (req.url=="/") {
			res.write(website);
		} else {
			try {
				res.write(fs.readFileSync("."+req.url))
			} catch(ex) { }
		}
	}

	res.end()

}


handler=handler3



var list=[]
list.push("raspberry")
list.push("mead")
list.push("plum")


stuff="<div class=\"row\"><div class=\"col-md-1\">.col-md-1</div><div class=\"col-md-1\">.col-md-1</div></div><form class=\"form-inline\" id=\"bing\" action=\"\" method=\"post\"><input type=\"hidden\" id=\"hello\" name=\"poo\" value=\"vomit\" />"
list.forEach(function(e) {
	stuff+="<button type=\"submit\" class=\"btn btn-lg btn-primary\" onclick=\"document.getElementById('hello').value=this.value;\" value=\""+e+"\">"+e+"</button>"
})
stuff+="</form>"


website="<!DOCTYPE html><html lang=\"en\"> <head> <meta charset=\"utf-8\"> <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <title>Wine Ticker</title> <link href=\"bootstrap-3.3.5-dist/css/bootstrap.min.css\" rel=\"stylesheet\"> <!--[if lt IE 9]> <script src=\"https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js\"></script> <script src=\"https://oss.maxcdn.com/respond/1.4.2/respond.min.js\"></script> <![endif]--> </head> <body> "+stuff+"  </body></html>"

*/
/*website="<!DOCTYPE html><html lang=\"en\"> <head> <meta charset=\"utf-8\"> <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <title>Wine Ticker</title> <link href=\"bootstrap-3.3.5-dist/css/bootstrap.min.css\" rel=\"stylesheet\"> <!--[if lt IE 9]> <script src=\"https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js\"></script> <script src=\"https://oss.maxcdn.com/respond/1.4.2/respond.min.js\"></script> <![endif]--> </head> <body> "+stuff+" <script src=\"bootstrap-3.3.5-dist/js/bootstrap.min.js\"></script> </body></html>"*/
