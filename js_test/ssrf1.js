//////////////////////////////////////////
// SSRF Demo App
// Node.js Application Vulnerable to SSRF
// Written by Seth Art <sethsec@gmail.com>
// MIT Licensed
//////////////////////////////////////////

var http = require('http');
var needle = require('needle');
var express = require('express');
var axios = require('axios');
var app = express();

// Currently this app is also vulnerable to reflective XSS as well. Kind of an easter egg :)

app.get('/', function(request, response){
    var params = request.params;
    var url = request.query['url'];
    if (request.query['mime'] == 'plain'){
	var mime = 'plain';
    } else {
	var mime = 'html';
    };

    console.log('New request: '+request.url);
    console.log('New url params: '+url);

    // needle.get(url, { timeout: 3000 }, function(error, response1) {
    //   if (!error && response1.statusCode == 200) {
    //     response.writeHead(200, {'Content-Type': 'text/'+mime});
    //     response.write('<h2>I am an application. I want to be useful, so I requested: <font color="red">'+url+'</font> for you\n</h2><br><br>\n\n\n');
    //     console.log(response1.body);
    //     response.write(response1.body);
    //     response.end();
    //   } else {
    //     response.writeHead(404, {'Content-Type': 'text/'+mime});
    //     response.write('<h2>I wanted to be useful, but I could not find: <font color="red">'+url+'</font> for you\n</h2><br><br>\n\n\n');
    //     response.end();
    //     console.log('error')

    //   }
    // });

    // axios.get(url)
    //     .then(response => {
    //         console.log(response.body);
    //         console.log(response.data.url);
    //         console.log(response.data.explanation);
    //     })
    //     .catch(error => {
    //         console.log(error);
    //     });


    axios.get(url)
        .then(function (response1) {
        // handle success
            console.log(response1);
            response.writeHead(200, {'Content-Type': 'text/'+mime});
            response.write('<h2>I am an application. I want to be useful, so I requested: <font color="red">'+url+'</font> for you\n</h2><br><br>\n\n\n');
            console.log(response1.body);
            // response.write(response1.body.toString());
            // response.write(response1.statusCode.toString());
            response.end();
        })
        .catch(function (error) {
        // handle error
        console.log(error);
        })
        .then(function () {
        // always executed
        });

})

const port = 8007;

app.listen(port);
console.log('\n##################################################')
console.log('#\n#  Server listening for connections on port:'+port);
console.log('#  Connect to server using the following url: \n#  -- http://[server]:'+port+'/?url=[SSRF URL]')
console.log('#\n##################################################')