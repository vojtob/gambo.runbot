var AWS = require("aws-sdk");
AWS.config.update({
    region: "eu-central-1",
    endpoint: "http://localhost:8000"
});


var fs = require('fs');
var lineReader = require('readline');
var windows1250 = require('windows-1250');
var stream = require('stream');

var docClient = new AWS.DynamoDB.DocumentClient();

var bufferStream = new stream.PassThrough();

fs.readFile('../res/dataTheRunGula.csv', function (err, buf) {
    bufferStream.end(windows1250.decode(buf.toString('binary')));
});

var lineReader = require('readline').createInterface({
    input: bufferStream
});

lineReader.on('line', function (line) {
    sline = line.split(";");

    var params = {
        TableName: "RunResults",
        Item: {
            "team": 29,
            "leg": parseInt(sline[0]),
            "info": {
                "runnerName": sline[1],
                "distance": parseFloat(sline[3].replace(',', '.')),
                "plan": {
                    "duration": sline[5]
                }
            }
        }
    };
    docClient.put(params, function (err, data) {
        if (err) {
            console.error("Unable to result", line, ". Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("Put Result succeeded:", line);
        }
    });
});
