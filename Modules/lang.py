import json

class Lang:
    
    @staticmethod
    def __(message,param0 = None, param1 = None, param2 = None):
        locale = Lang.__getLocale()
        i18n = Lang.__getTranslationFile(locale)
        
        if message in i18n:
            translatedMessage = i18n[message]

            if param0 != None and "{0}" in translatedMessage:
                translatedMessage = translatedMessage.replace('{0}',str(param0))

            if param1 != None and "{1}" in translatedMessage:
                translatedMessage = translatedMessage.replace('{1}',str(param1))

            if param2 != None and "{2}" in translatedMessage:
                translatedMessage = translatedMessage.replace('{2}',str(param2))

            return translatedMessage

        return message

    @staticmethod
    def __getLocale():
        config = open('config.json',)
        data = json.load(config)
        config.close()
        return data['locale']

    @staticmethod
    def __getTranslationFile(locale):
        config = open('./Assets/Lang/'+locale+'.json',)
        data = json.load(config)
        config.close()
        return data