from sopel import module, config, trigger, db
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.db import SopelDB
from redmine import Redmine
import re

class redmineIssues():
    rmdb = SopelDB
    rm = Redmine("")

def setup(bot):
    redmineIssues.rmdb = SopelDB(bot.config)

@module.rule(r".*#\d+")
def bug_subject(bot, trigger):
    redmineIssues.rm.key = redmineIssues.rmdb.get_channel_value(trigger.sender,"apikey")
    redmineIssues.rm.url = redmineIssues.rmdb.get_channel_value(trigger.sender,"url")
    matches = re.findall(r"#(\d+)",trigger.group(0))
    for match in matches:
        try:
            issue = redmineIssues.rm.issue.get(int(match))
        except Exception as ex:
            bot.say(ex)
        else:
            bot.say(issue.subject)
            bot.say(rm.url + "/issues/" + match)

@module.commands(r"seturl")
def set_url(bot, trigger):
    if trigger.owner is True:
        redmineIssues.rmdb.set_channel_value(trigger.group(3),"url",trigger.group(4))
        bot.reply("Redmine URL for channel " + trigger.group(3) + " set to " + trigger.group(4))

@module.commands(r"setapikey")
def set_api_key(bot, trigger):
    if trigger.owner is True:
        redmineIssues.rmdb.set_channel_value(trigger.group(3),"apikey",trigger.group(4))
        bot.reply("Redmine key for channel " + trigger.group(3) + " set to " + trigger.group(4))
