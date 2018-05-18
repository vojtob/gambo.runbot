var AWS = require("aws-sdk");

AWS.config.update({
    region: "eu-central-1",
    endpoint: "http://localhost:8000"
});
AWS.config.update({endpoint: "https://dynamodb.eu-central-1.amazonaws.com"});

var dynamodb = new AWS.DynamoDB();

var params = {
    TableName: "Leg",
    KeySchema: [
        { AttributeName: "leg", KeyType: "HASH" }
    ],
    AttributeDefinitions: [
        { AttributeName: "leg", AttributeType: "N" }
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 10,
        WriteCapacityUnits: 1
    }
};

dynamodb.createTable(params, function (err, data) {
    if (err) {
        console.error("Unable to create table. Error JSON:", JSON.stringify(err, null, 2));
    } else {
        console.log("Created table. Table description JSON:", JSON.stringify(data, null, 2));
    }
});
