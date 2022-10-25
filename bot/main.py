# setup env
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# settup developement
import discord
import interactions # for slash commands
from interactions.ext.tasks import IntervalTrigger, create_task 

bot = interactions.Client(token=os.environ.get("TOKEN"),default_scope=os.environ.get("GUILD_ID_TEST"))

class Scheduler():
    def __init__(self):
        self.ctx = None
        self.isupdating = False
    
    def update(self, ctx):
        self.ctx = ctx


schedule = Scheduler()

# server owner can set command permissions themself
@bot.command(name="setup",description="Setup this channel for Default notification update")
async def use_this_channel(ctx: interactions.CommandContext):
    schedule.update(ctx)
    await ctx.send(f"Select this channel '{ctx.channel_id}' for notification updates!")

@bot.command(name="start_stop_t2cns", description="start T2CNS with 30 min schedule feed update")
async def schedule_update(ctx: interactions.CommandContext):
    if schedule.isupdating:
        await ctx.send("Already updating! now stopping...")
        schedule.isupdating = False
    else:
        await ctx.send(f"t2cns started with 30 min schedule feed update...")
        schedule.isupdating = True

# create a task to update the channel every 10 seconds
@create_task(IntervalTrigger(10))
async def update_task():
    if schedule.isupdating and schedule.ctx is not None:
        await schedule.ctx.send("Updating channel...")

# start the task
update_task.start()
bot.start()