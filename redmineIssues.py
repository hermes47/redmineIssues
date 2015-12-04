from sopel import module, config, trigger
from sopel.config.types import StaticSection, ValidatedAttribute
from redmine import Redmine
import re

class redmineSection(StaticSection):
    url = ValidatedAttribute('url')
    apikey = ValidatedAttribute('apikey')
    channel = ValidatedAttribute('channel')

class redmineIssues():
    channel = None

def setup(bot):
    bot.config.define_section("redmine", redmineSection)
    rm.key = bot.config.redmine.apikey
    rm.url = bot.config.redmine.url
    redmineIssues.channel = bot.config.redmine.channel
    
@module.rule(r".*#\d+")
def bug_subject(bot, trigger):
    if redmineIssues.channel is None or redmineIssues.channel == trigger.sender:
        matches = re.findall(r"#(\d+)",trigger.group(0))
        for match in matches:
            try:
                bot.say(rm.issue.get(int(match)).subject)
            except Exception as ex:
                bot.say(ex)
            else:
                bot.say(rm.url + "/issues/" + match)

@module.commands(r"seturl")
def set_url(bot, trigger):
    if trigger.owner is True:
        rm.url = trigger.group(2)
        bot.config.redmine.url = rm.url
        bot.reply("Redmine URL set to " + trigger.group(2))

@module.commands(r"setapikey")
def set_api_key(bot, trigger):
    if trigger.owner is True:
        rm.key = trigger.group(2)
        bot.config.redmine.apikey = rm.key;
        bot.reply("Redmine key set to " + trigger.group(2))

@module.commands(r"lockchannel")
def lock_channel(bot, trigger):
    if trigger.owner is True:
        redmineIssues.channel = trigger.group(2)
        bot.config.redmine.channel = redmineIssues.channel
        bot.reply("Locking to channel " + trigger.group(2))
       
