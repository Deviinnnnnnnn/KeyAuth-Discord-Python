import discord, os, Devin

from discord.ext import tasks, commands

Config = "Settings.json"

Token = Devin.Load(Config, "Token")
Prefix = Devin.Load(Config, "Prefix")
Name = Devin.Load(Config, "Name")
GeneratorKeysChannel = Devin.Load(Config, "AdminChannel")
GenerateKeysRole = Devin.Load(Config, "AdminRole")
LogChannel = Devin.Load(Config, "LogChannel")

ErrorColor = 0xff0000
SuccessColor = 0x00ff2a

client = discord.Client()

client = commands.Bot(command_prefix=Prefix, case_insensitive=True)

client.remove_command('help')

os.system('cls')

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def GenKey(ctx, days, amt):
    if ctx.channel.id == GeneratorKeysChannel:
        await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Generated Keys!**\n**Days -> `{days}`**\n**Amount -> `{amt}`**", f"{Name} Logs")
        if int(amt) > 1:
            Keys = Devin.GenerateLicenses(days, amt)
            embed = discord.Embed(color=SuccessColor)
            embed.set_author(name='Successful!')
            embed.add_field(name=f'Successfully Generated Licenses', value=f'\n**Days --> `{days}`\nAmount --> `{amt}`**', inline=False)
            for k in range(len(Keys)):
                embed.add_field(name=f'‎', value=f'**`{Keys[k]}`**', inline=False)
            await ctx.send(embed=embed)
        elif int(amt) == 1:
            Key = Devin.GenerateLicense(days)
            embed = discord.Embed(color=SuccessColor)
            embed.set_author(name='Successful!')
            embed.add_field(name=f'Successfully Generated License', value=f'\n**Days --> `{days}`\nAmount --> `1`**', inline=False)
            embed.add_field(name=f'‎', value=f'**`{Key}`**', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=ErrorColor)
            embed.set_author(name='Error!')
            embed.add_field(name=f'Information', value=f'**Please Specify Days And Amount!**\n\n**Example -> `{Prefix}genlicense [Days] [Amount]`**', inline=False)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Information', value=f'**Please Execute This Command In A Different Channel!**', inline=False)
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def deleteuser(ctx, userid):
    await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Deleted User! -> `{userid}`**", f"{Name} Logs")
    if Devin.DeleteUser(userid):
        embed = discord.Embed(color=SuccessColor)
        embed.set_author(name='Successful!')
        embed.add_field(name=f'Successfully Deleted User', value=f'‎', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Errori Deleting User', value=f'‎', inline=False)
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def extend(ctx, userid, days):
    if Devin.ExtendUser(userid, days):
        await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Extended User -> `{userid}` | Days -> `{days}`**", f"{Name} Logs")
        embed = discord.Embed(color=SuccessColor)
        embed.set_author(name='Successful!')
        embed.add_field(name=f'Successfully Extended User', value=f'‎', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Error Extending User', value=f'‎', inline=False)
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def keys(ctx):
    if ctx.channel.id == GeneratorKeysChannel:
            await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Fetched Keys!**", f"{Name} Logs")
            Keys = Devin.GetActiveLicenses()
            if len(Keys) > 0:
                embed = discord.Embed(color=SuccessColor)
                embed.set_author(name='Successful!')
                embed.add_field(name=f'Successfully Fetched Licenses', value=f'‎', inline=False)
                for k in range(len(Keys)):
                    try:
                        embed.add_field(name=f'‎', value=Keys[k], inline=False)
                    except:
                        break
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=SuccessColor)
                embed.set_author(name='Successful!')
                embed.add_field(name=f'Successfully Fetched Licenses', value=f'‎', inline=False)
                embed.add_field(name=f'‎', value=f'**No Active Licenses!**', inline=False)
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'‎', value=f'**Please Execute This Command In A Different Channel!**', inline=False)
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def deleteallkeys(ctx):
    if ctx.channel.id == GeneratorKeysChannel:
            await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Deleted All Keys!**", f"{Name} Logs")
            if Devin.DeleteAllLicenses():
                embed = discord.Embed(color=SuccessColor)
                embed.set_author(name='Successful!')
                embed.add_field(name=f'Successfully Deleted All Licenses', value=f'‎', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=ErrorColor)
                embed.set_author(name='Error!')
                embed.add_field(name=f'Error Deleting All Licenses', value=f'‎', inline=False)
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Information', value=f'**Please Execute This Command In A Different Channel!**', inline=False)
        await ctx.send(embed=embed)

