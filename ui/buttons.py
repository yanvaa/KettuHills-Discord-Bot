import discord
from sql import *
from config import *
from modals import inviteFormModal, reportWorkModal, newNewsArticleModal

class newWorkButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Завершить", custom_id="work_result", style=discord.ButtonStyle.green, row=2)
    async def button_callback1(self, button, interaction: discord.Interaction):
        _d = False
        for r in interaction.user.roles:
            if r.id in [super_arhitect_role, super_builder_role, super_resourcer_role, mayor_role, depute_mayor_role, bun_role]:
                _d = True
        if not _d:
            await interaction.response.send_message("Недостаточно прав!", ephemeral=True, delete_after=3)
            return False
        for i in self.children:
            i.disabled = True
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.green()
        await interaction.message.edit(content=interaction.message.content, embed=embed, view=self)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)
        
    @discord.ui.button(label="Присоединиться", custom_id="work_invite", style=discord.ButtonStyle.grey, row=1)
    async def button_callback2(self, button, interaction: discord.Interaction):
        work = get_work(interaction.message.id)
        if interaction.guild.get_role(int(work[1])) not in interaction.user.roles:
            await interaction.response.send_message("Недостаточно прав!", ephemeral=True, delete_after=3)
            return False
        if str(interaction.user.id) in work[5]:
            await interaction.response.send_message("Вы уже присоединились!", ephemeral=True, delete_after=3)
            return False
        if int(work[3]) + 1 == int(work[4]) and int(work[4]) != 0:
            button.disabled = True
        embed = interaction.message.embeds[0]
        max_worker = work[4]
        if work[4] == 0: max_worker = len(interaction.guild.get_role(int(work[1])).members)
        embed.clear_fields()
        embed.add_field(name="Количество рабочих", value=f"{int(work[3]) + 1}/{max_worker}")
        await interaction.message.edit(content=interaction.message.content, embed=embed, view=self)
        update_work(interaction.message.id, int(work[3]) + 1, work[5] + str(interaction.user.id) + "-")
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)
        
    @discord.ui.button(label="Отказаться", custom_id="work_invite_cancel", style=discord.ButtonStyle.red, row=1)
    async def button_callback3(self, button, interaction: discord.Interaction):
        work = get_work(interaction.message.id)
        if interaction.guild.get_role(int(work[1])) not in interaction.user.roles or str(interaction.user.id) not in work[5]:
            await interaction.response.send_message("Недостаточно прав!", ephemeral=True, delete_after=3)
            return False
        if int(work[3]) - 1 < int(work[4]) and int(work[4]) != 0:
            button.disabled = False
        embed = interaction.message.embeds[0]
        max_worker = work[4]
        if work[4] == 0: max_worker = len(interaction.guild.get_role(int(work[1])).members)
        embed.clear_fields()
        embed.add_field(name="Количество рабочих", value=f"{int(work[3]) - 1}/{max_worker}")
        update_work(interaction.message.id, int(work[3]) - 1, work[5].replace(str(interaction.user.id) + "-", ""))
        await interaction.message.edit(content=interaction.message.content, embed=embed, view=self)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="Отчет", custom_id="work_report", style=discord.ButtonStyle.green, row=1)
    async def button_callback4(self, button, interaction: discord.Interaction):
        work = get_work(interaction.message.id)
        if interaction.guild.get_role(int(work[1])) not in interaction.user.roles or str(interaction.user.id) not in work[5]:
            await interaction.response.send_message("Недостаточно прав!", ephemeral=True, delete_after=3)
            return False
        await interaction.response.send_modal(reportWorkModal(interaction.guild.get_role(int(work[1])).id, interaction.message))
        


class workRoleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="", custom_id="resourcerwork", style=discord.ButtonStyle.grey, emoji="👩‍💼")
    async def button_callback1(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(resourcer_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="warehouserwork", style=discord.ButtonStyle.grey, emoji="👩‍💻")
    async def button_callback2(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(warehouser_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="arhitectwork", style=discord.ButtonStyle.grey, emoji="👩‍🎨")
    async def button_callback3(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(architect_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="builderwork", style=discord.ButtonStyle.grey, emoji="👷‍♀️")
    async def button_callback4(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(builder_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="engineerwork", style=discord.ButtonStyle.grey, emoji="👩‍🔧")
    async def button_callback5(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(engineer_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="artistwork", style=discord.ButtonStyle.grey, emoji="🎨", row=2)
    async def button_callback6(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(artist_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="barmanwork", style=discord.ButtonStyle.grey, emoji="🍺", row=2)
    async def button_callback7(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(barman_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="pizzaiolowork", style=discord.ButtonStyle.grey, emoji="🍕", row=2)
    async def button_callback8(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(pizzaiolo_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

    @discord.ui.button(label="", custom_id="croupierowork", style=discord.ButtonStyle.grey, emoji="♣️", row=2)
    async def button_callback9(self, button, interaction: discord.Interaction):
        role = interaction.guild.get_role(croupier_role)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
        else:
            await interaction.user.add_roles(role)
        await interaction.response.send_message("Успешно!", ephemeral=True, delete_after=3)

class inviteFormButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Подать заявку", custom_id="inviteform", style=discord.ButtonStyle.grey, emoji="📑")
    async def button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(inviteFormModal())

class acceptFormButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def get_form_id(self, interaction: discord.Interaction):
        return int(interaction.message.embeds[0].title.split(" @")[1])

    @discord.ui.button(label="Принять", custom_id="acceptform", style=discord.ButtonStyle.green)
    async def accept_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        id = self.get_form_id(interaction)
        form = get_form(id)
        member = interaction.guild.get_member(form[1])
        role = interaction.guild.get_role(981603198399836206)
        gender_role = interaction.guild.get_role(other_role)
        emoji = "🥑"
        gender = form[3]
        if "жен" in gender:
            emoji = "🍓"
            gender_role = interaction.guild.get_role(woman_role)
        if "муж" in gender:
            emoji = "🍇"
            gender_role = interaction.guild.get_role(man_role)
        message = await interaction.guild.get_thread(thread_channel).fetch_message(form[6])
        embed = message.embeds[0]
        embed.set_footer(text="Принята", icon_url=interaction.user.display_avatar)
        await message.edit(embed=embed)
        await member.add_roles(role)
        await member.add_roles(gender_role)
        await member.edit(nick=f"{emoji}{form[2]}")
    @discord.ui.button(label="Отклонить", custom_id="cancelform", style=discord.ButtonStyle.red)
    async def cancel_button_callback(self, button, interaction: discord.Interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        id = self.get_form_id(interaction)
        form = get_form(id)
        message = await interaction.guild.get_thread(thread_channel).fetch_message(form[6])
        embed = message.embeds[0]
        embed.set_footer(text="Отклонена", icon_url=interaction.user.display_avatar)
        await message.edit(embed=embed)

class newNewsArticleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Создать запись", custom_id="newnewsarticle", style=discord.ButtonStyle.grey, emoji="📰")
    async def button_callback(self, button, interaction: discord.Interaction):
        if interaction.user.id in news_block_list:
            await interaction.response.send_message("Вы в черном списке!", ephemeral=True)
            return False
        await interaction.response.send_modal(newNewsArticleModal())