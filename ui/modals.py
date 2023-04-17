import discord
import datetime
from sql import *
import random
from config import *
from buttons import *

class inviteFormModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(
            title="Анкета",
            custom_id="invite_form_modal",
            timeout=None
        )
        self.add_item(item=discord.ui.InputText(
            label="Ваш ник",
            placeholder="Player1056",
            custom_id="formNickname",
            style=discord.InputTextStyle.short
        ))
        self.add_item(item=discord.ui.InputText(
            label="Ваш пол",
            placeholder="жен|муж|другое",
            custom_id="formGender",
            style=discord.InputTextStyle.short
        ))
        self.add_item(item=discord.ui.InputText(
            label="Причина выбора города",
            placeholder="ну город типа крутой, и там ну я эта...",
            custom_id="formReason",
            style=discord.InputTextStyle.singleline
        ))
        self.add_item(item=discord.ui.InputText(
            label="Готовы ли вы работать на благо города?",
            placeholder="ну да я же заявку то подал_а...",
            custom_id="formMotivation",
            style=discord.InputTextStyle.singleline
        ))
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        id = random.randint(10000, 99999)
        nickname = self.children[0].value
        gender = self.children[1].value.lower()
        reason = self.children[2].value
        motivation = self.children[3].value
        channel = interaction.guild.get_channel(form_channel)
        pronous = "подал_а"
        if "жен" in gender:
            pronous = "подала"
        if "муж" in gender:
            pronous = "подал"
        embed = discord.Embed(
            title=f"{interaction.user.display_name} {pronous} заявку в город!", 
            description=f"Никнейм: {nickname}\nПол: {gender.capitalize()}\nПричина выбора: {reason.capitalize()}\nМотивация: {motivation.capitalize()}",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        message = await interaction.message.thread.send(embed=embed)
        embed = discord.Embed(
            title=f"Заявка от {interaction.user.display_name} @{id}", 
            description=f"Никнейм: {nickname}\nПол: {gender.capitalize()}\nПричина выбора: {reason.capitalize()}\nМотивация: {motivation.capitalize()}",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await channel.send(embed=embed, view=acceptFormButton())
        new_form(id, interaction.user.id, nickname, gender, reason, motivation, message.id)
        interaction.response.is_done()

class reportWorkModal(discord.ui.Modal):
    def __init__(self, role, message: discord.Message) -> None:
        super().__init__(
            title="Отчёт", 
            custom_id="report_work_modal", 
            timeout = None
        )
        self.add_item(item=discord.ui.InputText(
            label="Описание",
            placeholder="Опишите что сделали...",
            style=discord.InputTextStyle.paragraph
        ))
        self.type = role
        self.message = message

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        k = {
            resourcer_role: report_channel_resource,
            builder_role: report_channel_builder,
            warehouser_role: report_channel_warehouser
        }
        r = {
            resourcer_role: super_resourcer_role,
            builder_role: super_builder_role,
            warehouser_role: super_resourcer_role
        }
        channel = interaction.guild.get_channel(k[self.type])
        embed = discord.Embed(
            title=f"Отчет от {interaction.user.display_name}",
            description=self.children[0].value + "\n\n" + self.message.jump_url,
            color=discord.Color.green()
        )
        await channel.send(content=f"||{interaction.guild.get_role(r[self.type]).mention}||", embed=embed)
        interaction.response.is_done()

class newWorkModal(discord.ui.Modal):
    def __init__(self, type) -> None:
        super().__init__(
            title="Создать задание",
            custom_id="new_work_modal",
            timeout=None
        )
        self.type = type
        self.add_item(item=discord.ui.InputText(
            label="Максимальное количество рабочих (0 без макс)",
            placeholder="0",
            value=0,
            style=discord.InputTextStyle.short
        ))
        self.add_item(item=discord.ui.InputText(
            label="Задание",
            placeholder="Сделать это и то...",
            style=discord.InputTextStyle.paragraph
        ))
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        role = None
        if self.type.lower() == "ресурсер": role = interaction.guild.get_role(resourcer_role)
        if self.type.lower() == "складёр": role = interaction.guild.get_role(warehouser_role)
        if self.type.lower() == "строитель": role = interaction.guild.get_role(builder_role)
        embed = discord.Embed(
            title=f"Задание для @{self.type.capitalize()}!",
            description=self.children[1].value,
            color=discord.Color.red()
        )
        max_worker = self.children[0].value
        if max_worker == "0": max_worker = len(role.members)
        embed.add_field(name="Количество рабочих", value=f"0/{max_worker}")
        embed.set_footer(icon_url=interaction.user.display_avatar, text=interaction.user.display_name)
        message = await interaction.channel.send(content=f"||{role.mention}||", embed=embed, view=newWorkButton())
        new_work(message.id, role.id, self.children[1].value, 0, self.children[0].value)
        interaction.response.is_done()
        
class newNewsArticleModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="Создать запись",
            custom_id="new_article_news_modal",
            timeout=None
        )
        self.add_item(item=discord.ui.InputText(
            label="Заголовок",
            placeholder="ШОК?!?!? ГРИФАНУЛИ ГОРОД",
            custom_id="title_article"
        ))
        self.add_item(item=discord.ui.InputText(
            label="Текст новости",
            placeholder="сломали кнопку...",
            custom_id="description_article",
            style=discord.InputTextStyle.paragraph,
            max_length=2000
        ))
        self.add_item(item=discord.ui.InputText(
            label="URL картинки к новости (если есть)",
            custom_id="img_article",
            max_length=4000,
            required=False
        ))
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.green())
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        if self.children[2].value != "":
            embed.set_image(url=self.children[2].value)
        embed.timestamp = datetime.datetime.now()
        channel = interaction.guild.get_channel(article_channel)
        await channel.send(embed=embed)
        interaction.response.is_done()