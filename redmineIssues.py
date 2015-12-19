from sopel import module, config, trigger, db
from sopel.db import SopelDB
from redmine import Redmine
from redmine.resources import Version, Project, Issue
import re

def setup(bot):
    bot.rmdb = SopelDB(bot.config)
    bot.rm = Redmine("")

@module.rule(r".*#\d+")
def bug_subject(bot, trigger):
    bot.rm.key = bot.rmdb.get_channel_value(trigger.sender,"apikey")
    bot.rm.url = bot.rmdb.get_channel_value(trigger.sender,"url")
    matches = re.findall(r"#(\d+)",trigger.group(0))
    for match in matches:
        try:
            issue = bot.rm.issue.get(int(match))
        except Exception as ex:
            bot.say(ex)
        else:
            bot.say(issue.subject)
            bot.say(bot.rm.url + "issues/" + match)

@module.commands(r"seturl")
def set_url(bot, trigger):
    if trigger.owner is True:
        bot.rmdb.set_channel_value(trigger.group(3),"url",trigger.group(4))
        bot.reply("Redmine URL for channel " + trigger.group(3) + " set to " + trigger.group(4))

@module.commands(r"setapikey")
def set_api_key(bot, trigger):
    if trigger.owner is True:
        bot.rmdb.set_channel_value(trigger.group(3),"apikey",trigger.group(4))
        bot.reply("Redmine key for channel " + trigger.group(3) + " set to " + trigger.group(4))

@module.commands(r"setProject")
def set_project(bot,trigger):
    if trigger.owner is True:
        bot.rmdb.set_channel_value(trigger.group(3),"project",trigger.group(4))
        bot.reply("Redmine key for channel " + trigger.group(3) + " set to " + trigger.group(4))

@module.commands(r"build")
def get_build(bot, trigger):
    bot.rm.key = bot.rmdb.get_channel_value(trigger.sender,"apikey")
    bot.rm.url = bot.rmdb.get_channel_value(trigger.sender,"url")
    project = bot.rm.project.get(bot.rmdb.get_channel_value(trigger.sender,"project"))
    bot.reply(project.versions[len(project.versions)-3])

@module.interval(20)
def check_new_build(bot):
    for channel in bot.channels:
        bot.rm.key = bot.rmdb.get_channel_value(channel,"apikey")
        bot.rm.url = bot.rmdb.get_channel_value(channel,"url")
        try:
            project = bot.rm.project.get(bot.rmdb.get_channel_value(channel,"project"))
        except:
            project = None
        if project is not None:
            latestBuild = project.versions[len(project.versions)-3]
            lastBuild = bot.rmdb.get_channel_value(channel,"lastbuild")
            if lastBuild.__str__() != latestBuild.__str__():
                bot.notice("A new build has been triggered! New Build is " + latestBuild.__str__(),channel)
                bot.rmdb.set_channel_value(channel,"lastbuild",latestBuild.__str__())
