import discord
import sys
import os
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')

applicants = {}

@bot.event
async def on_member_join(member):
    await member.send("""
Silverblade is a World of Warcraft mythic raiding guild, formed in 2016 after a number of casual but dedicated players wanted to spend a few nights per week raiding together. We've been steadily growing our list of cutting edge achievements from Xavius in Emerald Nightmare, to Argus in Antorus, G'huun in Uldir and Jaina Proudmore in Battle of Dazar'alor.

We're currently progressing Azshara's Eternal Palace and have killed 7/8 bosses on mythic difficulty.

We raid every Sunday and Thursday from 20:30 game time and about 3-3½ hours. There are regular mythic+ runs, rated battleground events and casual heroic raids after the initial progression run.

If raiding with us is something you're interested in, hit the apply button and tell us why! We're always happy to read through applications! You can also contact any one of us in-game, and we'll make sure your request is directed to the right people so we can meet!

Please take a look at the !rules before applying""")

    await member.send("""
** **
If you are looking to make an application, please type `!application` and our friendly bot will send you everything you need to know.

If you are a friend of the guild, just ask your friend to type `!friend @you` in one of the channels they have access to.
""")


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def application(ctx):
    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("I'll send you the details now, please check your private messages!")

    await ctx.author.send("""\
*Thanks for your interest in applying!*

We're going to need some information from you, but make sure you've read the **!rules** first.

Once you've read the rules, please enter each of the commands below, providing links to your character information web pages:

**Please send each command below as a separate direct message to the bot.**

For example, `!armory https://worldofwarcraft.com/en-gb/character/eu/frostmane/christopher`

```
!armory      <Type the link to your armory profile>
!raiderio    <Type the link to your raider.io profile>
!logs        <Type the link to your best logs>
```

It would be great if you could also tell us a bit more about you by filling in the required information.
```
!why         <Type why do you want to join? What makes us the guild for you? What do you expect from us?>
!xp          <Type what raiding experience you have so far?>
```

Once you've provided all of this tell me you're `!done`, I'll have someone from our recruitment team get back to you really soon! :-)
""")


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
        await ctx.author.send("""Thank you for providing your armory information!""")


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def raiderio(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!raiderio <the link to your raiderio profile here or N/A>`.")
            return
        
        applicant(applicants, ctx.author)["raiderio"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send("""Thank you for providing your RaiderIO information!""")


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def logs(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!logs <the link to your logs here or N/A>`")
            return
        
        applicant(applicants, ctx.author)["logs"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send("""Thank you for providing your logs.""")


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def why(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!why <the reason you want to join>`")
            return
        
        applicant(applicants, ctx.author)["why"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send("""Thank you for telling us why you want to join.""")


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def xp(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(ctx.message.content.strip().split(" ")) <= 1:
            await ctx.author.send("You need to type `!xp <your raiding history/experience here>`")
            return
        
        applicant(applicants, ctx.author)["xp"] = ctx.message.content.split(None, 1)[1]
        await ctx.author.send("""Thank you for telling us your experience/history. If you've provided everything then you can type `!done` to submit your application.""")


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

        guild = bot.get_guild(238705194244898817)
        role = discord.utils.get(guild.roles, name='Applicant')
        await guild.get_member(ctx.author.id).add_roles(role)
        
        applicant_map["done"] = datetime.now().strftime("%D")

        await ctx.author.send("""Great! I'll post your details in #applications, head over there to check the status""")
        channel = bot.get_channel(651719224275894272)
        await channel.send("""**Application** ({0})

**Name**: {1}
**Armory**: {2}
**RaiderIO**: {3}
**Logs**: {4}

**Why the applicant wants to join**
{5}

**Experience so far**
{6}

**Status**
Pending
** **
""".format(datetime.now().strftime("%D"), ctx.author, applicant(applicants, ctx.author)["armory"],
           applicant(applicants, ctx.author)["raiderio"], applicant(applicants, ctx.author)["logs"],
           applicant(applicants, ctx.author)["why"], applicant(applicants, ctx.author)["xp"]))


@bot.command(pass_context=True)
@commands.has_any_role('Hand', 'Crusader', 'Sentinel', 'High Hand', 'Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def friend(ctx):
    role = discord.utils.get(bot.get_guild(238705194244898817).roles, name='Friend')
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
    role = discord.utils.get(bot.get_guild(238705194244898817).roles, name='Initiate')
    member = ctx.message.mentions[0]
    channel = bot.get_channel(651719224275894272)
    
    member = ctx.message.mentions[0]
    await ctx.send("Alright, I'll accept {0} and make them an initiate =)".format(member))

    await member.add_roles(role)
    await channel.send("""**Application** ({0})

    **Name**: {1}

    **Status**
    Accepted
    
    **Information**
    We've assigned you the 'Initiate' role which you'll have for 4 weeks so that both you and the guild can see if we're a good fit together.
    
    You can type `!roles` to understand more about the roles in the guild.
    
    ** **
    """.format(datetime.now().strftime("%D"), member))

@bot.command(pass_context=True)
@commands.has_any_role('Councillor')
@commands.cooldown(2, 5, commands.BucketType.user)
async def reject(ctx):
    role = discord.utils.get(bot.get_guild(238705194244898817).roles, name='Applicant')
    member = ctx.message.mentions[0]
    await ctx.send("Alright, I'll decline {0} and remove their applicant role =(".format(member))
    
    reason = "Please check back in the future and we will happily review again."
    if len(ctx.message.content.strip().split(" ")) >= 3:
        reason = ctx.message.content.split(None, 2)[2]

    await member.remove_roles(role)
    await member.send("""Hey {0},

Unfortunately we're not going to be progressing forward with your application to join Silverblade at this time.

{1}

Kind Regards,

-Silverblade Council 
    ** **
    """.format(member, reason))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def rules(ctx):
    await ctx.author.send("""
Our rules can be navigated with a menu based system. Our rules can be navigated with a menu based system. Simply type the `!command` you want to view into this message chain.

```
!ranks       - Types of ranks in the guild.
!times       - When Silverblade raids.
!prep        - Being prepared for raiding.
!addons      - We have a set of mandatory addons
!application - Becoming a raider is application based.
!alts        - We welcome alts in Silverblade.
!friend      - We allow our guild members to invite friends.
```
""")


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
    await ctx.send("""
There are a few ground rules you must follow in Silverblade depending on your rank.

**Ranks**

```
 Councillor  - Guild leader and Officer rank.leading.
 High Hand   - A non-raiding officer.
 Crusader    - The main raiding rank.
 Avatar      - The alts of Crusaders.
 Initiate    - People who are in the process of becoming a Crusader.
 Sentinel    - Support rank for people who cannot meet our schedule.
 Hand        - The main social rank
```
**Being a social**

Socials of all stripes are very welcome. They're the friends of other socials and raiders. They're here for the social aspect and the community. There are no demands to their skill. There are a few rules on general behaviour in the guild and falling afoul of those will get you removed. See the bottom of the post for details.

**Becoming a Raider**

In order to become a raider, you should submit an application through this site. Alternatively, contact one of the officers in-game, and we can arrange a meeting.

The standard trial process lasts 2 weeks (total of 4 raids). During this time, we want you to demonstrate that you can learn the fights, play your character, and otherwise adhere to all the other rules that apply to raiders. It may extend, however, if uncertainty arises, but usually it won't.
In other words: As a Trial/Initiate consider yourself a raider, but without the perks. After 2 weeks, you'll be promoted assuming you pass and the perks will be yours.

If, in the unlikely event you, or the raid team decide staying as a raider isn't appropriate, we'll offer you a social rank :-)
""")


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def alts(ctx):
    await ctx.send("""
We expect you to turn up to raids with you main character in your main spec by default. In some cases, such as when a boss calls for a specific comp, we may discuss asking you to go off-spec or even to an alt.

While it is not required to roll offspecs or alts and getting them ready for raiding, doing so will result in a lot of appreciation, higher priority when it becomes time to hand out off-spec items (which may also help outside the raid), and of course personal loot upgrades will go to an alt.

We will not invite your alt just because you feel like playing it on that particular day. You must provide a good reason why it will make it easier to defeat the boss using the alt.

This is primarily because of forced personal loot, because we don't want items spreading across many characters being played by one person. We prefer more loot to go to one character for improved output, leading to improved progress.
""")


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def prep(ctx):
    await ctx.send("""
We expect you to have read the strategies posted on Discord before the raid. Be ready to deal with any special assignment you may get as a result of your role on the given fight.

Maintain your knowledge of the game and your spec especially. This means a combination of continuous play and practice in various modes of play (M+, lower difficulty raids, PvP, etc.), and using class resources and guides, such as the Discord for your class or continuously updated guides found across the web.

We do not merely expect you to use one of these tools, but to use several in combination to form a strong understand of the class and spec you play.

Furthermore, we expect you to be continuously simming your character with Simcraft, Ask Mr. Robot, or a similar tool in order to always know whether or not a particular item is an upgrade.

Upgrade your gear by participating in WoW's many activities outside raiding to upgrade your gear. Frequently the guild will set particular demands on how prepared you must be to enter a raid with the team. Make sure you are familiar with and meet those goals.
""")

    await ctx.send("""
** **
**Preparation**

Have all types of consumables ready for every fight BEFORE joining the raid.

That means:
- Food, the best type and with the correct stat. Food is used on every pull besides literally the first few "We have no idea what we're doing and wil lwipe to that" pulls.
- Flask, of the best type. Flasks are always expected.
- Potions - 2x per attempted pull

Vantus runes may be provided when needed. If feast is the best type of food at the time, feasts may also be provided, but you should still have food so we don't have to pop an entire table for one guy.
""")


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def addons(ctx):
    await ctx.send("""
These add-ons are mandatory:

1. Deadly Boss Mods OR BigWigs
2. RCLootCouncil
3. Exorsus Raid Tools - Enable Note in /ert -> Note.
4. WeakAuras

Please keep them updated!
""")


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def times(ctx):
    await ctx.send("""
Our raid days are **Thursday** 20:30-23:30 and **Sunday** 20:30-23:30 server time every week. Occasionally the raid time may extend for a few more pulls if we feel we're close to a kill, but never past midnight.   

We expect our raiders to be able to attend both days unless signing the calendar to decline on occasional circumstances.

**Important**

Try to be online 15 minutes before raid. Be on no later than the start and be ready to accept summon immediately.

*Sign up on guild calendar!*

- If you can come and will be there on time.
- If you can come but will be late. Write in the Discord #absences channel
- If you cannot come at all. Write in the Discord #absences channel
""")


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def about(ctx):
    await ctx.send("""
Silverblade is a World of Warcraft **mythic** raiding guild, formed in 2016 after a number of casual but dedicated players wanted to spend a few nights per week raiding together. We've been steadily growing our list of cutting edge achievements from Xavius in Emerald Nightmare, to Argus in Antorus, G'huun in Uldir and Jaina Proudmore in Battle of Dazar'alor.

We're currently progressing Azshara's Eternal Palace and have killed 7/8 bosses on mythic difficulty.

We raid every **Sunday** and **Thursday** from **20:30** game time and about 3-3½ hours. There are regular mythic+ runs, rated battleground events and casual heroic raids after the initial progression run.

If raiding with us is something you're interested in, hit the apply button and tell us why! We're always happy to read through applications! You can also contact any one of us in-game, and we'll make sure your request is directed to the right people so we can meet!

Please take a look at the `!rules` before applying
""")


bot.run(os.getenv('DISCORD_TOKEN'))
