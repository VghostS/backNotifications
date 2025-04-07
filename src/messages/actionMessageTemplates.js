function getStartMessage(userName) 
{
    return 'Hello, ' + userName + '\n' +
    'Wish you a great Journey Ahead! \n \n' +
    'Tap Launch to Launch TLS'
}

function getSuccessPurchaseMessage(
    username, payloadId, starsAmount)
{
    return `${username}, wow, u have successfully `+
        `purchased the item <b>${payloadId}</b> for ${starsAmount}🌟`;
}

module.exports =
{
    getStartMessage,
    getSuccessPurchaseMessage,
}