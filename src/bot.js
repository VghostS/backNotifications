const logger = require('./utils/logger');

const startAttachController = require('./controllers/startAttachController');
const paymentController = require('./controllers/paymentCallbacksController');

const express = require('express');
const path = require('path');;
const TelegramBot = require('node-telegram-bot-api');

require('dotenv').config();

const server = express();
const port = process.env.PORT;
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

server.use(express.static(path.join(__dirname, 'TelegramBot-UnigramPayment')));
server.use(express.json());

server.listen(port, () => 
{
    logger.message(`Unigram Payment Bot Template started at port: ${port}`);
});

bot.onText('/start', (message) => 
{
    startAttachController.sendStartMessage(bot, message);
});

bot.on('successful_payment', (message) =>
{
    paymentController.validateSuccessPurchase(bot, message);
});

bot.on('pre_checkout_query', async (query) => 
{
    await paymentController.validateInvoiceProcess(bot, query);
});

bot.on('polling_error', (error) => 
{
    logger.error(`Failed to attach with bot, reason: ${error.message}`);
});