@client.command()
@commands.has_any_role(GenerateKeysRole) 
async def deletekey(ctx, key):
    if ctx.channel.id == GeneratorKeysChannel:
            await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Deleted A Key -> `{key}`**", f"{Name} Logs")
            if Devin.DeleteLicense(key):
                embed = discord.Embed(color=SuccessColor)
                embed.set_author(name='Successful!')
                embed.add_field(name=f'Successfully Deleted Key!', value=f'‎', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=ErrorColor)
                embed.set_author(name='Error!')
                embed.add_field(name=f'Error Deleting Key!', value=f'‎', inline=False)
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Information', value=f'**Please Execute This Command In A Different Channel!**', inline=False)
        await ctx.send(embed=embed)

@client.command()
async def redeem(ctx,key = None):
    if key == None:
        embed = discord.Embed(color=ErrorColor)
        embed.set_author(name='Error!')
        embed.add_field(name=f'Missing License!', value=f'‎', inline=False)
        await ctx.send(embed=embed)
    else:
        if Devin.AddSubscription(ctx.author.id, key):
            await Devin.Log(client, LogChannel, f"{ctx.author.mention} **Redeemed A Key -> `{key}`**", f"{Name} Logs")
            embed = discord.Embed(color=SuccessColor)
            embed.set_author(name='Successfully Redeemed!')
            embed.add_field(name=f'‎', value=f'{ctx.author.mention} **You Have Redeemed A License!**', inline=False)
            await ctx.send(embed=embed)
        elif Devin.AddSubscription(ctx.author.id, key) == None:
            embed = discord.Embed(color=ErrorColor)
            embed.set_author(name='Error!')
            embed.add_field(name=f'You Already Have An Active Subscription!', value='‎', inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=ErrorColor)
            embed.set_author(name='Error')
            embed.add_field(name=f'You Have Redeemed An Invalid License!', value=f'‎', inline=False)
            await ctx.send(embed=embed)

@client.command()
async def auth(ctx):
    if Devin.VerifyUser(ctx.author.id):
        embed = discord.Embed(color=SuccessColor)
        embed.set_author(name='Successfully Authenticated User!')
        await ctx.send(embed=embed)
    else:
        embeda = discord.Embed(color=ErrorColor)
        embeda.set_author(name='Error!')
        embeda.add_field(name=f"You Don't Have An Active Subscription To Use This! ", value=f'‎', inline=False)
        await ctx.send(embed=embeda)

@client.command()
async def info(ctx):
    if Devin.VerifyUser(ctx.author.id):
        embed = discord.Embed(color=SuccessColor)
        embed.set_author(name='Plan Info!')
        embed.add_field(name=f'‎', value=f'{Devin.GetExpiry(ctx.author.id)}', inline=False)
        await ctx.send(embed=embed)
    else:
        embeda = discord.Embed(color=ErrorColor)
        embeda.set_author(name='Error!')
        embeda.add_field(name=f"You Don't Have An Active Subscription To Use This! ", value=f'‎', inline=False)
        await ctx.send(embed=embeda)

@client.command()
async def help(ctx):
    embed = discord.Embed(color=SuccessColor)
    embed.set_author(name=Name + ' Commands')
    embed.add_field(name=f'‎', value=f'** ----- Admin Commands ----- **\n\n   **`{Prefix}GenKey [Days] [Amount]`**\n\n   **`{Prefix}DeleteUser [UserID]`**   \n\n   **`{Prefix}DeleteKey [Key]`**   \n\n   **`{Prefix}Extend [UserID] [Days]`**\n\n   **`{Prefix}Keys`**\n\n    **`{Prefix}DeleteAllKeys`**\n\n** ----- Commands ----- **\n\n    **`{Prefix}Redeem [Key]`**\n\n**`{Prefix}Info`**\n\n**`{Prefix}Auth`**', inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit + 1)

@client.event
async def on_ready():
    Update.start()
    await Devin.Log(client, LogChannel, f"**Message -> `Bot Ready!`**", f"{Name} Logs")
    print(f'{client.user} Online')

@tasks.loop(seconds=60)
async def Update():
    Devin.DeleteExpiredUsers() # Wouldn't Recommend Messing With
 
def InitilazeBot():
    client.run(Token)

InitilazeBot()