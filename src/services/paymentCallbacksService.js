const logger = require('../utils/logger');

const { getSuccessPurchaseMessage } = require('../messages/actionMessageTemplates');
const { sendMessage } = require('../messages/messageBuilder');
const { getUserData } = require('../utils/chatUtils');
const { addNewPurchase } = require('./paymentBackendService');

async function validateInvoiceProcess(bot, 
    queryId, payload, username)
{
    await bot.answerPreCheckoutQuery(queryId, true).then(() =>
    {
        logger.message(`Stars transaction with payload `+
            `${payload} received from user ${username}`);
    })
    .catch((error) =>
    {
        logger.error(`Failed to validate PreCheckoutQuery `+
            `callback, reason: ${error.message}`);
    });
}

function validateSuccessPurchase(bot, message, options, paymentInfo)
{
    logger.message(`Received stars payment data: ${paymentInfo}`);

    const userData = getUserData(message);
    const starsAmount = paymentInfo.total_amount;
    const payloadId = paymentInfo.invoice_payload;

    const callbackMessage = getSuccessPurchaseMessage(
        userData.names, payloadId, starsAmount);

    addNewPurchase(paymentInfo);

    sendMessage(bot, userData.chatId, callbackMessage, options);
}

module.exports =
{
    validateInvoiceProcess,
    validateSuccessPurchase,
};