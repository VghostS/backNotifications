function getUserData(message) 
{
    const names = `${message.from.first_name} `+
        `${message.from.last_name || ''}`;

    var userData = 
    {
        userId: message.from.id,
        chatId: message.chat.id,
        names: names.trim()
    }

    return userData;
}

module.exports = 
{ 
    getUserData 
};