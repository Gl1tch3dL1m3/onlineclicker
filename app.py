import discord
import aiomysql
import bcrypt
import datetime
from random import randint
from discord.ext import commands
from dotenv import load_dotenv
from asyncio import sleep
from os import getenv

# https://discord.gg/StJxMSc8kM

testing = False # don't mind this :p
players_column = "test_players" if testing else "players"
colors = (["Red", ":red_square:"], ["Orange", ":orange_square:"], ["Yellow", ":yellow_square:"], ["Green", ":green_square:"], ["Blue", ":blue_square:"], ["Purple", ":purple_square:"], ["Brown", ":brown_square:"])

load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())

# CHANGE THESE VARIABLES!!!
# -------------------------
modroles = [1514286817653030995, 1514286817653030994, 1514286817653030993] # admin, bots, support
verification_role = 1484121694573432956 if testing else 1514286817644515464
purgatory_channel = 1522839761423831081 if testing else 1522839147658608721
registered_role = 1517988134950932502 if testing else 1517967915868094494
server_id = 1224057238142849074 if testing else 1514286817636257862
# -------------------------

username_change_cooldowns = {}

db = {
        "host": getenv("DB_HOST"),
        "port": 3306,
        "user": getenv("DB_USER"),
        "password": getenv("DB_PASS"),
        "db": getenv("DB_NAME")
    }

async def execDB(sql, vars=None):
    selected = []

    async with pool.acquire() as con:
        async with con.cursor() as cur:
            if vars != "" and vars != None:
                await cur.execute(sql, vars)
            else:
                await cur.execute(sql)

            rows = await cur.fetchall()

            for row in rows:
                selected.append(list(row))

    return selected

def errorEmbed(author, description, title="Error!"):
    return discord.Embed(
        author=discord.EmbedAuthor(name=author.name, icon_url=author.avatar.url),
        title=title + " :x:",
        description=description,
        color=discord.Color.red()
    )

def successEmbed(author, description, title="Success!"):
    return discord.Embed(
        author=discord.EmbedAuthor(name=author.name, icon_url=author.avatar.url),
        title=title + " :white_check_mark:",
        description=description,
        color=discord.Color.green()
    )

def isModerator(member):
    if member.guild_permissions.administrator:
        return True
    else:
        for role in member.roles:
            if role.id in modroles:
                return True
            
        return False

def generate_hash(_str):
    salt = bcrypt.gensalt()
    hashed_str = bcrypt.hashpw(_str.encode("utf-8"), salt)
    return hashed_str

async def delete_user(discord_id):
    guild = bot.get_guild(server_id)
    member = guild.get_member(discord_id)
    role = guild.get_role(registered_role)

    await execDB(f"DELETE FROM {players_column} WHERE discord_id=%s", (discord_id, ))

    if role in member.roles:
        await member.remove_roles(role)

@bot.event
async def on_ready():
    global pool
    pool = await aiomysql.create_pool(
        **db,
        autocommit=True,
        connect_timeout=None
    )

    await bot.change_presence(activity=discord.Game("Cookie Clicker"))
    print(bot.user.name + " is ready!")

    # Refreshing connection between DB because I can't change database connection timeout...if you don't need this, remove it
    while True:
        await execDB("DO 0;")
        await sleep(10)

# Purgatory
@bot.event
async def on_message(message):
    if message.channel.id == purgatory_channel:
        try:
            await message.delete()
            await message.author.kick()
        except:
            pass

@bot.slash_command(description="Registers a new account.")
async def register(ctx, username: discord.Option(str, "The username you want to use", min_length=1, max_length=50), password: discord.Option(str, "The password you want to use to access your account (min. 8 characters)", min_length=8, max_length=50)): # type: ignore
    await ctx.defer(ephemeral=True)

    registered_for_this_discord_account = await execDB(f"SELECT username FROM {players_column} WHERE discord_id=%s", (ctx.user.id, ))
    is_already_registered = await execDB(f"SELECT username FROM {players_column} WHERE LOWER(username)=%s", (username.lower(), ))
    banned = await execDB("SELECT reason FROM bans WHERE discord_id=%s", (ctx.user.id, ))

    if not (ctx.user.get_role(verification_role) or isModerator(ctx.user)):
        await ctx.respond(embed=errorEmbed(ctx.user, "You can't create an account because you're unverified. To verify yourself, use the command `/verify`."), ephemeral=True)
    elif len(banned) != 0:
        await ctx.respond(embed=errorEmbed(ctx.user, f"You can't create an account because you're banned from using OnlineClicker. Reason: `{banned[0][0]}`"), ephemeral=True)
    elif len(registered_for_this_discord_account) != 0:
        await ctx.respond(embed=errorEmbed(ctx.user, "You can have a maximum of one OnlineClicker account. If you want to change something, use the command `/manage`."), ephemeral=True)
    elif len(is_already_registered) != 0:
        await ctx.respond(embed=errorEmbed(ctx.user, "An account with this username has already been registered. Please choose another one!"), ephemeral=True)
    elif not username.isalnum():
        await ctx.respond(embed=errorEmbed(ctx.user, "Your username must be alphanumeric (must contain only letters and numbers)."), ephemeral=True)
    else:
        pass_hash = generate_hash(password).decode("utf-8")

        await execDB(f"INSERT INTO {players_column} VALUES (%s, %s, %s, %s)", (ctx.user.id, username, pass_hash, randint(0, len(colors)-1)))

        role = ctx.guild.get_role(registered_role)
        await ctx.user.add_roles(role)
        await ctx.respond(embed=successEmbed(ctx.user, "Your account was successfully created!"), ephemeral=True)

