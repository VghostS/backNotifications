const payCallbacksService = require('../services/paymentCallbacksService');

function validateSuccessPurchase(bot, message)
{
    var options =
    {
        parse_mode: 'HTML'
    };

    const paymentInfo = message.successful_payment;

    payCallbacksService.validateSuccessPurchase(bot,
        message, options, paymentInfo);
}

async function validateInvoiceProcess(bot, query)
{
    const queryId = query.id;
    const payloadId = query.invoice_payload;
    const username = query.from.username;

    await payCallbacksService.validateInvoiceProcess(bot,
        queryId, payloadId, username);
}

module.exports =
{
    validateInvoiceProcess,
    validateSuccessPurchase,
}