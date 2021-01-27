import mysql.connector as mysql
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

#Inutil
#
#class Personas:
#    def __init__(self,name,rank,descripcion):
#        self.name=name
#        self.rank=rank
#        self.descripcion=descripcion
#        
#    def __repr__(self):
#        return repr((self.name,self.rank,self.descripcion))

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
#Prefijo del bot
bot = commands.Bot(command_prefix='%')
global temp
temp=False

#!ranking [rank]
#!+1
@bot.command(name='change')
async def subir(ctx,p1:discord.Member,*args):
    bool=True
    signo=True
    def inserta(p1,rangos,nivel,descripcion,ctx):
        conexion=mysql.connect(host='localhost',user='root',passwd='',db='niveles2')
        cursor=conexion.cursor(prepared=True)
        cursor.execute("select id_usuario from usuario where nombre='"+str(p1)+"' limit 1;")
        
        try:
            id_usuario=int(cursor.fetchone()[0])
            print(id_usuario)
        except TypeError as e:
            print(e)
            cursor.execute("insert into usuario(nombre) values('"+str(p1)+"');")
            conexion.commit()
            cursor.execute("select id_usuario from usuario where nombre='"+str(p1)+ "';")
            id_usuario=int(cursor.fetchone()[0])
        
        try:
            cursor.execute("select nivel from nivel where id_rango="+str(rangos)+" and id_usuario="+str(id_usuario)+";")
            actual=int(cursor.fetchone()[0])
            cursor.execute("update nivel set nivel="+str(actual+nivel)+" where id_rango="+str(rangos)+" and id_usuario="+str(id_usuario)+";")
            conexion.commit()
            #cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion) values("+str(rangos)+","+str(id_usuario)+","+str(nivel)+",'"+str(descripcion)+"');")
            cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion) values(%s,%s,%s,%s);",(str(rangos),str(id_usuario),str(nivel),str(descripcion),))
            conexion.commit()
            conexion.close()
        except TypeError:
            cursor.execute("insert into nivel(id_rango,id_usuario,nivel) values("+str(rangos)+","+str(id_usuario)+","+str(nivel)+");")
            conexion.commit()
            #cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion) values("+str(rangos)+","+str(id_usuario)+","+str(nivel)+",'"+str(descripcion)+"');")
            cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion) values(%s,%s,%s,%s);",(str(rangos),str(id_usuario),str(nivel),str(descripcion),))
            conexion.commit()
            conexion.close()
        

    rank=args[0]
    try:
        nivel=int(args[1])
        try:
            descripcion=args[2]
        except:
            descripcion='pudin'
    except:
        try:
            nivel=1
            descripcion=args[1]
        except:
            nivel=1
            descripcion='pudin'
    if (nivel<0):
        signo=False

    if (nivel>10 or nivel<-10):
        await ctx.send("El valor no es válido, debe estar en el intervalo [-10,10], {0.mention}".format(ctx.message.author))

    elif(rank=="Comedia" or rank=="comedia"):
        inserta(p1,1,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("¡Has subido un nivel de comedia!, {0.mention}".format(p1))
        elif(not signo):
            await ctx.send("No dio risa, {0.mention}".format(p1))
    
    elif(rank=="estupidez" or rank=="Estupidez"):
        inserta(p1,2,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Cada dia eres mas pendejo(a), {0.mention}".format(p1))
        elif(not signo):
            await ctx.send("Bueno un dia menos estupido(a), {0.mention}".format(p1))

    elif(rank=="puteria" or rank=="puteria"):
        inserta(p1,3,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Ahora eres mas puto(a) {0.mention}".format(p1))
        elif(not signo):
            await ctx.send("Se te ha quitado lo joto(a) {0.mention}".format(p1))
    
    elif(rank=="chismes" or rank=="chismes"):
        inserta(p1,4,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Deja de chismear, {0.mention}, has ganado puntos en vieja chismosa".format(p1))
        elif(not signo):
            await ctx.send("Aun asi en tu corazon eres una vieja chismosa, {0.mention}".format(p1))
        
    elif(rank=="amabilidad" or rank=="amabilidad"):
        inserta(p1,5,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Awwww, {0.mention}, cada dia eres mas amable".format(p1))
        elif(not signo):
            await ctx.send("Eres una persona horrible, {0.mention}, deja de serlo".format(p1))
    
    elif(rank=="amigos" or rank=="amigos"):
        inserta(p1,6,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Sucio vendeamigos, {0.mention}".format(p1))
        elif(not signo):
            await ctx.send("No te puedes quitar lo vende amigos, {0.mention}, +1 de estupidez".format(p1))
    
    elif(rank=="sordera" or rank=="sordera"):
        inserta(p1,7,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Lávate las orejas, {0.mention}, maldito(a) sordo(a)".format(p1))
        elif(not signo):
            await ctx.send("Ya te las lavaste, {0.mention}, maldito(a) (no tan) sordo(a) ".format(p1))
    
    elif(rank=="otaku" or rank=="otaku"):
        inserta(p1,8,nivel,descripcion,ctx)
        if(signo):
            await ctx.send("Cada día hueles peor, {0.mention}, maldito(a) otaku".format(p1))
        elif(not signo):
            await ctx.send("Ya te bañaste, {0.mention}".format(p1))

    elif(bool==True):
        usuario = ctx.message.author 
        await ctx.send('¿Sabes escribir?, +1 estupidez, {0.mention}, "por pendejo(a)"'.format(usuario))

@bot.command(name='ranking')
async def ranking(ctx,pal):
    bool=True
    def acomodar(stri):
        bool=False
        #Conexion a base de datos
        conexion=mysql.connect(host='localhost',user='root',passwd='',db='niveles2')
        cursor= conexion.cursor()
        cursor.execute("select u.nombre, n.nivel from nivel n inner join usuario u inner join rango r on n.id_rango=r.id_rango and u.id_usuario=n.id_usuario where r.id_rango="+str(stri)+" order by n.nivel desc;")
        temp=cursor.fetchall()
        return temp
    def formato(temp,stri):
        res= "Rank de "+stri
        embed = discord.Embed(
            title=res,
            description="Top de "+stri,
            color = discord.Color.green()
        )
        i=0
        for reng in temp:
            if(reng[1]!=0):
                temp2=(str(reng[0])+", Nivel: "+str(reng[1]))
                if(i==0):
                    embed.add_field(name=":first_place:",value=temp2,inline=True)
                elif(i==1):
                    embed.add_field(name=":second_place:",value=temp2,inline=True)
                elif(i==2):
                    embed.add_field(name=":third_place:",value=temp2,inline=True)
                else:
                    embed.add_field(name=str(i+1)+"° lugar:",value=temp2,inline=False)
                i+=1
        return embed
    nom=["Comedia","Estupidez","Putería","Vieja chismosa","Amabilidad","Vende amigos","Sordera","Otaku"]
    if(pal=="All" or pal=="all"):
        for i in range(1,9):
            temp=acomodar(i)
            print(temp)
            embed=formato(temp,nom[i-1])
            await ctx.send(embed=embed)
    elif(pal=="Comedia" or pal=="comedia"):
        temp=acomodar(1)
        print(temp)
        embed=formato(temp,"Comedia")
        await ctx.send(embed=embed)
    
    elif(pal=="estupidez" or pal=="Estupidez"):
        temp=acomodar(2)
        print(temp)
        embed=formato(temp,"estupidez")
        await ctx.send(embed=embed)

    elif(pal=="puteria" or pal=="puteria"):
        temp=acomodar(3)
        print(temp)
        embed=formato(temp,"puteria")
        await ctx.send(embed=embed)
    
    elif(pal=="chismes" or pal=="chismes"):
        temp=acomodar(4)
        print(temp)
        embed=formato(temp,"chismes")
        await ctx.send(embed=embed)
    
    elif(pal=="amabilidad" or pal=="amabilidad"):
        temp=acomodar(5)
        print(temp)
        embed=formato(temp,"Amabilidad")
        await ctx.send(embed=embed)
    
    elif(pal=="amigos" or pal=="amigos"):
        temp=acomodar(6)
        print(temp)
        embed=formato(temp,"Vende amigos")
        await ctx.send(embed=embed)

    elif(pal=="sordera" or pal=="sordera"):
        temp=acomodar(7)
        print(temp)
        embed=formato(temp,"Sordera")
        await ctx.send(embed=embed)
    
    elif(pal=="Otaku" or pal=="otaku"):
        temp=acomodar(8)
        print(temp)
        embed=formato(temp,"Otaku")
        await ctx.send(embed=embed)

    elif(bool==True):
        usuario = ctx.message.author
        await ctx.send('¿Sabes escribir?, +1 estupidez {0.mention} "por pendejo"'.format(usuario))    

@bot.command(name='log')
async def log(ctx,pal):
    bool=True
    def acomodar(stri):
        bool=False
        #Conexion a base de datos
        conexion=mysql.connect(host='localhost',user='root',passwd='',db='niveles2')
        cursor= conexion.cursor()
        if(stri==0):
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario order by l.fecha desc limit 30;")
        else:
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario where l.id_rango="+str(stri)+" order by l.fecha desc limit 30;")
        temp=cursor.fetchall()
        return temp
    def formato(temp,stri):
        res= "Log de: "+stri
        embed = discord.Embed(
            title=res,
            description="Log de "+stri,
            color = discord.Color.green()
        )
        for ren in temp:
            if(ren[3]!=0):
                temp2=(str(ren[0])+"|"+str(ren[1])+"|"+str(ren[2])+"|"+str(ren[3])+"|"+str(ren[4]))
                embed.add_field(name='Fecha    Rango    Usuario    Cambio    Descripción',value=temp2,inline=False)
        return embed
    if(pal=="All" or pal=="all"):
        temp=acomodar(0)
        embed=formato(temp,"Todo")
        await ctx.send(embed=embed)
    elif(pal=="Comedia" or pal=="comedia"):
        temp=acomodar(1)
        embed=formato(temp,"Comedia")
        await ctx.send(embed=embed)
    
    elif(pal=="estupidez" or pal=="Estupidez"):
        temp=acomodar(2)
        embed=formato(temp,"Estupidez")
        await ctx.send(embed=embed)

    elif(pal=="puteria" or pal=="puteria"):
        temp=acomodar(3)
        embed=formato(temp,"Putería")
        await ctx.send(embed=embed)
    
    elif(pal=="chismes" or pal=="chismes"):
        temp=acomodar(4)
        embed=formato(temp,"Chismes")
        await ctx.send(embed=embed)
    
    elif(pal=="amabilidad" or pal=="amabilidad"):
        temp=acomodar(5)
        print(temp)
        embed=formato(temp,"Amabilidad")
        await ctx.send(embed=embed)
    
    elif(pal=="amigos" or pal=="amigos"):
        temp=acomodar(6)
        embed=formato(temp,"Vende Amigos")
        await ctx.send(embed=embed)

    elif(pal=="sordera" or pal=="sordera"):
        temp=acomodar(7)
        embed=formato(temp,"Sordera")
        await ctx.send(embed=embed)
    
    elif(pal=="Otaku" or pal=="otaku"):
        temp=acomodar(8)
        embed=formato(temp,"Otaku")
        await ctx.send(embed=embed)

    elif(bool==True):
        usuario = ctx.message.author
        await ctx.send('¿Sabes escribir?, +1 estupidez {0.mention} "por pendejo"'.format(usuario))    

@bot.command(name='crash')
async def crash(ctx):
    await ctx.send("!p windows xp error sound")
    await play(ctx,'https://www.youtube.com/watch?v=0lhhrUuw2N8')


@bot.command(name='punishment')
async def punishment(ctx):
    await ctx.send("I've prepared a very special punishment for {0.mention}!".format(ctx.message.author))
    await play(ctx,'https://www.youtube.com/watch?v=edLOAiPSt5Q')

#!ayuda
@bot.command(name='ayuda')
async def ayuda(ctx):
    f =open('ayuda.txt')
    embed = discord.Embed(
        title=":customs: Help.me",
        description="La ayuda va en camino",
        color = discord.Color.red()
    )
    embed.add_field(name="Comandos basicos",value=f.read(),inline=True)
    f.close()
    await ctx.send(embed=embed)

#!version
@bot.command(name='version')

async def version(ctx):
    icon=str(ctx.guild.icon_url)

    f = open('novedades.txt','r')
    descripcion=f.read()
    f.close()
    embed = discord.Embed(
        title="Version" + " 0.1 " + " ALPHA",
        description = descripcion,
        color = discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name=":first_place: Inserts", value=10,inline=True)
    await ctx.send(embed=embed)

#!ayuda
@bot.command(name='pudin')
async def pudin(ctx):
    embed = discord.Embed(
        title=":customs: Pudín",
        description="Pudín",
        color = discord.Color.red()
    )
    embed.add_field(name="Pudín",value="Pudín\nPuhuhuhu\nPuhuhuhuhuhuhu",inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, url : str):
    global temp
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    print(str(ctx.author.voice.channel))
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(ctx.author.voice.channel))

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        await voiceChannel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    except discord.ClientException as e:
        print(e)
        if not (ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel):
            await ctx.send("El bot ya está conectado a otro canal. Intenta ejecutar desconectar al bot antes de llamarlo")
            return
        #voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        #await voice.move_to(ctx.author.voice.channel)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3")) 
    except youtube_dl.DownloadError as e:
        print(e)
        await ctx.send('Este bot no realiza búsquedas de palabras clave, solo reproduce videos dada una url')
    


@bot.command(name='leave')
async def leave(ctx):
    global temp
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        temp=False
    else:
        await ctx.send("The bot is not connected to a voice channel.")
@bot.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    
bot.run(token)