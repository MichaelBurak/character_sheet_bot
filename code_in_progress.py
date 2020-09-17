''' version of edit cells with confirming/reverting choice
async def editcell(ctx,cell,val):
    prev_val = worksheet.acell(cell).value
    auth = ctx.author 
    # worksheet.update(cell, val)
    response = f"Cell at position {cell} of worksheet --{worksheet.title}-- changed value to {val}, confirm with 'confirm' or revert with 'revert'!"
# and str(reaction.message.content) == 'confirm'
    async def check(reaction, user):
        print(f"Previous value is {prev_val}")
        if user == auth and ctx.message.content == "confirm":
            await worksheet.update(cell, val)
            # return 
        if user == auth and ctx.message.content == "revert":
            print(f"Prev val is {prev_val}")
            await worksheet.update(cell,prev_val)
        try:
            await bot.wait_for('reaction_add', timeout=60.0, check=check)
        #user = ? 
        except asyncio.TimeoutError:
            await ctx.send(response)
        else:
            await ctx.send(f'reverted to {prev_val}')
    await ctx.send(response)
'''

'''kinda a test event for message handling with wait_for('message'), not really a command of relevance
@bot.event
async def on_message(message,bot=bot):
    # for some reason doesn't seem to block on the first message?
        
        channel = message.channel
        
        def msg_info(m):
            return m.author == message.author and m.channel == message.channel and m.content == message.content and m.author.id == message.author.id

        msg = await bot.wait_for('message', check=msg_info)
        if msg.content.startswith('whoami?'):
                print("Author id is {.author.id}".format(msg))
                await channel.send('Hello {.author}!'.format(msg))
                await bot.process_commands(message)
        else:
            await bot.process_commands(message)
'''