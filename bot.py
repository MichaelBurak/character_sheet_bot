# bot.py
import os
import random
import re
import gspread

from discord.ext import commands
from dotenv import load_dotenv

#oAuth gspread to access google drive/sheets
gc = gspread.oauth()

#env var handling of token and testing Google Sheet
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SHEET = os.getenv("BASE_SHEET")

#prefix for cmnds is !
bot = commands.Bot(command_prefix='!')
timer_id= None
#base sheet setting to env SHEET's first tab
sh = gc.open(SHEET)
worksheet = sh.get_worksheet(0)

'''Helper functions'''

''' Events ''' 
@bot.listen()
async def on_message(message):
    '''This function is to parse out and extract arguments displayed 
    from another bot on the server, particularly a timer. '''

    starting_timer_str = "The timer is now set for"
    timer_end_prompt = "To end the timer, type `t?stop`"

    #fail gracefully if bot is sender 
    global bot 
    if message.author.id == bot.user.id:
        return 

    #need to remove "``" but otherwise grabs time
    if message.content.startswith(starting_timer_str):
        time_amt = message.content.split("for",1)[1].replace(timer_end_prompt,"").replace("`","").partition("When the timer ends")[0]
        global timer_id
        timer_id = message.author.id

    #store the characters after "it will send" in a variable as to dump into sheet
    if message.content.find("it will send") == -1:
        return
    else:
        #grabbing message and sheet dump of message and time with formatting to arbitrary cell
        sent_msg_sanitized= message.content.partition("send")[2].partition("to")[0].replace("`","").replace('"', "")
        #here is where it gets tricky, linking the mentioned user worksheet and the user
        #message.mentions would be key here 
        
        #needs to check if forcibly stopped 
        conf = await bot.wait_for('message', check=lambda message: message.author.id == timer_id and "has ended" in message.content)
        
        if conf: 
            worksheet.update("A1", f"Action:{sent_msg_sanitized}, taking: {time_amt}")
        
        # deny = await bot.wait_for('message', check=lambda message: message.author.id == timer_id and "stopped forcibly" in message.content)
        # if deny:
        #     print("FORCEQUIT")
        #     return

'''BEGIN COMMANDS
------------------------ 

Resources and methods to map out and code: 
-Tabs(worksheets)
    -Create
    -Reading?
    -Update current 
-Cells
    -Create
    -Reading (values)
    -Updating (values)
    -Deleting (clearing)
        -Columns
            -Create
            -Reading
            -Updating
            -Deleting
        -Rows
            -Create
            -Reading
            -Updating
            -Deleting
        -Ranges 
            -Create
            -Reading
            -Updating
            -Deleting
'''

#---Sheets---

@bot.command()
async def setsheet(ctx,sheet):
    '''UPDATES current spreadsheet from user input'''
    global sh
    sh = gc.open(sheet)
    global worksheet 
    worksheet = sh.get_worksheet(0)
    response = f"Current sheet: {sh.title}"
    await ctx.send(response)

#---Tabs---
#CREATE new tab to current google sheet with base 100 row and column
# @bot.command()
# async def addtab(ctx,title="fill this in",rows=100,cols=100):
#     sh.add_worksheet(title,rows,cols)
#     response = f"Tab of name --{title}-- with {rows} rows and {cols} added to spreadsheet {sh.title}"
#     await ctx.send(response)

#READ
#Reading whole tab to pandas or other libraries?


@bot.command()
async def switchtab(ctx,tab):
    '''UPDATE current tab to user provided tab by name'''
    global worksheet
    worksheet = sh.worksheet(tab)
    response = f"Switched tab of spreadsheet to {tab}"
    await ctx.send(response)



@bot.command()
async def cleartab(ctx):
    '''#DELETE to clear whole tab, with user confirmation/deny'''
    await ctx.send("Are you sure you want to clear this tab? Y or N")

    #checks for y/n from user
    async def confirmation(m):
        return m.content.lower() in ["y", "n"] and ctx.message.author == ctx.author

    msg = await bot.wait_for('message', check=confirmation)

    if msg.content.lower() == "y":
        global worksheet
        worksheet.clear()
        await ctx.send("Tab cleared") 
    elif msg.content.lower() == "n":
        await ctx.send("Cancelled clearing of tab")

#---Cells---

#CREATE a cell?
#Does this have a use case on a properly formatted sheet? This is probably create row/column coverage.

#CREATE a column or row at given position
# @bot.command()
# async def createcells(ctx,direction='column',n=1,idx=1):
#     #TBD
#     await ctx.send("Check back later for implementation of creating columns and rows with this command!")


@bot.command()
async def editcell(ctx,cell,val):
    '''UPDATES a given cell's value'''
    worksheet.update(cell, val)
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- changed value to {val}"
    await ctx.send(response)


@bot.command()
async def readcell(ctx,cell, location=None):
    '''READS a given cell's value or cell at pre-set location
    (not yet implemented)'''
    read_val = worksheet.acell(cell).value
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- value is {read_val}"
    await ctx.send(response)


@bot.command()
async def readcells(ctx, direction, idx, location=None):
    '''READS a given column or row w/cells delimeted by space at given index or pre-set location
    (not yet implemented)'''
    val_list = []
    if direction == "row":
        if location:
            await ctx.send("Row location")
        else:
            val_list = worksheet.row_values(idx)
            response = f"Row no. {idx} reads {' '.join(val_list)}"
            await ctx.send(response)
    elif direction == "column":
        if location:
            await ctx.send("Column location")
        else:
            val_list = worksheet.col_values(idx)
            response = f"Column no. {idx} reads {' '.join(val_list)}"
            await ctx.send(response)
    else:
        await ctx.send("Please select row or column as the first argument")

'''END COMMANDS
-------------------- '''

#run the bot using env TOKEN
bot.run(TOKEN)