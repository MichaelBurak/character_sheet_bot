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

#base sheet setting to env SHEET's first tab
sh = gc.open(SHEET)
worksheet = sh.get_worksheet(0)

'''BEGIN COMMANDS
------------------------ '''

#set spreadsheet to user input 
@bot.command()
async def setsheet(ctx,sheet):
    global sh
    sh = gc.open(sheet)
    global worksheet 
    worksheet = sh.get_worksheet(0)
    response = f"Current sheet: {sh.title}"
    await ctx.send(response)

#add new tab to current google sheet with base 100 row and column
@bot.command()
async def addtab(ctx,title="fill this in",rows=100,cols=100):
    sh.add_worksheet(title,rows,cols)
    response = f"Tab of name --{title}-- with {rows} rows and {cols} added to spreadsheet {sh.title}"
    await ctx.send(response)

#switch to user provided tab by name
@bot.command()
async def switchtab(ctx,tab):
    global worksheet
    worksheet = sh.worksheet(tab)
    response = f"Switched tab of spreadsheet to {tab}"
    await ctx.send(response)

#U-pdate a given cell's value
@bot.command()
async def editcell(ctx,cell,val):
    worksheet.update(cell, val)
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- changed value to {val}"
    await ctx.send(response)

#R-ead a given cell's value
@bot.command()
async def readcell(ctx,cell):
    read_val = worksheet.acell(cell).value
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- value is {read_val}"
    await ctx.send(response)

#R-ead a given column or row w/cells delimeted by space
@bot.command()
async def readcells(ctx, direction, idx):
    val_list = []
    if direction == "row":
        val_list = worksheet.row_values(idx)
        response = f"Row no. {idx} reads {' '.join(val_list)}"
        await ctx.send(response)
    elif direction == "column":
        val_list = worksheet.col_values(idx)
        response = f"Column no. {idx} reads {' '.join(val_list)}"
        await ctx.send(response)
    else:
        await ctx.send("Please select row or column as the first argument")

'''END COMMANDS
-------------------- '''

#run the bot using env TOKEN
bot.run(TOKEN)