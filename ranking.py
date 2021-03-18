import mysql.connector as mysql
import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import youtube_dl
import sys


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

#Prefijo del bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='%')
global temp
temp = False


def connectToSQL():
    conexion = mysql.connect(host='localhost',user='root',passwd='',db='niveles2')
    cursor = conexion.cursor(prepared=True)
    return conexion,cursor

@bot.command(name='change')
async def subir(ctx,p1:discord.Member,*args):
    bool = True
    signo = True
    #hola duarte
    def inserta(p1,rangos,nivel,descripcion,admin,ctx):
        conexion,cursor = connectToSQL()
        cursor.execute("select id_usuario from usuario where nombre='"+str(p1)+"' limit 1;")
        
        try:
            id_usuario = int(cursor.fetchone()[0])
            print(id_usuario)
        except TypeError as e:
            print(e)
            cursor.execute("insert into usuario(nombre) values('"+str(p1)+"');")
            conexion.commit()
            cursor.execute("select id_usuario from usuario where nombre='"+str(p1)+ "';")
            id_usuario = int(cursor.fetchone()[0])
        
        try:
            cursor.execute("select nivel from nivel where id_rango="+str(rangos)+" and id_usuario="+str(id_usuario)+";")
            actual = int(cursor.fetchone()[0])
            cursor.execute("update nivel set nivel="+str(actual+nivel)+" where id_rango="+str(rangos)+" and id_usuario="+str(id_usuario)+";")
            conexion.commit()
            cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion,id_admin) values(%s,%s,%s,%s,%s);",(str(rangos),str(id_usuario),str(nivel),str(descripcion),str(admin),))
            conexion.commit()
            conexion.close()
        except TypeError:
            cursor.execute("insert into nivel(id_rango,id_usuario,nivel) values("+str(rangos)+","+str(id_usuario)+","+str(nivel)+");")
            conexion.commit()
            cursor.execute("insert into log(id_rango,id_usuario,cambio,descripcion,id_admin) values(%s,%s,%s,%s,%s);",(str(rangos),str(id_usuario),str(nivel),str(descripcion),str(admin),))
            conexion.commit()
            conexion.close()
        
    def mensaje(id_rango, nivel):
        conexion,cursor=connectToSQL()
        cursor.execute("select parte1,parte2 from mensaje where id_rango=(%s);",(str(id_rango),))
        try:
            m1,m2=cursor.fetchone()
        except:
            m1="Has subido un nivel"
            m2="Has bajado un nivel"
        cursor.close()
        if nivel>0:
            return m1
        else:
            return m2

    rank = args[0]
    try:
        nivel = int(args[1])
        try:
            descripcion = args[2]
        except:
            await ctx.send("La descripcion es obligatoria, {0.mention}".format(ctx.message.author))
            return
    except:
        try:
            nivel = 1
            descripcion = args[1]
        except:
            await ctx.send("La descripcion es obligatoria, {0.mention}".format(ctx.message.author))
            return

    if (nivel<0):
        signo=False

    if (nivel>10 or nivel<-10):
        await ctx.send("El valor no es válido, debe estar en el intervalo [-10,10], {0.mention}".format(ctx.message.author))

    try:
        conexion,cursor = connectToSQL()
        cursor.execute("select count(id_rango),id_rango from rango where descripcion=(%s);",(rank.lower(),))
        auxiliar1,ran = cursor.fetchone()
        auxiliar1=int(auxiliar1)
        if auxiliar1==1:
            print(ran)
            print(auxiliar1)
            inserta(p1,ran,nivel,descripcion,ctx.message.author,ctx)
            men=mensaje(ran,nivel)
            if "|" in str(men):
                s1,s2=str(men).split("|")
                await ctx.send((str(s1)+", {0.mention}, "+str(s2)).format(p1))
            else:
                await ctx.send((str(men)+", {0.mention}").format(p1))
                        
        else:
            usuario = ctx.message.author 
            await ctx.send('¿Sabes escribir?, +1 estupidez, {0.mention}, "por pendejo(a)"'.format(usuario))
    except Exception as e:
        usuario = ctx.message.author 
        await ctx.send('Ha ocurrido un error {0.mention}, "intentelo mas tarde"'.format(usuario))
        print(e)


