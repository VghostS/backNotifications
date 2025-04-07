const BOT_USERNAME = 'UnigramPayment_bot';
const UNITY_BUILD_HOST = 'https://vghosts.github.io/Gmae/';

const UNIGRAM_PAYMENT_REPO = 'https://github.com/MrVeit/Veittech-UnigramPayment/blob/master/README.md';
const UNITON_CONNECT_REPO = 'https://github.com/MrVeit/Veittech-UnitonConnect';
const UNITON_CONNECT_DEMO = 'https://t.me/UnitonConnect_bot/dAppStart';

function getBotUrl()
{
    return `https://t.me/${encodeURIComponent(BOT_USERNAME)}`;
}

module.exports =
{
    BOT_USERNAME,
    UNITY_BUILD_HOST,

    UNIGRAM_PAYMENT_REPO,
    UNITON_CONNECT_REPO,
    UNITON_CONNECT_DEMO,

    getBotUrl
};