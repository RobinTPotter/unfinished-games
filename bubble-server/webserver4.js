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

stuff+="<div class=\"dropdown\">  <button class=\"btn btn-primary dropdown-toggle\" type=\"button\" data-toggle=\"dropdown\">Dropdown Example<span class=\"caret\"></span></button>  <ul class=\"dropdown-menu\">"
list.forEach(function(e) {
	stuff+="<li><a href=\"#\">"+e+"</a></li>"
})
stuff+="</ul></div>"
stuff+="</form>"
website="<!DOCTYPE html><html lang=\"en\"> <head> <script src=\"d3/d3.js\"></script>    <script src=\"jQuery/jquery.js\"></script>   <script src=\"bootstrap-3.3.5-dist/js/bootstrap.min.js\"></script>   <meta charset=\"utf-8\"> <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> <title>Wine Ticker</title> <link href=\"bootstrap-3.3.5-dist/css/bootstrap.min.css\" <link href=\"nvd3/nv.d3.css\" rel=\"stylesheet\"> </head> <body> "+stuff+"  </body></html>"


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
