# setup env
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# settup developement
import interactions # for slash commands
from interactions.ext.tasks import IntervalTrigger, create_task 

bot = interactions.Client(token=os.environ.get("TOKEN"),default_scope=os.environ.get("GUILD_ID_TEST"))

class Scheduler():
    def __init__(self):
        self.channel = None
        self.isupdating = False
    
    def update(self, ctx):
        # collect channel
        self.channel = ctx.channel


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

# setup camp filter
from campfilter import iscamp_update, recommend

# create a task to update the camps every 30 minutes
@create_task(IntervalTrigger(10))
async def update_task():
    def article_model(camp_data):
        data = camp_data
        return f"""
        {data['link']}
        {data['small_description']}
        จัดโดย {data['organizer']}
        ค่าใช้จ่าย {data['costs']}
        """

    def get_recommend(camp):
        isnice, why = recommend(camp)
        if isnice is None:
            return '' # no recommendation/feedback
        elif isnice:
            return f"**⭐** {why}"
        else:
            return f"**⛔** {why}" 

    if schedule.isupdating and schedule.channel is not None:
        # get update
        isupdate, camp, changes = iscamp_update(test=True)
        if isupdate:
            # send update
            embeds = interactions.Embed(title=f"ค่าย/งานแข่งใหม่ {changes} งาน", description=f"ระบบ Update กิจกรรมสายคอม T2CNS https://github.com/DevCommunities/T2CNS \n ⭐ (ฟรี/ค่ายดี/งานน่าแข่ง) \n ⛔ (ค่ายเปลืองตัง/แพง/เกียรติบัตรไม่มีประโยชน์/เรียนใน youtube ฟรีได้)", color=0x00ff00)
            for i in range(changes):
                embeds.add_field(name=f"{camp[i]['title']} {get_recommend(camp[i])}", value=article_model(camp[i]), inline=False)
            await schedule.channel.send(embeds=embeds)
        else:
            print('no update')

# start the task
update_task.start()
bot.start()