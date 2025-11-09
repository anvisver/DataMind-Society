
import discord
from discord.ext import commands
from discord.ext.commands import Context

usserbase:list["Usser"] = []
projectbase:list["Project"] = []

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class Usser:
    r"""
    registry of all ussers in the server
    """
    _SENTRY_VALUE_:object = object()
    def __init__(self, ussername:discord.member):

        self.ussername = ussername

        self.servers_that_usser_belongs_to:list[discord.Guild] = []

        pending_requests:dict["Project":bool] = {} #my idea was the following, None means the usser hasnt decided yet, 
        #if more than 2 days pass, the request times out, if its accepted (True), or denied (False),it will either way dissapear, 
        # we will usse an instance method or smt like that to check that kind of think
    def __contains__(self,item:tuple):  #un tuple de 2 valores, primero es usser, segundo es server
        #this method enables me to usse "in" directly over this object
        #might be slightly usseless, unsure

        return item in self.servers_that_usser_belongs_to
    
class Project:
    r"""
    """
    
    def __init__(self, proyect_name:str, leader:Usser, member_requests):

        self.proyect_name = proyect_name
        self.leader = leader
        self.member_requests = member_requests
        self.members = []

@bot.event
async def on_ready():
    for g in bot.guilds:    #I know we only have 1 server but whatever, scalability always cames in handy
        async for m in g.fetch_members(limit=None):
            # find existing user
            existing_user = next((u for u in usserbase if u.ussername == m.name), None)

            if not existing_user:
                usserbase.append(Usser(m.name).servers_that_usser_belongs_to.append(g))

            else:
                if g not in existing_user.servers_that_usser_belongs_to:
                    existing_user.servers_that_usser_belongs_to.append(g)

    await bot.close()

@bot.command(name = "DataMindSociety")
async def create_project(ctx:Context, project_name: str, *members: discord.Member): #ctx is related to the discord in built command line "Context"
    """
    Usage: !DataMindSociety <project_name> @member1 @member2 ...
    mention @ format is required, to avoid ussing unspecified strings
    """
    leader = ctx.author
    #limit number of participants to 5 as an example
    if len(members) > 5:
        await ctx.send("Threshold overstepped")
        return 
    projectbase.append(Project(name=project_name, leader=leader, member_requests= members))

    #we probably need rn another storage for staff proyect management, unsure about this part as of now
    

bot.run("DataMindSociety") #the name might be wrong, please check it out