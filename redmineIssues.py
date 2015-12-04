from sopel import module, config
from sopel.config.types import StaticSection, ValidatedAttribute
from redmine import Redmine
import re

rm = Redmine("");

class redmineSection(StaticSection):
    url = ValidatedAttribute('url')
    apikey = ValidatedAttribute('apikey')

def setup(bot):
    bot.config.define_section("redmine", redmineSection)
    rm.key = bot.config.redmine.apikey
    rm.url = bot.config.redmine.url

@module.rule(r".*#\d+")
def bug_subject(bot, trigger):
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