@bot.command(name = 'add', pass_context = True)
@has_permissions(administrator = True)
async def add(ctx,*args):
    nuevo = args[0]
    conexion,cursor = connectToSQL()
    cursor.execute("select count(descripcion) from rango where descripcion=(%s);",(str(nuevo),))
    aux = cursor.fetchone()[0]
    if (int(aux) != 0):
        usuario = ctx.message.author
        await ctx.send('Ese rango ya existe, {0.mention}'.format(usuario))
        return
    else:
        try:   
            parte1=args[1]
        except:
            await ctx.send('Se necesita ingresar un mensaje positivo y un mensaje negativo para el rango, {0.mention}'.format(ctx.message.author))
            return
        
        try:
            parte2=args[2]
        except:
            await ctx.send('Se necesita ingresar un mensaje positivo y un mensaje negativo para el rango, {0.mention}'.format(ctx.message.author))
            return
        print(str(parte1)+"    "+str(parte2))
        cursor.execute("insert into rango(descripcion) values(%s);",(str(nuevo),))
        conexion.commit()
        print("rangos")
        cursor.execute("select id_rango from rango order by id_rango desc limit 1;")
        n=cursor.fetchone()[0]
        cursor.execute("insert into mensaje(parte1,parte2,id_rango) values(%s,%s,%s);",(str(parte1),str(parte2),str(n),))
        print("mensajes")
        conexion.commit()
        await ctx.send('Rango insertado exitosamente, {0.mention}'.format(ctx.message.author))
        conexion.close()
        

