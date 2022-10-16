const dynamodb = require('aws-sdk/clients/dynamodb')
const { LambdaClient, InvokeCommand } = require('@aws-sdk/client-lambda')
const { PYTHON_TEST_ARN } = require('../constants/ARN_CONSTANTS')
const docClient = new dynamodb.DocumentClient()
const client = new LambdaClient() //{ region: process.env.REGION }
const tableName = process.env.SAMPLE_TABLE

exports.mainHandler = async (event) => {
    const { body, httpMethod, path } = event
    if (httpMethod !== 'POST') {
        throw new Error(
            `mainMethod only accepts POST method, you tried: ${httpMethod} method.`,
        )
    }
    // All log statements are written to CloudWatch by default. For more information, see
    // https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-logging.html
    console.log('received:', JSON.stringify(event))

    // Get id and name from the body of the request
    // const { id, name } = JSON.parse(body);

    const params = {
        FunctionName: PYTHON_TEST_ARN,
        LogType: 'Tail',
    }

    const command = new InvokeCommand(params)

    try {
        const { Payload } = await client.send(command)
        const asciiDecoder = new TextDecoder('ascii')
        const data = asciiDecoder.decode(Payload)
        console.log(Payload)
        console.log(data)
    } catch (error) {
        console.log('Error msg:', error.message)
        console.log(error)
    }

    const response = {
        statusCode: 200,
        body: JSON.stringify({ data: 'Hello world' }),
    }

    console.log(
        `response from: ${path} statusCode: ${response.statusCode} body: ${response.body}`,
    )
    return response
}
