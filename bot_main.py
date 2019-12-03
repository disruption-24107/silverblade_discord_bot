import discord
import sys
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
@commands.guild_only()
async def application(ctx):
    await ctx.send("I'll send you the details now, please check your private messages!")
    await ctx.author.send("""\
*Thanks for your interest in applying!*

We're going to need some information from you, but make sure you've read the **!rules** first. 

Once you've read the rules, please provide us with the following:
```
!armory      The link to your armory profile (repeatable for each alt if you have alts)
!raider.io   The link to your raider.io profile
!logs        A link to your best logs
```
It would be great if you could also tell us:
```
!why         Why do you want to join?
!xp          What experience you have so far?
```
  
Once you've provided all of this, I'll have someone from our recruitment team get back to you really soon! :-)

""")

@bot.command(pass_context=True)
@commands.has_any_role('Hand', 'Crusader', 'Sentinel', 'High Hand', 'Councillor')
async def friend(ctx):
    try:
        role = discord.utils.get(bot.get_guild(238705194244898817).roles, name='Friend')
        member = ctx.message.mentions[0]

        if role in member.roles:
            await ctx.send("That person is already a friend of mine!")
        else:
            await member.add_roles(role)
            await ctx.send("A friend of yours is a friend of mine!")
    except:
        await ctx.send("I couldn't do that right now, sorry!")

@bot.command(pass_context=True)
@commands.cooldown(1, 180, commands.BucketType.user)
async def rules(ctx):
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
""")

    await ctx.send("""
** **
**Being a social**

Socials of all stripes are very welcome. They're the friends of other socials and raiders. They're here for the social aspect and the community. There are no demands to their skill. There are a few rules on general behaviour in the guild and falling afoul of those will get you removed. See the bottom of the post for details.

**Becoming a Raider**

In order to become a raider, you should submit an application through this site. Alternatively, contact one of the officers in-game, and we can arrange a meeting.

The standard trial process lasts 2 weeks (total of 4 raids). During this time, we want you to demonstrate that you can learn the fights, play your character, and otherwise adhere to all the other rules that apply to raiders. It may extend, however, if uncertainty arises, but usually it won't.
In other words: As a Trial/Initiate consider yourself a raider, but without the perks. After 2 weeks, you'll be promoted assuming you pass and the perks will be yours.

Failing the trial process gets you demoted to Social.""")

    await ctx.send("""
** **
**Knowledge**

We expect you to have read the strategies posted on Discord before the raid. Be ready to deal with any special assignment you may get as a result of your role on the given fight.

Maintain your knowledge of the game and your spec especially. This means a combination of continuous play and practice in various modes of play (M+, lower difficulty raids, PvP, etc.), and using class resources and guides, such as the Discord for your class or continuously updated guides found across the web.

We do not merely expect you to use one of these tools, but to use several in combination to form a strong understand of the class and spec you play.

Furthermore, we expect you to be continuously simming your character with Simcraft, Ask Mr. Robot, or a similar tool in order to always know whether or not a particular item is an upgrade.

Upgrade your gear by participating in WoW's many activities outside raiding to upgrade your gear. Frequently the guild will set particular demands on how prepared you must be to enter a raid with the team. Make sure you are familiar with and meet those goals.
""")

    await ctx.send("""
** **
**Alts**

We expect you to turn up to raids with you main character in your main spec by default. In some cases, such as when a boss calls for a specific comp, we may discuss asking you to go off-spec or even to an alt.

While it is not required to roll offspecs or alts and getting them ready for raiding, doing so will result in a lot of appreciation, higher priority when it becomes time to hand out off-spec items (which may also help outside the raid), and of course personal loot upgrades will go to an alt.

We will not invite your alt just because you feel like playing it on that particular day. You must provide a good reason why it will make it easier to defeat the boss using the alt.

This is primarily because of forced personal loot, because we don't want items spreading across many characters being played by one person. We prefer more loot to go to one character for improved output, leading to improved progress.
""")


@bot.command(pass_context=True)
async def about(ctx):
    await ctx.send("""
Silverblade is a World of Warcraft **mythic** raiding guild, formed in 2016 after a number of casual but dedicated players wanted to spend a few nights per week raiding together. We've been steadily growing our list of cutting edge achievements from Xavius in Emerald Nightmare, to Argus in Antorus, G'huun in Uldir and Jaina Proudmore in Battle of Dazar'alor.

We're currently progressing Azshara's Eternal Palace and have killed 7/8 bosses on mythic difficulty.

We raid every **Sunday** and **Thursday** from **20:30** game time and about 3-3½ hours. There are regular mythic+ runs, rated battleground events and casual heroic raids after the initial progression run.

If raiding with us is something you're interested in, hit the apply button and tell us why! We're always happy to read through applications! You can also contact any one of us in-game, and we'll make sure your request is directed to the right people so we can meet!

Please take a look at the `!rules` before applying
""")

bot.run(sys.argv[1])
