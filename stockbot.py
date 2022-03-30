import yfinance
import hikari

bot = hikari.GatewayBot(
    token='TOKEN'
    )

list = []

@bot.listen(hikari.GuildMessageCreateEvent)
async def commands(event):

    if (event.content[0] == '!'):
        command = event.content.replace('!', '')

        stock_info = yfinance.Ticker(command).info

        if (stock_info['regularMarketPrice'] == None and command != 'watchlist' and command != 'commands'):
            await event.message.respond('Not a valid ticker.')
            print(stock_info['regularMarketPrice'])

        elif (stock_info['regularMarketPrice'] != None):
            market_price = stock_info['regularMarketPrice']
            await event.message.respond(command + ': ' + str(market_price))

        elif (command == 'watchlist'):
            await event.message.respond('Watchlist:')
            for ticker in list:
                await event.message.respond(str(ticker['symbol']) + ': ' + str(ticker['regularMarketPrice']))

        elif (command == 'commands'):
            embed = hikari.Embed(title='Commands:')
            embed.add_field(name='!SYMBOL', value='current price of symbol', inline=False)
            embed.add_field(name='!watchlist',value='current prices of symbols in watchlist', inline=False)
            embed.add_field(name='-SYMBOL,premarket',value='prices of symbol at open', inline=False)
            embed.add_field(name='-SYMBOL,dayrange',value='price range of the day', inline=False)
            embed.add_field(name='-SYMBOL,add',value='adds symbol to watchlist', inline=False)
            embed.add_field(name='-SYMBOL,remove',value='removes symbol from watchlist', inline=False)

            await event.message.respond(embed = embed)
                        

    elif (event.content[0] == '-'):
        command = event.content.replace('-', '')
        txt = command.split(',')
        
        stock_info = yfinance.Ticker(txt[0]).info

        if (stock_info['regularMarketPrice'] == None and txt[0] != 'watchlist'):
            await event.message.respond('Not a valid ticker.')
            print(stock_info['regularMarketPrice'])

        elif (txt[1].strip() == 'premarket'):
            await event.message.respond('Open: ' + str(stock_info['preMarketPrice']))

        elif (txt[1].strip() == 'dayrange'):
            await event.message.respond("Day's Range: " + str(stock_info['dayLow']) + ' - ' + str(stock_info['dayHigh']))

        elif (txt[1].strip() == 'add'):
            list.append(stock_info)
            await event.message.respond(str(stock_info['symbol']) + ' has been added to watchlist')

        elif (txt[1].strip() == 'remove'):
            if (stock_info in list):
                list.remove(stock_info)
                await event.message.respond(str(stock_info['symbol']) + ' has been removed from watchlist')

        else:
            await event.message.respond('Not a valid command')
        

bot.run()