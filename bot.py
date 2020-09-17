# bot.py
import os
import random
import re
import gspread

from discord.ext import commands
from dotenv import load_dotenv

gc = gspread.oauth()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SHEET = os.getenv("BASE_SHEET")

bot = commands.Bot(command_prefix='!')

#base sheet setting, hide/comment out on commits
sh = gc.open(SHEET)
worksheet = sh.get_worksheet(0)

@bot.command()
async def setsheet(ctx,sheet):
    global sh
    sh = gc.open(sheet)
    global worksheet 
    worksheet = sh.get_worksheet(0)
    response = f"Current sheet: {sh.title}"
    await ctx.send(response)

@bot.command()
async def addtab(ctx,title="fill this in",rows=100,cols=100):
    sh.add_worksheet(title,rows,cols)
    response = f"Tab of name --{title}-- with {rows} rows and {cols} added to spreadsheet {sh.title}"
    await ctx.send(response)

@bot.command()
async def switchtab(ctx,tab):
    global worksheet
    worksheet = sh.worksheet(tab)
    response = f"Switched tab of spreadsheet to {tab}"
    await ctx.send(response)


@bot.command()
async def editcell(ctx,cell,val):
    worksheet.update(cell, val)
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- changed value to {val}"
    await ctx.send(response)

@bot.command()
async def readcell(ctx,cell):
    read_val = worksheet.acell(cell).value
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- value is {read_val}"
    await ctx.send(response)

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


bot.run(TOKEN)