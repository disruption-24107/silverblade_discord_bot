import discord
import os

from discord.ext import commands
from datetime import datetime
from bot_text_resources import *


class GuildRoles:
    ROLE_FRIEND = "Friend"
    ROLE_INITIATE = "Initiate"
    ROLE_APPLICANT = "Applicant"


APPLICATIONS_CHANNEL = 651719224275894272
GUILD = 238705194244898817

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')

applicants = {}


@bot.event
async def on_member_join(member):
    await member.send(ON_MEMBER_JOIN_1)
    await member.send(ON_MEMBER_JOIN_2)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def application(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(APPLICATION_PUBLIC)
        
    await ctx.author.send(APPLICATION)


def applicant(applicant_map, member):
    if member not in applicant_map:
        applicant_map[member] = {}
        
    return applicant_map[member]


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def armory(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send(APPLICATION_NOT_ENOUGH_ARMORY_INFO)
            return
        
        applicant(applicants, ctx.author)["armory"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_ARMORY)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def raiderio(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send(APPLICATION_NOT_ENOUGH_RAIDERIO_INFO)
            return
        
        applicant(applicants, ctx.author)["raiderio"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_RAIDERIO)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def logs(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send(APPLICATION_NOT_ENOUGH_LOGS_INFO)
            return
        
        applicant(applicants, ctx.author)["logs"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_LOGS)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def why(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send(APPLICATION_NOT_ENOUGH_WHY_INFO)
            return
        
        applicant(applicants, ctx.author)["why"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_WHY)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def xp(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send(APPLICATION_NOT_ENOUGH_XP_INFO)
            return
        
        applicant(applicants, ctx.author)["xp"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_XP)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def done(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        applicant_map = applicant(applicants, ctx.author)

        if "done" in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_ALREADY)
            return

        if "armory" not in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_MISSING_ARMORY)
            return

        if "raiderio" not in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_MISSING_RAIDERIO)
            return

        if "logs" not in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_MISSING_LOGS)
            return

        if "why" not in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_MISSING_WHY)
            return

        if "xp" not in applicant_map:
            await ctx.author.send(APPLICATION_SUBMIT_MISSING_XP)
            return

        guild = bot.get_guild(GUILD)
        role = discord.utils.get(guild.roles, name=GuildRoles.ROLE_APPLICANT)
        await guild.get_member(ctx.author.id).add_roles(role)
        
        applicant_map["done"] = datetime.now().strftime("%D")

        await ctx.author.send(APPLICATION_SUBMITTED)
        channel = bot.get_channel(APPLICATIONS_CHANNEL)
        await channel.send(APPLICATION_ACCEPTED.format(datetime.now().strftime("%D"), ctx.author, applicant(applicants, ctx.author)["armory"], applicant(applicants, ctx.author)["raiderio"], applicant(applicants, ctx.author)["logs"], applicant(applicants, ctx.author)["why"], applicant(applicants, ctx.author)["xp"]))


@bot.command(pass_context=True)
@commands.has_any_role('Hand', 'Crusader', 'Sentinel', 'High Hand', 'Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def friend(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name=GuildRoles.ROLE_FRIEND)
    member = ctx.message.mentions[0]

    if role in member.roles:
        await ctx.send(FRIEND_ROLE_ALREAD_ASSIGNED)
    else:
        await member.add_roles(role)
        await ctx.send(FRIEND_ROLE_ASSIGNED)


@bot.command(pass_context=True)
@commands.has_any_role('Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def accept(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name=GuildRoles.ROLE_INITIATE)
    member = ctx.message.mentions[0]
    channel = bot.get_channel(APPLICATIONS_CHANNEL)
    await ctx.send(APPLICATION_ACCEPTED_RESPONSE.format(member))
    await member.add_roles(role)
    await channel.send(APPLICATION_ACCEPTED.format(datetime.now().strftime("%D"), member.mention()))


@bot.command(pass_context=True)
@commands.has_any_role('Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def reject(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name=GuildRoles.ROLE_APPLICANT)
    member = ctx.message.mentions[0]
    
    if role not in member.roles:
        await ctx.send(APPLICATION_REJECTED_NOT_APPLICANT.format(member))
        return

    reason = APPLICATION_DEFAULT_REJECTION_REASON
    if len(ctx.message.content.strip().split(" ")) >= 3:
        reason = ctx.message.content.split(None, 2)[2]
        
    await ctx.send(APPLICATION_REJECTED_RESPONSE.format(member))
    await member.remove_roles(role)
    await member.send(APPLICATION_REJECTED.format(member, reason))


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def rules(ctx):
    await ctx.author.send(RULES)


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def menu(ctx):
    await rules.invoke(ctx)


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    await rules.invoke(ctx)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def ranks(ctx):
    await ctx.send(RANKS)


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def roles(ctx):
    await ranks.invoke(ctx)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def alts(ctx):
    await ctx.send(ALTS)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def prep(ctx):
    await ctx.send(PREPARATION_1)
    await ctx.send(PREPARATION_2)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def addons(ctx):
    await ctx.send(ADDONS)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def times(ctx):
    await ctx.send(TIMES)


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def about(ctx):
    await ctx.send(ABOUT)


bot.run(os.getenv('DISCORD_TOKEN'))
