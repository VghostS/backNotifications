const logger = require('../utils/logger');

function sendMessage(bot, chatId, text, options)
{
    bot.sendMessage(chatId, text, options).then(() =>
    {
        logger.message(`Message '${text}' sended by user: ${chatId}`);
    })
    .catch((error) =>
    {
        logger.error(`Failed to send message '${text}' by `+
            `user: ${chatId}, reason: ${error.message}`);
    });
}

function sendPhoto(bot, chatId, iconIdOrPath, options)
{
    bot.sendPhoto(chatId, iconIdOrPath, options).then((result) =>
    {
        logger.message(`Message with photo sended by user: ${chatId}`);

        const fileId = result.photo[result.photo.length - 1].file_id;

        iconIdOrPath = fileId;

        logger.message(`Loaded file id ${fileId} from photo ${iconIdOrPath}`);
    })
    .catch((error) =>
    {
        logger.error(`Failed to send message with `+
            `photo ${iconIdOrPath}, reason: ${error.message}`);
    });
}

module.exports =
{
    sendMessage,
    sendPhoto
};