@add.error
async def random_error_2(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "Lamentablemente {}, estas pendejo(a)!".format(ctx.message.author)
        await ctx.channel.send(text)


@bot.command(name = 'ranking')
async def ranking(ctx,pal):
    bool = True
    def acomodar(stri):
        bool = False
        conexion,cursor = connectToSQL()
        cursor.execute("select u.nombre, n.nivel from nivel n inner join usuario u inner join rango r on n.id_rango=r.id_rango and u.id_usuario=n.id_usuario where r.id_rango="+str(stri)+" order by n.nivel desc;")
        temp = cursor.fetchall()
        conexion.close()
        return temp
    def formato(temp,stri):
        res = "Rank de "+stri
        embed = discord.Embed(
            title = res,
            description ="Top de "+stri,
            color = discord.Color.green()
        )
        i = 0
        boolin = True
        for reng in temp:
            if(reng[1]!= 0):
                temp2 = (str(reng[0])+", Nivel: "+str(reng[1]))
                if(reng[1]>0):
                    if(i == 0):
                        embed.add_field(name=":first_place:",value=temp2,inline=True)
                    elif(i == 1):
                        embed.add_field(name=":second_place:",value=temp2,inline=True)
                    elif(i == 2):
                        embed.add_field(name=":third_place:",value=temp2,inline=True)
                    else:
                        embed.add_field(name=str(i+1)+"° lugar:",value=temp2,inline=False)
                else:
                    if(boolin == True):
                        boolin = False
                        embed.add_field(name="Niveles Negativos",value="\n\t .",inline=True)
                    embed.add_field(name=str(i+1)+"° lugar:",value=temp2,inline=False)
                i+=1
        return embed   
    try:
        if(pal.lower() == "all"):
            conexion,cursor = connectToSQL()
            cursor.execute("select id_rango,descripcion from rango")
            temp = cursor.fetchall()
            aux = ""
            for i in temp:
                temp3=acomodar(int(i[0]))
                aux=str(i[1]).replace("(","")
                aux=aux.replace("'","")
                aux=aux.replace(")","")
                embed=formato(temp3,aux)
                await ctx.send(embed=embed)
        else:
            conexion,cursor = connectToSQL()
            cursor.execute("select count(id_rango),id_rango from rango where descripcion=(%s);",(pal,))
            auxiliar1,ran = cursor.fetchone()
            conexion.close()
            auxiliar1 = int(auxiliar1)
            if auxiliar1 == 1:
                temp=acomodar(int(ran))
                print(temp)
                embed=formato(temp,pal)
                await ctx.send(embed=embed)
        
            elif bool == True:
                usuario = ctx.message.author 
                await ctx.send('¿Sabes escribir?, +1 estupidez, {0.mention}, "por subnormal"'.format(usuario))
    except Exception as e:
        usuario = ctx.message.author 
        await ctx.send('Ha ocurrido un error {0.mention}, "intentelo mas tarde"'.format(usuario))
        print(e)

@bot.command(name = 'log')
async def log(ctx,pal):
    bool=True
    def acomodar(stri):
        bool=False
        conexion,cursor = connectToSQL()
        if(stri==0):
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion,l.id_admin from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario order by l.fecha desc limit 30;")
        else:
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion,l.id_admin from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario where l.id_rango="+str(stri)+" order by l.fecha desc limit 30;")
        temp=cursor.fetchall()
        conexion.close()
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
                temp2=(str(ren[0])+"|"+str(ren[1])+"|"+str(ren[2])+"|"+str(ren[3])+"|"+str(ren[4])+"|"+str(ren[5]))
                embed.add_field(name='Fecha    Rango    Usuario    Cambio    Descripción    Admin',value=temp2,inline=False)
        return embed

    async def feo(stri):
        bool=False
        conexion,cursor = connectToSQL()
        if(stri==0):
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion,l.id_admin from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario order by l.fecha desc;")
        else:
            cursor.execute("select l.fecha,r.descripcion,u.nombre,l.cambio,l.descripcion,l.id_admin from log l inner join rango r inner join usuario u on r.id_rango=l.id_rango and u.id_usuario=l.id_usuario where l.id_rango="+str(stri)+" order by l.fecha desc limit 15;")
        temp=cursor.fetchall()     
        res=""
        for ren in temp:
            print(ren)
            await ctx.send(str(ren))
        return 


    try:
        if(pal == "all"):
            temp = acomodar(0)
            embed = formato(temp,"Todo")
            await ctx.send(embed = embed)
        elif pal == "pudaningon":
            await feo(0)
            
        else:
            conexion,cursor = connectToSQL()
            cursor.execute("select count(id_rango),id_rango from rango where descripcion=(%s);",(pal,))
            auxiliar1,ran = cursor.fetchone()
            conexion.close()
            auxiliar1 = int(auxiliar1)
            if auxiliar1 == 1:
                if(pal.lower() == "all"):
                    temp = acomodar(0)
                else:
                    temp = acomodar(int(ran))
                embed = formato(temp,pal)
                await ctx.send(embed = embed)
        
            elif bool == True:
                usuario = ctx.message.author 
                await ctx.send('¿Sabes escribir?, +1 estupidez, {0.mention}, "por pendejo(a)"'.format(usuario))
    except Exception as e:
        usuario = ctx.message.author 
        await ctx.send('Ha ocurrido un error {0.mention}, "intentelo mas tarde"'.format(usuario))
        print(e)

@bot.command(name='punishment')
async def punishment(ctx):
    await localsound(ctx,"sonidos/mono.mp3")

@bot.command(name='crash')
async def crash(ctx):
    await localsound(ctx,"sonidos/error.mp3")
    """
    global temp
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
    try:
        voice.play(discord.FFmpegPCMAudio("sonidos/error.mp3")) 
    except Exception as e:
        await ctx.send("Usted no deberia de ver este error, comuniquese con un administador inmediatamente "+e)
"""
async def localsound(ctx,logino):
    global temp
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
    try:
        voice.play(discord.FFmpegPCMAudio(logino)) 
    except Exception as e:
        await ctx.send("Usted no deberia de ver este error, comuniquese con un administador inmediatamente "+e)


#!ayuda
@bot.command(name='ayuda')
async def ayuda(ctx):
    f =open('texto/ayuda.txt')
    embed = discord.Embed(
        title=":customs: Help.me",
        description="La ayuda va en camino",
        color = discord.Color.red()
    )
    embed.add_field(name="Comandos basicos",value=f.read(),inline=True)
    f.close()
    conexion,cursor = connectToSQL()
    cursor.execute("select descripcion from rango;")
    temp = cursor.fetchall()
    conexion.close()
    newwe=" "
    for i in temp:
        print(i)
        aux=str(i).replace("(","")
        aux=aux.replace("'","")
        aux=aux.replace(")","")
        print(aux)
        newwe+="\n"+aux
    embed.add_field(name="Rangos aceptados",value=newwe,inline=True)
    await ctx.send(embed=embed)


#!version
@bot.command(name='version')

async def version(ctx):
    icon = str(ctx.guild.icon_url)

    f = open('texto/novedades.txt','r')
    descripcion = f.read()
    f.close()
    embed = discord.Embed(
        title = "Version" + " 3.0 " + "(not public)",
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
