const { getStartActions } = require('../keyboards/startKeyboards');
const { sendStartAction } = require('../services/startAttachService');

function sendStartMessage(bot, message)
{
    var options =
    {
        reply_markup: getStartActions(),
        parse_mode: 'HTML'
    };

    console.log(`Parsed message options: ${JSON.stringify(options)}`);

    sendStartAction(bot, message, options);
}

module.exports = 
{
    sendStartMessage
};