#Prueba de conexión con la base de datos
import mysql.connector as mysql
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

conexion=mysql.connect(host='localhost',user='root',passwd='',db='niveles2')
operacion = conexion.cursor()
operacion.execute( "SELECT * FROM nivel" )