const logger = require('../utils/logger');

const crypto = require('crypto-js');
const axios = require('axios');

require('dotenv').config();

const backendUrl = process.env.SERVER_DOMAIN;
const botToken = process.env.BOT_TOKEN;
const authSecret = process.env.AUTHORIZATION_SECRET_KEY;

const addNewPurchaseUrl = `${backendUrl}/api/payment/update-order-receipt`;

function addNewPurchase(paymentInfo)
{
    const encryptedAuthToken = getEncryptedAuthToken();
    
    axios.post(addNewPurchaseUrl, paymentInfo,
    {
        headers:
        {
            'Content-Type': `application/json`,
            'Authorization': `Bearer ${encryptedAuthToken}`
        }
    })
    .then(result =>
    {
        logger.message(`Purchase invoice successfully send `+
            `to backend, result: ${result.data}`);
    })
    .catch(error =>
    {
        logger.error(`Failed to send purchase invoice `+
            `to backend, reason: ${error.message}`);
    });
}

function getEncryptedAuthToken()
{
    return crypto.AES.encrypt(botToken, authSecret);
}

module.exports =
{
    addNewPurchase,
}