import discord
import os
from discord.ext import commands
from datetime import datetime
from pathlib import Path

ADDONS_TEXT = Path("resources/addons.txt").read_text()
ABOUT_TEXT = Path("resources/about.txt").read_text()
RULES_TEXT = Path("resources/rules.txt").read_text()
RANKS_TEXT = Path("resources/ranks.txt").read_text()
TIMES_TEXT = Path("resources/times.txt").read_text()
APPLICATION_TEXT = Path("resources/application.txt").read_text()
APPLICATION_PUBLIC_TEXT = Path("resources/application_public.txt").read_text()
APPLICATION_ACCEPTED_TEXT = Path("resources/application_accepted.txt").read_text()
APPLICATION_REJECTED_TEXT = Path("resources/application_rejected.txt").read_text()
APPLICATION_DEFAULT_REJECTION_REASON_TEXT = Path("resources/application_default_rejection_reason.txt").read_text()
APPLICATION_PROVIDED_XP_TEXT = Path("resources/application_provided_xp.txt").read_text()
APPLICATION_PROVIDED_WHY_TEXT = Path("resources/application_provided_why.txt").read_text()
APPLICATION_PROVIDED_LOGS_TEXT = Path("resources/application_provided_logs.txt").read_text()
APPLICATION_PROVIDED_ARMORY_TEXT = Path("resources/application_provided_armory.txt").read_text()
APPLICATION_PROVIDED_RAIDERIO_TEXT = Path("resources/application_provided_raiderio.txt").read_text()
ALTS_TEXT = Path("resources/alts.txt").read_text()
PREPARATION_1_TEXT = Path("resources/preparation.1.txt").read_text()
PREPARATION_2_TEXT = Path("resources/preparation.2.txt").read_text()
ON_MEMBER_JOIN_1_TEXT = Path("resources/on_member_join.1.txt").read_text()
ON_MEMBER_JOIN_2_TEXT = Path("resources/on_member_join.2.txt").read_text()

APPLICATIONS_CHANNEL = 651719224275894272
GUILD = 238705194244898817

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')

applicants = {}

@bot.event
async def on_member_join(member):
    await member.send(ON_MEMBER_JOIN_1_TEXT)
    await member.send(ON_MEMBER_JOIN_2_TEXT)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def application(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(APPLICATION_PUBLIC_TEXT)
        
    await ctx.author.send(APPLICATION_TEXT)

def applicant(applicant_map, member):
    if member not in applicant_map:
        applicant_map[member] = {}
        
    return applicant_map[member]

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def armory(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!armory <the link to your armory profile here>`")
            return
        
        applicant(applicants, ctx.author)["armory"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_ARMORY_TEXT)

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def raiderio(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!raiderio <the link to your raiderio profile here or N/A>`.")
            return
        
        applicant(applicants, ctx.author)["raiderio"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_RAIDERIO_TEXT)

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def logs(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!logs <the link to your logs here or N/A>`")
            return
        
        applicant(applicants, ctx.author)["logs"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_LOGS_TEXT)

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def why(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!why <the reason you want to join>`")
            return
        
        applicant(applicants, ctx.author)["why"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_WHY_TEXT)

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def xp(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!xp <your raiding history/experience here>`")
            return
        
        applicant(applicants, ctx.author)["xp"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send(APPLICATION_PROVIDED_XP_TEXT)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def done(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        applicant_map = applicant(applicants, ctx.author)

        if "done" in applicant_map:
            await ctx.author.send("""You've already applied, check #applications to see your full application.""")
            return

        if "armory" not in applicant_map:
            await ctx.author.send("""You're missing the armory link (use `!armory <URL>` here to provide it). If you don't want to provide this, just say N/A""")
            return

        if "raiderio" not in applicant_map:
            await ctx.author.send("""You're missing your RaiderIO information (use `!raiderio <URL>` here to provide it). If you don't want to provide this, just say N/A""")
            return

        if "logs" not in applicant_map:
            await ctx.author.send("""You're missing your logs (use `!logs <URL>` here to provide it). If you don't want to provide this, just say N/A""")
            return

        if "why" not in applicant_map:
            await ctx.author.send("""You haven't told us why you want to join (use `!why <reason>` here to provide it). If you don't want to provide this, just say N/A""")
            return

        if "xp" not in applicant_map:
            await ctx.author.send("""You haven't told us about your raiding history (use `!xp <history>` here to provide it). If you don't want to provide this, just say N/A""")
            return

        guild = bot.get_guild(GUILD)
        role = discord.utils.get(guild.roles, name='Applicant')
        await guild.get_member(ctx.author.id).add_roles(role)
        
        applicant_map["done"] = datetime.now().strftime("%D")

        await ctx.author.send("""Great! I'll post your details in #applications, head over there to check the status""")
        channel = bot.get_channel(APPLICATIONS_CHANNEL)
        await channel.send(APPLICATION_ACCEPTED_TEXT.format(datetime.now().strftime("%D"), ctx.author, applicant(applicants, ctx.author)["armory"], applicant(applicants, ctx.author)["raiderio"], applicant(applicants, ctx.author)["logs"], applicant(applicants, ctx.author)["why"], applicant(applicants, ctx.author)["xp"]))


@bot.command(pass_context=True)
@commands.has_any_role('Hand', 'Crusader', 'Sentinel', 'High Hand', 'Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def friend(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name='Friend')
    member = ctx.message.mentions[0]

    if role in member.roles:
        await ctx.send("That person is already a friend of mine!")
    else:
        await member.add_roles(role)
        await ctx.send("A friend of yours is a friend of mine!")

@bot.command(pass_context=True)
@commands.has_any_role('Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def accept(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name='Initiate')
    member = ctx.message.mentions[0]
    channel = bot.get_channel(APPLICATIONS_CHANNEL)
    await ctx.send("Alright, I'll accept {0} and make them an initiate =)".format(member))
    await member.add_roles(role)
    await channel.send(APPLICATION_ACCEPTED_TEXT.format(datetime.now().strftime("%D"), member.mention()))

@bot.command(pass_context=True)
@commands.has_any_role('Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def reject(ctx):
    role = discord.utils.get(bot.get_guild(GUILD).roles, name='Applicant')
    member = ctx.message.mentions[0]
    
    if role not in member.roles:
        await ctx.send("Uh oh, {0} isn't an applicant.".format(member))
        return

    reason = APPLICATION_DEFAULT_REJECTION_REASON_TEXT
    if len(ctx.message.content.strip().split(" ")) >= 3:
        reason = ctx.message.content.split(None, 2)[2]
        
    await ctx.send("Alright, I'll decline {0} and remove their applicant role =(".format(member))
    await member.remove_roles(role)
    await member.send(APPLICATION_REJECTED_TEXT.format(member, reason))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def rules(ctx):
    await ctx.author.send(RULES_TEXT)
    
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
    await ctx.send(RANKS_TEXT)

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def roles(ctx):
    await ranks.invoke(ctx)

@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def alts(ctx):
    await ctx.send(ALTS_TEXT)

@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def prep(ctx):
    await ctx.send(PREPARATION_1_TEXT)
    await ctx.send(PREPARATION_2_TEXT)

@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def addons(ctx):
    await ctx.send(ADDONS_TEXT)

@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def times(ctx):
    await ctx.send(TIMES_TEXT)

@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def about(ctx):
    await ctx.send(ABOUT_TEXT)

bot.run(os.getenv('DISCORD_TOKEN'))