@bot.slash_command(description="Manages your account.")
async def manage(ctx):
    registered_for_this_discord_account = await execDB(f"SELECT username FROM {players_column} WHERE discord_id=%s", (ctx.user.id, ))

    if not (ctx.user.get_role(verification_role) or isModerator(ctx.user)):
        await ctx.respond(embed=errorEmbed(ctx.user, "You can't manage an account because you're unverified. To verify yourself, use the command `/verify`."), ephemeral=True)
    elif len(registered_for_this_discord_account) == 0:
        await ctx.respond(embed=errorEmbed(ctx.user, "You haven't registered an OnlineClicker account. Use the command `/register` to make one!"), ephemeral=True)
    else:
        username = registered_for_this_discord_account[0][0]
        await ctx.user.add_roles(ctx.guild.get_role(registered_role))

        class ManageView(discord.ui.View):
            @discord.ui.button(
                label="Change Username",
                style=discord.ButtonStyle.gray,
                emoji=":pencil:"
            )

            async def change_username(self, button, interaction):
                if interaction.user.id != ctx.user.id:
                    await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                else:
                    class Modal(discord.ui.Modal):
                        def __init__(self, *args, **kwargs) -> None:
                            super().__init__(*args, **kwargs)

                            self.add_item(discord.ui.InputText(label="New username", max_length=50, min_length=1))

                        async def callback(self, interaction: discord.Interaction):
                            if interaction.user.id in username_change_cooldowns and datetime.datetime.now() - username_change_cooldowns[interaction.user.id] < datetime.timedelta(days=1):
                                await interaction.response.send_message(embed=errorEmbed(ctx.user, "You can change your username again after 1 day. Please wait!"), ephemeral=True)
                                return

                            is_already_registered = await execDB(f"SELECT username FROM {players_column} WHERE LOWER(username)=%s", (self.children[0].value.lower(), ))

                            if len(is_already_registered) != 0:
                                await interaction.response.send_message(embed=errorEmbed(ctx.user, "An account with this username has already been registered. Please choose another one!"), ephemeral=True)
                                return
                            
                            old_username = await execDB(f"SELECT username FROM {players_column} WHERE discord_id=%s", (interaction.user.id, ))

                            await execDB(f"UPDATE {players_column} SET username=%s WHERE discord_id=%s; INSERT INTO logs VALUES (%s, %s, %s, %s)", (self.children[0].value, interaction.user.id, interaction.user.id, interaction.user.id, "username", f"{old_username[0][0]} -> {self.children[0].value}"))
                            username_change_cooldowns[interaction.user.id] = datetime.datetime.now()
                            await interaction.response.send_message(embed=successEmbed(interaction.user, f"Your account username has successfully been changed to `{self.children[0].value}`."), ephemeral=True)

                    await interaction.response.send_modal(Modal(title="Change Username"))

            @discord.ui.button(
                label="Change Password",
                style=discord.ButtonStyle.gray,
                emoji=":pencil:"
            )

            async def change_password(self, button, interaction):
                if interaction.user.id != ctx.user.id:
                    await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                else:
                    class Modal(discord.ui.Modal):
                        def __init__(self, *args, **kwargs) -> None:
                            super().__init__(*args, **kwargs)

                            self.add_item(discord.ui.InputText(label="New password (min. 8 characters)", max_length=50, min_length=8))

                        async def callback(self, interaction: discord.Interaction):
                            pass_hash = generate_hash(self.children[0].value).decode("utf-8")
                            await execDB(f"UPDATE {players_column} SET password=%s WHERE discord_id=%s", (pass_hash, interaction.user.id))
                            await interaction.response.send_message(embed=successEmbed(interaction.user, f"Your account password has successfully been changed."), ephemeral=True)

                    await interaction.response.send_modal(Modal(title="Change Password"))

            @discord.ui.button(
                label="Change Nickname Color",
                style=discord.ButtonStyle.gray,
                emoji=":art:"
            )

            async def change_nickname_color(self, button, interaction):
                if interaction.user.id != ctx.user.id:
                    await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                else:
                    options = []

                    for i in range(len(colors)):
                        color = colors[i]
                        options.append(discord.SelectOption(label=color[0], emoji=color[1], value=str(i)))

                    class ChangeNickColor(discord.ui.View):
                        @discord.ui.select(
                            placeholder="Select a color...",
                            options=options
                        )

                        async def change_color(self, select, interaction):
                            if interaction.user.id != ctx.user.id: # just in case
                                await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                            else:
                                await execDB(f"UPDATE {players_column} SET nickname_color=%s WHERE discord_id=%s", (int(select.values[0]), interaction.user.id))
                                await interaction.response.send_message(embed=successEmbed(interaction.user, "Your chat color has successfully been changed."), ephemeral=True)

                    await interaction.response.send_message(embed=discord.Embed(
                        author=discord.EmbedAuthor(name=interaction.user.name, icon_url=interaction.user.avatar.url),
                        title="Choose a chat nickname color! :art:",
                        description="Now you can choose the color of the nickname you want in the chat by using the select menu!",
                        color=discord.Color.teal()
                    ), view=ChangeNickColor(), ephemeral=True)

            @discord.ui.button(
                label="Delete Account",
                style=discord.ButtonStyle.danger,
                emoji=":wastebasket:"
            )

            async def delete_account(self, button, interaction):
                if interaction.user.id != ctx.user.id:
                    await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                else:
                    class Msg:
                        val = None

                    class Confirm(discord.ui.View):
                        @discord.ui.button(
                            label="Yes!",
                            style=discord.ButtonStyle.red
                        )

                        async def yes(self, button, interaction):
                            if interaction.user.id != ctx.user.id: # just in case
                                await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                            else:
                                await delete_user(interaction.user.id)
                                await Msg.val.delete()
                                await interaction.response.send_message(embed=successEmbed(interaction.user, "Your account has successfully been deleted."), ephemeral=True)

                        @discord.ui.button(
                            label="No!",
                            style=discord.ButtonStyle.green
                        )

                        async def no(self, button, interaction):
                            if interaction.user.id != ctx.user.id: # just in case
                                await interaction.response.send_message(errorEmbed(interaction.user, "You can't interact with this."), ephemeral=True)

                            else:
                                await Msg.val.delete()

                    Msg.val = await interaction.response.send_message(embed=discord.Embed(title="Account Deletion :wastebasket:", description="Are you sure you want to delete your account?", color=discord.Color.red()), view=Confirm(), ephemeral=True)
                    Msg.val = await Msg.val.original_response()

        await ctx.respond(embed=discord.Embed(
            author=discord.EmbedAuthor(name=ctx.user.name, icon_url=ctx.user.avatar.url),
            title="Account Manager :gear:",
            description=f"Here you can manage your account by clicking one of the buttons below!\n\nYour username is: `{username}`\nYour password is hidden for security reasons. If you forgot it, please change it.",
            color=discord.Color.teal()
        ), view=ManageView(), ephemeral=True)

