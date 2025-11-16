import discord
from discord.ext import commands, tasks
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz
import asyncio


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = RotatingFileHandler(filename='discord.log', encoding='utf-8', mode='a', maxBytes=10*1024*1024, backupCount=5)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

subjects: list[str] = ["Calculo","Electronica Digital","Algebra","ICO","Progrmacion","Trusted"] #easier to modify 

roles: list[str] = ["Admin","Tech Support"] 

secret_role:str = "trusted"

#subjects became roles too

roles += subjects

class BRM:
    """Backend Error Manager:how about hiping this up with a error center\n
       we could connect it to a separate admin log with a specific format to identify errors easier"""

    def __init__(self, error, pleace, problem): #demo version, the error-type, the pleace of the code it happened, and a 1-2 word problem description, maybe even with enum inheritance at this point lol
        pass



class Proyect:
    """wraps all information related to a proyect, and generates an instance \n 
    with all the attributes present, if data is missing, it rases ValueError"""
    proyectbase:list["Proyect"] = []    #contains all proyects at a class level, for discarding or accepting the proyects
    _SN_ = object() #fullname: _SENTINEL_VALUE_ -> to check wether all values have correctly been inputed, I know its kinda usseless, its a habit at this point
    def __init__(self): #cant even write discord.member as a type :c
        
        self.name = Proyect._SN_
        self.team_leader = Proyect._SN_
        self.related_subject = Proyect._SN_
        self.member_requests = Proyect._SN_
        self.members = Proyect._SN_
        self.approval_state = Proyect._SN_     #wether the moderators have approved or denied the proyect
        self.server_of_origin = Proyect._SN_

    def __str__(self):
        # Compute max widths for each attribute
        max_name = max(len(str(obj.name)) for obj in Proyect.proyectbase)   #I know its already an str, last safeguard I guess, would be great to automate the type check later on
        max_team_leader = max(len(str(obj.team_leader)) for obj in Proyect.proyectbase)
        max_member_requests = max(len(str(obj.member_requests)) for obj in Proyect.proyectbase)
        max_members = max(len(str(obj.members)) for obj in Proyect.proyectbase)
        max_approval_state = max(len(str(obj.approval_state)) for obj in Proyect.proyectbase)
        max_server_of_origin = max(len(str(obj.server_of_origin)) for obj in Proyect.proyectbase)

        # Return an aligned formatted string -> if we want to print all of them this could come in handy
        return (
            f"{self.name:<{max_name}}  " #lets aligne it to the left just cuz 
            f"{self.team_leader:<{max_team_leader}}  "
            f"{self.member_requests:<{max_member_requests}}  "
            f"{self.members:<{max_members}}  "
            f"{self.approval_state:<{max_approval_state}}"
            f"{self.server_of_origin:<{max_server_of_origin}}"
    )
    
    @property
    def check_object(self):
        """Return list of attributes still using the sentinel."""
        missing = []
        for attr, value in vars(self).items():
            if value is Proyect._SN_:
                missing.append(attr)
        return missing  # empty list means everything OK
        #therefore, missing: means smt is wrong

        
    @classmethod    #for trusted members to create proyect requests
    def create_proyect(cls,*, name:str, team_leader:discord.member,related_subject:str | bool, member_requests:discord.member,server_of_origin:discord.guild):   #again, I say its a string because I cant write discord.member as a type
        """for trusted members to create proyect requests"""
        self = cls()    #init runs when an instance is created
        
        self.name = name
        self.team_leader =  team_leader
        self.related_subject = related_subject #we can make the related subject None by default althought maybe its stupid, unsure
        self.member_requests = member_requests
        self.members = []
        self.approval_state = False
        self.server_of_origin = server_of_origin
        if self.check_object:
            raise ValueError("at list one of the required values wasnt given")
        
        
        Proyect.proyectbase.append(self)

        return self
    


