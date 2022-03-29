var http = require('http');
var url = require('url');
const fs = require('fs');
const { strict } = require('assert');
const res = require('express/lib/response');
const { parse } = require('csv-parse/sync');
const { exec } = require('child_process');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  if(filename === "./" || filename === "./index.html")  {
    let hi = buildIndex();
    data = fs.readFileSync("index.html");
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write(hi);
    res.write(data);

    return res.end();
  }
  switch(filename) {
    case "./download.html":
      data = fs.readFileSync("download.html");
      if(q.query.year == "" || q.query.year == null) {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write(data)
        return res.end();
      }
      try {
        exec('zip -r data.zip data/ -i data/'+q.query.year+'*.csv', (err, stdout, stderr) => {
          if (err) {
            console.log('failed to zip file');
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data)
            res.write("invalid year");
            return;
          }
          // the *entire* stdout and stderr (buffered)
          console.log(`stdout: ${stdout}`);
          console.log(`stderr: ${stderr}`);
          fs.readFile("data.zip", function(err,file) {
            res.setHeader("Content-Disposition", "attachment; filename=data.zip");
            res.write(file);
            res.end();
          }
          )
        });
      }
      catch {
        console.log('failed to send file');
        return res.end();
      }
      break;
  }
  
}).listen(8080, () => console.log("server start"));

function buildIndex() {
  let date_ob = new Date();
  let year = date_ob.getFullYear();
  let out = "<script>\nfunction func() {\n";
  let ids = [];
  let contents = [];
  fs.readdirSync("./data/").forEach(file => {
    if(file.substring(0,4) == year.toString()) {
      let id = file.substring(5,file.length-4);
      ids=ids.concat([id]);
      let content = fs.readFileSync("./data/"+file)
      contents=contents.concat([content]);
    }
  });
  var list = [];
  ids.forEach(function(item, iter){
    list=list.concat([[item,contents[iter]]]);
  });
  list.sort(function(a, b){  
    return a[0] - b[0];
  });
  list.forEach(function(item,iter) {
    ids[iter] = item[0];
    contents[iter] = item[1];
  })
  contents.forEach(function(item,iter) {
    let id = ids[iter];
    let rows = parse(item, {columns: false, trim: true});
    lastData = rows[rows.length-1];
    let time = new Date(lastData[0]*1000);
    time = convertTZ(time, "America/Toronto")
    let data1 = "Hive "+id+" at "+time.toLocaleString();
    let data2= lastData[1]+" lb(s),\t"+lastData[2]+" C, \t"+lastData[3]+"% humidity";
    out += "const node"+id+" = document.createElement('p');\n";
    out+= "const textnode"+id+" = document.createTextNode('"+data1+"');\n";
    out+="node"+id+".appendChild(textnode"+id+")\n"

    out += "const info"+id+" = document.createElement('p');\n";
    out+= "const textinfo"+id+" = document.createTextNode('"+data2+"');\n";
    out+="info"+id+".appendChild(textinfo"+id+")\n"
    out += "document.getElementById('currentinfo').appendChild(node"+id+")\n";
    out += "document.getElementById('currentinfo').appendChild(info"+id+")\n";
  });
  out+="}\n</script>"
  return out;
}

function convertTZ(date, tzString) {
  return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", {timeZone: tzString}));   
}