import time, datetime
import discord
import asyncio
from discord import Embed
from discord.commands import Option
from discord.ext import commands
from discord.flags import Intents

from sql import *
from ui.modals import newWorkModal
from ui.buttons import newWorkButton, workRoleButton, acceptFormButton, inviteFormButton, newNewsArticleButton
from config import *

bot = commands.Bot(intents=Intents.all())

@bot.event
async def on_ready():
    bot.add_view(inviteFormButton())
    bot.add_view(acceptFormButton())
    bot.add_view(workRoleButton())
    bot.add_view(newWorkButton())
    bot.add_view(newNewsArticleButton())
    print("Mama")

@bot.event
async def on_message(message: discord.Message):
    thread = get_thread(message.channel.id)
    reaction = get_reaction(message.channel.id)
    if thread:
        await message.create_thread(name=thread[1])
    if reaction:
        for i in reaction[1].split(","):
            await message.add_reaction(i)

@bot.slash_command(name="threadchannel")
@discord.default_permissions(manage_channels=True)
async def set_channel(interaction: discord.Interaction, channel: Option(discord.TextChannel, "Канал где будут создаваться ветки"), threadname: Option(str, "Название создаваемой ветки")):
    d = new_thread(channel.id, threadname)
    if d:
        await interaction.response.send_message("Успешно!", ephemeral=True)

@bot.slash_command(name="reactionchannel")
@discord.default_permissions(manage_channels=True)
async def set_channel(interaction: discord.Interaction, channel: Option(discord.TextChannel, "Канал где будут ставиться реакции"), emojis: Option(str, "Эмоции для реакции. Вида :example:,:example2:,✅")):
    d = new_reaction(channel.id, emojis)
    if d:
        await interaction.response.send_message("Успешно!", ephemeral=True) 

@bot.slash_command(name="deletethreadchannel")
@discord.default_permissions(manage_channels=True)
async def set_channel(interaction: discord.Interaction, channel: Option(discord.TextChannel, "Канал где будут создаваться ветки")):
    d = delete_thread(channel.id)
    if d:
        await interaction.response.send_message("Успешно!", ephemeral=True)

@bot.slash_command(name="deletereactionchannel")
@discord.default_permissions(manage_channels=True)
async def set_channel(interaction: discord.Interaction, channel: Option(discord.TextChannel, "Канал где будут ставиться реакции")):
    d = delete_reaction(channel.id)
    if d:
        await interaction.response.send_message("Успешно!", ephemeral=True) 

@bot.slash_command(name="work")
async def work_command(interaction: discord.Interaction, type: Option(str, "Профессия", choices=["Ресурсер", "Складёр", "Строитель"])):
    _d = False
    for r in interaction.user.roles:
        if r.id in [super_arhitect_role, super_builder_role, super_resourcer_role, mayor_role, depute_mayor_role, bun_role]:
            _d = True
    if _d:
        await interaction.response.send_modal(newWorkModal(type))

@bot.slash_command(name="invitemessage")
@discord.default_permissions(administrator=True)
async def invite_message_command(interaction: discord.Interaction):
    embed = Embed(
        title="Для того что вступить в город, вам нужно подать заявку", 
        description="Заполнив анкету и ждите результата!",
        color=discord.Color.green()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/793769528441962537/1090303961287884810/2023-03-17_19.55.13_2.png")
    message = await interaction.channel.send(embed=embed, view=inviteFormButton())
    await message.create_thread(name="Заявки")

@bot.slash_command(name="workrolemessage")
@discord.default_permissions(administrator=True)
async def work_role_message_command(interaction: discord.Interaction):
    embed = Embed(
        title="Попав в город вам нужно выбрать роль, чтобы быть полезным городу", 
        description=f"**Основные роли профессий:**\n👩‍💼 <@&{resourcer_role}>  - собирает ресурсы на постройки/фермы и т.д.\n👩‍💻 <@&{warehouser_role}>  -  следит за складом, сортировкой и порядком.\n👩‍🎨 <@&{architect_role}>  -  строит здания на тесте или в одиночном мире.\n👷‍♀️ <@&{builder_role}>  -  переносит здания с теста на основной сервер при помощи мода litematica.\n👩‍🔧 <@&{engineer_role}>  - строит механизмы, фермы для города.\n\n**Дополнительные роли профессий:**\n🎨 <@&{artist_role}> - строит или рисует арты.\n🍺 <@&{barman_role}> - работает в баре\n🍕 <@&{pizzaiolo_role}> - работает в пиццерии\n♣️ <@&{croupier_role}> - заведует игральным столом\n\n||У вас должна быть минимум одна основная роль!||",
        color=discord.Color.green()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/932701238397657129/1094378629955321866/wqHTs-AscNM.png")
    await interaction.channel.send(embed=embed, view=workRoleButton())

@bot.message_command(name="Список рабочих")
async def list_worker_message_command(interaction: discord.Interaction, message):
    work = get_work(message.id)
    members = []
    for i in str(work[5]).split("-"):
        if i != '':
            members.append(interaction.guild.get_member(int(i)))
    content = "\n".join([i.mention for i in members])
    await interaction.response.send_message(content=content, ephemeral=True)

@bot.slash_command(name="articlenewsmessage")
@discord.default_permissions(administrator=True)
async def invite_message_command(interaction: discord.Interaction):
    embed = Embed(
        title="Новость города", 
        description="Здесь вы можете опубликовать любую новость, она будет видна гостям нашего дс сервера!\nНо есть небольшие правила:\n> Запрещена клевета\n> Запрещено оскорбление города, жителей города, также относится к другим городам\n> Также действуют правила Poopland",
        color=discord.Color.green()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/793769528441962537/1097568236544983120/2023-04-16_17.34.21.png")
    await interaction.channel.send(embed=embed, view=newNewsArticleButton())

if __name__ == "__main__":
    bot.run(token)