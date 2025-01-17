import discord
from discord.ext import commands
import aiohttp
import json

class General:
    """
        Commands to search the ArchWiki, Arch package repositories, and AUR
    """

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(pass_context=True)
    async def repos(self, ctx, *, query=None):
        """Search for a package from the Arch Linux repositories"""
        Repo = 'Repo'
        Arch = 'Arch'
        Name = 'Name'
        Relevance = 1

        if query is None:
            return await self.bot.say('Invalid amount of arguments passed.')

        print('Searching for {0} in Arch repositories.'.format(query))

        await self.bot.say('Searching for {0} in the Arch repositories.'.format(query))
        pkgs = [['Name','Repo','Arch']]
        pkgsinfos = [['Name','Repo','Arch','Version','Description','URL']]
        
        async with aiohttp.get('https://www.archlinux.org/packages/search/json/?q={0}'.format(query)) as r:
                ar = await r.json()
                ar = ar['results']
                print(len(ar))
                for count, res in enumerate(ar):
                    if count < 20:
                        if not res['pkgname'] in pkgs:
                            pkgs.append([res['pkgname'],res['repo'],res['arch']])
                            pkgsinfos.append([res['pkgname'],res['repo'],res['arch'],res['pkgver']+"-"+res['pkgrel'],res['pkgdesc'],res['url']])
                            pkgname = res['pkgname']
                    else:
                        count -= 1
        
        if(len(pkgs) > 1):
            result = ''
            for cnt, i in enumerate(pkgs):
                #print(i)
                for _cnt, ii in enumerate(pkgsinfos):
                    if i[0] != 'Name' and i[1] != 'Repo' and i[2] != 'Arch':
                        if i[1] != Repo or i[2] != Arch or i[0] != Name:
                            result += '#' + str(Relevance) + '  Repo: ' + i[1] + '  | Arch: ' + i[2] + '  | Name: ' + i[0] + "\n"
                            Repo = i[1]
                            Arch = i[2]
                            Name = i[0]
                            Relevance += 1
            
            pkgmessage = discord.Embed(title='Reply with the name of one of the following package names within 30 seconds to get more information',description=result)
            await self.bot.send_message(ctx.message.channel, embed=pkgmessage)
            
            def reply_check(m):
                print('Content of m : ' + m)
                for cnt, i in enumerate(pkgs):
                    if m == i[0]:
                        print ("Is in the search results")
                        return True

            userReply = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

            try:
                replyMatch = reply_check(userReply.content)
            except Exception as error:
                print(error)
                print('Probably a time-out')

            if userReply is None:
                await self.bot.say('Timed out.')
            elif replyMatch == True:
                for j in pkgsinfos:
                    print("Ready to send info")
                    if userReply.content in j:
                        print("Found package: ")
                        print(j)
                        pName = userReply.content
                        pVersion = j[3]
                        pDescription = j[4]
                        pArch = j[2]
                        pRepo = j[1]
                        pSourceURL = j[5]
                        pkgdescription = discord.Embed(title="Info on: {0}".format(pName), description='Package Name: {0}\n Version: {1}\n Description: {2}\n Arch: {3}\n Repo: {4}\n Source: {5}'.format(pName, pVersion, pDescription, pArch, pRepo, pSourceURL))
                        await self.bot.send_message(ctx.message.channel, embed=pkgdescription)
                        return
            else:
                return await self.bot.say("Previous search was exited.")
        else:
            return await self.bot.say("No results found.")
        
    @commands.command(pass_context=True)
    async def aur(self, ctx, *, query=None):
        """Search for a package from the AUR"""
        Repo = 'Repo'
        Arch = 'Arch'
        Name = 'Name'
        Relevance = 1

        if query is None:
            return await self.bot.say('Invalid amount of arguments passed.')

        print('Searching for {0} in the AUR.'.format(query))

        await self.bot.say('Searching for {0} in the AUR.'.format(query))
        pkgs = [['Name','Repo','Arch']]
        pkgsinfos = [['Name','Repo','Arch','Version','Description','URL']]
        
        async with aiohttp.get('https://aur.archlinux.org/rpc.php?type=search&arg={0}'.format(query)) as r:
                ar = await r.json()
                ar = ar['results']
                print(len(ar))
                #print(ar)
                for count, res in enumerate(ar):
                    #print(count)
                    if count < 20:
                        #print(res)
                        if not res['Name'] in pkgs:
                            pkgs.append([res['Name'],'AUR','any'])
                            print([res['Name'],'AUR','any'])
                            pkgsinfos.append([res['Name'],'AUR','any',res['Version'],res['Description'],res['URL']])
                            #Name = res['Name']
                    else:
                        count -= 1
        
        if(len(pkgs) > 1):
            result = ''
            for cnt, i in enumerate(pkgs):
                #print(i)
                if i[0] != 'Name' and i[1] != 'Repo' and i[2] != 'Arch':
                    if i[1] != Repo or i[2] != Arch or i[0] != Name:
                        result += '#' + str(Relevance) + '  Repo: ' + i[1] + '  | Arch: ' + i[2] + '  | Name: ' + i[0] + "\n"
                        Repo = i[1]
                        Arch = i[2]
                        Name = i[0]
                        Relevance += 1
            
            pkgmessage = discord.Embed(title='Reply with the name of one of the following package names within 30 seconds to get more information',description=result)
            await self.bot.send_message(ctx.message.channel, embed=pkgmessage)
            
            def reply_check(m):
                print('Content of m : ' + m)
                for cnt, i in enumerate(pkgs):
                    if m == i[0]:
                        print ("Is in the search results")
                        return True

            userReply = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

            try:
                replyMatch = reply_check(userReply.content)
            except Exception as error:
                print(error)
                print('Probably a time-out')

            if userReply is None:
                await self.bot.say('Timed out.')
            elif replyMatch == True:
                for j in pkgsinfos:
                    print("Ready to send info")
                    if userReply.content in j:
                        print("Found package: ")
                        print(j)
                        pName = userReply.content
                        pVersion = j[3]
                        pDescription = j[4]
                        pArch = j[2]
                        pRepo = j[1]
                        pSourceURL = j[5]
                        pkgdescription = discord.Embed(title="Info on: {0}".format(pName), description='Package Name: {0}\n Version: {1}\n Description: {2}\n Arch: {3}\n Repo: {4}\n Source: {5}'.format(pName, pVersion, pDescription, pArch, pRepo, pSourceURL))
                        await self.bot.send_message(ctx.message.channel, embed=pkgdescription)
                        return
            else:
                return await self.bot.say("Previous search was exited.")
        else:
            return await self.bot.say("No results found.")

    @commands.command(pass_context=True)
    async def wiki(self, ctx, *, query=None):
        """Search for an article from the ArchWiki"""
        if query is None:
            return await self.bot.say('Invalid amount of arguments passed.')

        articlelist = []

        await self.bot.say('Searching for {0} in the ArchWiki.'.format(query))
        
        async with aiohttp.get('https://wiki.archlinux.org/api.php?action=opensearch&format=json&search={0}'.format(query)) as r:
            ar = await r.json()
            print(ar)
            for i in ar:
                print (i)
                articles = ar[1]
                print(articles)
                links = ar[3]
                print(links)
                for cnt, j in enumerate(articles):
                    if cnt < 35:
                        if not j in articlelist:
                            articlelist.append([j, links[cnt]])
                    else:
                        count=-1

        if (len(articlelist) > 1):
            result = ''
            Name = []
            for cnt, i in enumerate(articlelist):
                if i[0] not in Name:
                    Name.append(i[0])
                    result += '#' + str(cnt+1) + ') ' + i[0] + '\n'
                    print(result)

            articlemessage = discord.Embed(title="Reply with one of the following titles within 30 seconds to get more information", description=result)
            await self.bot.send_message(ctx.message.channel, embed=articlemessage)
            
            def reply_check(m):
                print('Content of m : ' + m)
                for cnt, i in enumerate(articlelist):
                    if m == i[0]:
                        print ("Is in the search results")
                        return True
            userReply = await self.bot.wait_for_message(timeout=30.0, author=ctx.message.author)

            try:
                replyMatch = reply_check(userReply.content)
            except Exception as error:
                print(error)
                print('Probably a time-out')

            if userReply is None:
                await self.bot.say('Timed out.')
            elif replyMatch == True:
                for j in articlelist:
                    if userReply.content in j:
                        print(j)
                        articleName=userReply.content
                        articleURL=j[1]
                        articleDescription = discord.Embed(title="ArchWiki page on: {0}".format(articleName), description='Link: {0} \n'.format(articleURL))
                        await self.bot.send_message(ctx.message.channel, embed=articleDescription)
                        return
            else:
                return await self.bot.say("Previous search was exited.")

        else:
            return await self.bot.say("No results found.")