@bot.slash_command(description="Bans a user from using OnlineClicker.")
async def ban_service(ctx, user: discord.Option(discord.User, "The user you want to ban"), reason: discord.Option(str, "The reason for banning the user", max_length=255)): # type: ignore
    user = user if isinstance(user, int) else user.id

    if not isModerator(ctx.user):
        await ctx.respond(embed=errorEmbed(ctx.user, "You can't interact with this."), ephemeral=True)

    else:
        is_banned = await execDB("SELECT reason FROM bans WHERE discord_id=%s", (user, ))

        if len(is_banned) != 0:
            await ctx.respond(embed=errorEmbed(ctx.user, f"This user has already been banned.\nReason: `{is_banned[0][0]}`"), ephemeral=True)
        else:
            await execDB(f"INSERT INTO bans VALUES (%s, %s); INSERT IGNORE INTO logs VALUES (%s, %s, %s, %s);", (user, reason, ctx.user.id, user, "ban", reason))
            await delete_user(user)
            await ctx.respond(embed=successEmbed(ctx.user, f"The user has successfully been banned from using OnlineClicker.\nReason: `{reason}`"))

@bot.slash_command(description="Unbans a user from using OnlineClicker.")
async def unban_service(ctx, user: discord.Option(discord.User, "The user you want to unban"), reason: discord.Option(str, "The reason for unbanning the user", max_length=255)): # type: ignore
    user = user if isinstance(user, int) else user.id

    if not isModerator(ctx.user):
        await ctx.respond(embed=errorEmbed(ctx.user, "You can't interact with this."), ephemeral=True)

    else:
        is_banned = await execDB("SELECT reason FROM bans WHERE discord_id=%s", (user, ))

        if len(is_banned) == 0:
            await ctx.respond(embed=errorEmbed(ctx.user, f"This user isn't banned."), ephemeral=True)
        else:
            await execDB("DELETE FROM bans WHERE discord_id=%s; INSERT IGNORE INTO logs VALUES (%s, %s, %s, %s);", (user, ctx.user.id, user, "unban", reason))
            await delete_user(user)
            await ctx.respond(embed=successEmbed(ctx.user, f"The user has successfully been unbanned from using OnlineClicker.\nReason: `{reason}`"))

bot.load_extension("cogs", recursive=True)
bot.run(getenv("BOT_TEST_TOKEN") if testing else getenv("BOT_TOKEN"))