def get_users_from_list():
    """Read existing user IDs from User_List file."""
    user_ids = set()
    try:
        with open("User_List", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # New format: ID|DisplayName|Timestamp or ID|DisplayName - Joined: Timestamp
                if "|" in line:
                    user_id_str = line.split("|")[0].strip()
                    try:
                        user_id = int(user_id_str)
                        user_ids.add(user_id)
                    except ValueError:
                        continue
                elif line.startswith("ID:"):
                    try:
                        user_id = int(line.split("ID:")[1].split()[0])
                        user_ids.add(user_id)
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        pass
    return user_ids
async def sync_users_to_list():
    """Check all members on server and add any missing ones to User_List."""
    cet = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(cet).strftime("%Y-%m-%d %H:%M:%S CET")
    existing_user_ids = get_users_from_list()
    
    # Get all members from all guilds
    missing_members = []
    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot and member.id not in existing_user_ids:  # Exclude bots and existing users
                missing_members.append(member)
    
    # Add missing members to the list
    if missing_members:
        with open("User_List", "a", encoding="utf-8") as f:
            for member in sorted(missing_members, key=lambda m: m.id):
                f.write(f"{member.id}|{member.display_name}|{current_time}\n")
        print(f"Added {len(missing_members)} missing member(s) to User_List")
    return len(missing_members)

@bot.event
async def on_ready():

    def load_bad_words(path="bad-words"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    @tasks.loop(hours=1)
    async def hourly_sync():
        """Sync users every hour."""
        await sync_users_to_list()

    
    
    global bad_words 
    bad_words = load_bad_words()
    print(f"We are ready to go in, {bot.user.name}")
    await sync_users_to_list()
    hourly_sync.start()
        
    try:# Ensure slash commands are synced to the guild ones
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")


#control functions related to member automated - management
@bot.event
async def on_member_remove(member):
    # Remove member by ID from User_List
    try:
        with open("User_List", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("User_List", "w", encoding="utf-8") as f:
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    f.write(line)
                    continue
                # Check if line contains member.id (handles both new format ID|DisplayName|Timestamp and old formats)
                if "|" in line_stripped:
                    # Extract ID from format: ID|DisplayName|Timestamp
                    try:
                        line_id = int(line_stripped.split("|")[0].strip())
                        if line_id == member.id:
                            continue  # Skip this line (member being removed)
                    except (ValueError, IndexError):
                        pass
                f.write(line)
    except FileNotFoundError:
        pass

def get_role_case_insensitive(guild: discord.Guild, name: str):
    """Return the role whose name matches case-insensitively, or None."""
    return discord.utils.find(lambda r: r.name.lower() == name.lower(), guild.roles)

def bot_has_permission(guild: discord.Guild, permission: str) -> bool:
    """Check if the bot has a specific guild-level permission."""
    me = guild.me if guild and guild.me else None
    if not me:
        return False
    perms = me.guild_permissions
    return getattr(perms, permission, False)

@bot.event
async def on_member_join(member: discord.Member):

    real_name = "-" 
    try:
        await member.send(f"Welcome to the server, {member.display_name}! 🎉")
        await member.send("What is your actual name?")

        def check(m: discord.Message):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        # wait_for with a sensible timeout
        msg = await bot.wait_for("message", check=check, timeout=None)
        # sanitize pipe to keep your `|`-separated file format
        real_name = msg.content.replace("|", "¦").strip() or "-"
        await member.send(f"Thanks, {real_name}! Your name has been noted.")
        # Set their nickname on the server
        nickname = real_name if real_name != "-" else None
        if nickname and bot_has_permission(member.guild, "manage_nicknames"):
            nickname = nickname[:32]  # Discord limit
            try:
                await member.edit(nick=nickname, reason="Provided real name to welcome DM")
            except discord.Forbidden:   #check missing permissions, never happens due to bot_has_permission
                await member.send("I couldn't change your server nickname due to missing permissions.")
            except discord.HTTPException:   #when the discord servers API denies or doesnt answer the request
                await member.send("There was an error changing your nickname, but I saved your name.")
        elif nickname:  #in truth 
            await member.send("I don't have permission to change nicknames right now; please ask a moderator.")

        # Assign Trusted role after they provide their name
        role = get_role_case_insensitive(member.guild, secret_role)
        if role and bot_has_permission(member.guild, "manage_roles"):
            await member.add_roles(role, reason="Assigned after providing name")
            system_channel = member.guild.system_channel
            if system_channel:
                await system_channel.send(f"{member.mention} has been assigned to {secret_role}")
        elif role:
            await member.send("I couldn't assign you the trusted role because I am missing permissions. Please contact a moderator.")
    except discord.Forbidden:
        pass
    except asyncio.TimeoutError:
        try:
            await member.send("No worries—if you want me to note your name later, just DM me.")
        except discord.Forbidden:
            pass

    tz = pytz.timezone("Europe/Berlin")  # CET/CEST
    join_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    display_name_sanitized = member.display_name.replace("|", "¦").strip() or "-"
    try:
        with open("User_List", "a", encoding="utf-8") as f:
            # Format: ID|DisplayName|RealName|Timestamp
            f.write(f"{member.id}|{display_name_sanitized}|{real_name}|{join_time}\n")
    except Exception as e:
        print(f"Failed to write User_List: {e}")

@bot.command()
@commands.has_role(secret_role)
async def study(ctx, member: discord.Member):
    try:
        await member.send(f"Hey what would you like to study?, {member.display_name}!")
        await member.send(f"What do you wish to study?: {' '.join(subjects)}")   #we create a clean string containing all assigments
        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)
        msg = await bot.wait_for("message", check=check, timeout=None)

        study_choice = msg.content.replace("|","!").strip()
    
        role_name = study_choice

        if role_name in subjects: #we check wether the requested subject-type is valid 
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role:
                await member.add_roles(role, reason=f"For study of {role} ")
                system_channel = member.guild.system_channel
            
                if system_channel:
                    await system_channel.send(f"{member.mention} has been assigned to {role.name}")
                else:
                    await member.send("Role not found in the server.")
            else:
                await member.send("Invalid study choice. Please try again.")
        else:
                await member.send("Invalid study choice. Please try again.") #outer case in case the requested subject - type is uncorrect

    except asyncio.TimeoutError:
        await member.send("You took too long to respond. Please try the command again.")
    except discord.Forbidden:
        await member.send("I don't have permission to assign roles. Please contact tech support.")


@bot.command()  #to salute yourself xd
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()  #ussed to assign trusted role as of now
async def assign(ctx):
    role = get_role_case_insensitive(ctx.guild, secret_role)
    if role and bot_has_permission(ctx.guild, "manage_roles"):
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    elif role:
        await ctx.send("I can't assign that role right now; please check my permissions.")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):  #ussed to remove the usser 
    role = get_role_case_insensitive(ctx.guild, secret_role)
    if role and bot_has_permission(ctx.guild, "manage_roles"):
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    elif role:
        await ctx.send("I can't remove that role right now; please check my permissions.")
    else:
        await ctx.send("Role doesn't exist")

#unclasified - commands
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

#trusted only commands
@bot.command()
@commands.has_role(f"{secret_role}")
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@bot.command(name = "groupcreate")
@commands.has_role(secret_role)
async def groupcreate(ctx):
    """Interactive step-by-step project creation wizard."""

    author = ctx.author

    def check(m: discord.Message):
        return m.author == author and m.channel == ctx.channel  
    #copy pasted your function from before, wanted to make it a global method, but outside ctx thoesnt exist so it raises error sadly

    await ctx.send("**Let's create a new project!**\n(Type `cancel` at any time to stop.)")
    #in python descriptions ussing **smt** makes it appear pretty, unsure wether it works with ctx :/


    # 1 – Project name

    await ctx.send("Step 1/3 — **Enter the project name:**")

    while True:
        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() == "cancel":
            await ctx.send("Project creation cancelled.")
            return

        project_name = msg.content.strip()
        if len(project_name) >= 3:
            break
        else:
            await ctx.send("Project name is too short. Try again:")


    # 2 – Related subject

    lines = []
    for i, s in enumerate(subjects):
        lines.append(f"{i+1}. {s}")
    subj_text = "\n".join(lines)    #this way, the usser can answer by tiping the subjects number directly

    await ctx.send(
        f"Step 2/3 — **Choose the related subject:**\n"
        f"{subj_text}\n\n"
        f"Reply with the number."
    )

    while True:
        msg = await bot.wait_for("message", check=check)
        if msg.content.lower() == "cancel":
            await ctx.send("Project creation cancelled.")
            return

        try:
            if msg.content.strip().isdigit():   #if its a number
                num = int(msg.content.strip()) - 1
                if 0 <= num < len(subjects):    #check wether the number is a valid one
                    related_subject = subjects[num]
                    break
                else:
                    await ctx.send("Invalid number. Try again:")
            else:   #if the usser inputs CORRECTLY the name of the subject
                unmach = False
                for item in subjects:
                    if item.lower() == msg.content.strip().lower():  #check if msg is in subjects
                        related_subject = item
                        break
                if unmach:
                    await ctx.send("Please enter a valid number or a subject correctly: ")



        except ValueError:
            await ctx.send("Please enter a valid number or a subject correctly: ")


    # 3 – Member selection

    await ctx.send(
        "Step 3/3 — **Enter up to 5 member names**, separated by commas.\n"
        "Example: `Luka, Antal, Sergio`\n"
        "(Leave empty or type `none` if no members)."
    )

    while True:
        msg = await bot.wait_for("message", check=check)
        content = msg.content.strip()

        if content.lower() == "cancel":
            await ctx.send("Project creation cancelled.")
            return

        if content.lower() in ("", "none"):
            member_list = []
            break

        member_list = [m.strip() for m in content.split(",") if m.strip()]
        if len(member_list) <= 5:
            break
        else:
            await ctx.send("You can only include up to 5 members. Try again:")


    try:
        Proyect.create_proyect(name=project_name,team_leader=ctx.author,related_subject=related_subject,member_requests=member_list, server_of_origin = ctx.guild)
    except Exception as e:
        await ctx.send(f"Failed to create project: `{e}`")
        return


    # return a random message confirming the creation

    await ctx.send(
        "**Project created successfully!**\n\n"  
        f"**Name:** {project_name}\n"
        f"**Leader:** {ctx.author.display_name}\n"
        f"**Subject:** {related_subject}\n"
        f"**Members:** {', '.join(member_list) if member_list else 'None'}"
    )

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole): 
        await ctx.send("You do not have permission to do that!")

#staff commands
@bot.command(name="update_user_list")
@commands.has_role("test dev")
async def update_user_list(ctx):
    async with ctx.typing():
        added = await sync_users_to_list()
    await ctx.send(f"User_List updated. Added {added} new member(s).")

@update_user_list.error 
async def update_user_list_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to update the User_List.")
    else:
        await ctx.send("An error occurred while updating the User_List.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)