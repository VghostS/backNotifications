const projectConsts = require('../utils/projectConsts');

function getStartActions() 
{
    return {
        inline_keyboard: [
            [
                { 
                    text: 'Launch 🎮', 
                    web_app:
                    {
                        url: projectConsts.UNITY_BUILD_HOST
                    }
                }
            ]

        ],
    };
}

module.exports =
{
    getStartActions,
};