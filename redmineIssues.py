from sopel import module
from redmine import Redmine
from redmine.exceptions import AuthError, ResourceNotFoundError
from redmine.packages.requests.exceptions import MissingSchema
import re

rm = Redmine('');

@module.rule('.*#\d+')
def bug_subject(bot, trigger):
    matches = re.findall('#\d+',trigger.group(0))
    for match in matches:
        bugNum = re.search('\d+',match)
        try:
            bot.say(rm.issue.get(int(bugNum.group(0))).subject)
            bot.say(rm.url + '/issues/' + bugNum.group(0))
        except MissingSchema:
            bot.reply('No URL Set')
        except AuthError:
            bot.reply('No Key Set')
        except ResourceNotFoundError:
            bot.reply('Issue not found')

@module.commands('seturl')
def set_url(bot, trigger):
    if(trigger.owner):
        rm.url = trigger.group(2)
        bot.reply('Redmine URL set to ' + trigger.group(2))

@module.commands('setapikey')
def set_api_key(bot, trigger):
    if(trigger.owner):
        rm.key = trigger.group(2)
        bot.reply('Redmine key set to ' + trigger.group(2))