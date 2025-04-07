function getStartMessage(userName) 
{
    return `Good day, ${userName} 😎\n\nHere you can test the <b>Unigram Payment library</b>, ` +
    `which allows you <b>to make payments via Telegram Stars</b>, inside web applications made on Unity!`;
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