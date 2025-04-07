const logger = require('../utils/logger');

const { getUserData } = require('../utils/chatUtils');
const { sendMessage } = require('../messages/messageBuilder');
const { getStartMessage } = require('../messages/actionMessageTemplates');

function sendStartAction(bot, message, options)
{
    const userData = getUserData(message);
    const startMessage = getStartMessage(userData.names);

    logger.message(`Parsed start message: ${startMessage}`);

    logger.message(`Parsed user data: ${JSON.stringify(userData)} `+
        `and message: '${startMessage}' for send`);

    sendMessage(bot, userData.chatId, startMessage, options);
}

module.exports =
{
    sendStartAction,
}