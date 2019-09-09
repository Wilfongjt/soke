'use strict';
const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
const authorizer = require('./authorizer');
const users = require('./users');
const JWT_EXPIRATION_TIME = '5m';

const cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Accept-Langauge",
    "Access-Control-Allow-Methods": "OPTIONS,GET"
};
/* Welcome to Serverless!
 * Generated from write_handler_starter.sh
 * See serverless.yml for configuration
*/

// SIGNIN
module.exports.signin = async (event, context) => {
  // get un and pw
  const { username, password } = JSON.parse(event.body);
  try {
    const user = users.signin(username, password);
    const token = authorizer.generateToken({user});
    const response = {
      statusCode: 200,
      headers: cors_headers,
      body: JSON.stringify({
        token
      })
    };
    return response;
  } catch(e) {
    console.log('Error logging in: ${e.message}');
    const response = { // Error response
     statusCode: 401,
     headers: {
       'Access-Control-Allow-Origin': '*', // cors header
     },
     body: JSON.stringify({
       error: e.message,
     }),
    };
    return response;
  }
};
// AUTHORIZE
module.exports.authorize = async (event, context) => {
  const token = event.authorizationToken;
  try {
    // verify JWT
    const decoded = authorizer.decodeToken(token);
    // Check  user has privileges
    const user = decoded.user;
    // Check privileges to resource
    const isAllowed = authorizer.authorizeMe(user.scopes, event.methodArn);
    // return IAM poloicy
    const effect = isAllowed ? 'Allow' : 'Deny';
    const userId = user.username;
    const authorizerContext = { user: JSON.stringify(user) };
    const policy = authorizer.generatePolicy(userId, effect, event.methodArn, authorizerContext);

    return policy;
  } catch (error) {
    console.log('Unauthorized');
    return error.message;

  }
};

module.exports.index = async (event) => {
  // return list of words with link to documents
  // need to remove duplicate words
  //let keywords = event.queryStringParameters && event.queryStringParameters.keywords;
  // convert the words to lowercase before search...get around mac capitalizing first char in textbox
  const body = JSON.parse(event.body);
  let keywords = undefined;
  let vals = []; // list of keywords
  // let param = {};
  let param_list = [];
  let data = [];

  let headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type,Accept-Langauge",
      "Access-Control-Allow-Methods": "OPTIONS,GET"
  };
  if (body.words !== null) {
    keywords = body.words.toLowerCase();
  }
  // keyword not sent
  if (keywords === undefined
    || keywords === null
  ) {

    return {
      statusCode: 200, // no requested keywords
      headers: headers,
      body: JSON.stringify({})
    };
  }
  // keyword is empty
  if (keywords.length === 0) {

    return {
      statusCode: 400, // bad format
      headers: headers,
      body: JSON.stringify({})
    };
  }
  // handle multiple keywords
  vals = keywords.split(" ");

  if(vals.length === 0){
    return {
      statusCode: 400,
      headers: headers,
      body: JSON.stringify({ param_list, data }) };
  }

  let i = 0;
  /*
   prepare a search for each word
  */
  for(i = 0; i < vals.length; i++){
    let skv = "%w#1".replace("%w",vals[i]);
    // let gsi_1 = "gsi_1_"
    param_list.push({
      TableName: process.env.TABLE_NAME,
      IndexName: process.env.GSI_1,
      KeyConditionExpression: "sk = :sk1",
      ExpressionAttributeValues: {
       ":sk1": skv
      }
    });
  }
  /*
  run all the searches
  */
  const plst = [];

  try {
    for(i=0; i < param_list.length; i++){
      plst.push(docClient.query(param_list[i]).promise());
    }
  } catch(error){
    return {statusCode: 400, body: error};
  }

  // wait for the searches to end
  try {
    const results = await Promise.all(plst);

    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify({results}),
      isBase64Encoded: false
    };
  } catch(error){
    return {statusCode: 400, body: error};
  }

};

module.exports.document = async (event) => {
  /*
  returns all items for a document by pk
  {
    "pk": "d#001",
    "sk": "s#001#000001#000001",
    "data": "The brown fox jumped over the fence."
  }
  */
  let msg = 'document';
  let pk = event.pathParameters && event.pathParameters.pk;
  let headers = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type,Accept-Langauge",
      "Access-Control-Allow-Methods": "OPTIONS,GET"
  };

  if (pk === undefined) {
    msg = JSON.stringify({message: 'Missing pk {}'.replace('{}',pk)});
    return {
      statusCode: 400,
      body: msg
    };
  }
  pk = pk.replace('-', '#'); // key are formated with # and # is reserved in url so replace
  var params = {
    TableName: process.env.TABLE_NAME,
    KeyConditionExpression: "pk = :a and begins_with(sk, :t)",
    ExpressionAttributeValues: {
     ":a": pk,
     ":t": "s#"
    }
   };
   try {

     const data = await docClient.query(params).promise();

     return { statusCode: 200,
       headers: headers,
       body: JSON.stringify({ params, data }) };

   } catch (error){

     return {
       statusCode: error.statusCode,
       error: error.message
     };

   }

};
