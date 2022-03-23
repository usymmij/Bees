var http = require('http');
var url = require('url');
const fs = require('fs');
const { strict } = require('assert');
const res = require('express/lib/response');
const { parse } = require('csv-parse');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  if(filename === "./" || filename === "./index.html")  {
    index(res);
    return res.end();
  }

  res.writeHead(404, {'Content-Type': 'text/html'});
  return res.end("404 Not Found");
}).listen(8080, () => console.log("server start"));

function index(res) {
  fs.readFile("./index.html", function(err, data) {
    if(err) {
      res.writeHead(404, {'Content-Type': 'text/html'});
      return res.end("404 Not Found");
    }
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(data);
    var ind = buildIndex()
    res.write(ind)
    res.end();
  });
}

function buildIndex() {
  let date_ob = new Date();
  let year = date_ob.getFullYear();
  fs.readdirSync("./data/").forEach(file => {
    if(file.substring(0,4) == year.toString()) {
      let id = (file.substring(5,file.length-9));
      let content = fs.readFileSync("./data/"+file)
      parse(content, {columns: false, trim: true}, function(err, rows) {
        lastData = rows[rows.length-1];
        let time = new Date(lastData[0]*1000);
        console.log(time)
      })
    }
  });
  return'';
}