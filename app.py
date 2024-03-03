import customtkinter
from skills.skill_manager import Skill, get_all_skills
from functions import PrivateFunctions
import os
from PIL import Image
from main_ap import MainAP

class SideBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        self.__app = None
        self.grid(row=0, column=0, sticky="nsew")

        self.label = customtkinter.CTkLabel(self, text="PAC",
                                            compound="left", font=customtkinter.CTkFont(family = 'Ubuntu', size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_homemenu)
        self.home_button.grid(row=1, column=0, padx=20, pady=10)
        self.skill_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Skill",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_skillmenu)
        self.skill_button.grid(row=2, column=0, padx=20, pady=10)
        self.ap_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Personal Assistant",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command = master.select_apmenu)
        self.ap_button.grid(row=3, column=0, padx=20, pady=10)

class HomeMenu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.title = customtkinter.CTkLabel(self, text = "Personal Assistant Creator", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky = "W")
        self.insf = customtkinter.CTkFrame(self)
        self.insf.grid_columnconfigure(0, weight = 1)
        f = open('./instructions.txt', 'r')
        i = f.readlines()
        f.close()
        self.ins = customtkinter.CTkTextbox(self.insf, fg_color = "transparent", height = 2000, font = customtkinter.CTkFont('arial', size = 15))
        self.ins.insert("0.0", ''.join(i))
        self.ins.configure(state= "disabled")
        self.ins.grid(row=0, column=0, padx=5, pady=5, sticky = "NESW")
        self.insf.grid(row = 1, column = 0, padx = 30, pady = (10,10), sticky = "NESW")

class SkillMenu(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.save_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "save_ico.png")), size=(30, 30))
        self.export_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "export_ico.png")), size=(30, 30))
        self.delete_ico = customtkinter.CTkImage(Image.open(os.path.join(master.image_path, "delete_ico.png")), size=(30, 30))
        self.grid_columnconfigure(0, weight = 1)
        self.label = customtkinter.CTkLabel(self, text="Personal Assistant Skills", compound="left", anchor = "w", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky = "W")
        _skills: list[Skill] = get_all_skills()
        self.skills: list[SkillFrame] = []
        for i, skill in enumerate(_skills):
            self.skills.append(SkillFrame(self, skill.name, '\n'.join(skill.commands), skill.code, True, skill, i))
            self.skills[-1].grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
        
        self.more = customtkinter.CTkFrame(self)
        self.more.grid_columnconfigure(2, weight = 1)

        self.more_addbtn = customtkinter.CTkButton(self.more, text = "Add Skill", command = self.newskill)
        self.more_addbtn.grid(column = 0, row = 0, columnspan = 2, padx=10, pady=(10, 10), sticky = "WE")

        self.more_lib = customtkinter.StringVar(self.more, "", "libi")
        self.more_libe = customtkinter.CTkEntry(self.more, textvariable = self.more_lib)
        self.more_libb = customtkinter.CTkButton(self.more, text = "Install Lib", fg_color = "#2f2f2f", hover_color = "#222222", command = self.installlib)

        self.more_libe.grid(column = 0, row = 1, padx=10, pady=(10, 10), sticky = "W")
        self.more_libb.grid(column = 1, row = 1, padx=10, pady=(10, 10), sticky = "W")

        self.more.grid(column = 0, row = len(self.skills) + 1, padx = 30, pady = 10, sticky = "EW")

    def delete(self, idx: int):
        self.skills.pop(idx)
        self.reprint()
    
    def reprint(self):
        for i, skill in enumerate(self.skills):
            skill.grid_forget()
            skill.grid(column = 0, row = i+1, padx = 30, pady = 10, sticky = "EW")
    
    def newskill(self):
        __newskill = Skill("name", "my skill", "#Your Code")
        self.skills.append(SkillFrame(self, "name", "my skill", "#Your Code", False, __newskill, len(self.skills)))
        self.more.grid_forget()
        self.skills[-1].grid(column = 0, row = len(self.skills), padx = 30, pady = 10, sticky = "EW")
        self.more.grid(column = 0, row = len(self.skills) + 1, padx = 30, pady = 10, sticky = "EW")
    
    def installlib(self):
        installed = PrivateFunctions.install_lib(self.more_lib.get())
        print(f"Installed {self.more_lib.get()}" if installed else f"Not founded {self.more_lib.get()}")
        self.more_lib.set("")

class SkillFrame(customtkinter.CTkFrame):
    def __init__(self, master, name: str = "", commands: str = "", code: str = "#Your Code", saved:bool = True, skill: Skill = Skill, idx: int = 0):
        super().__init__(master)
        self.grid_columnconfigure((0), weight = 1)
        self.__name = customtkinter.StringVar(self, name, "name")
        self.__commands = commands
        self.__code = code
        self.__skill: Skill = skill
        self.__saved = saved
        self.__idx = idx
        self.name_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Skill Name", textvariable = self.__name)
        self.name_entry.grid(row=0, column=0, padx=10, pady=(10, 10), sticky = "W", columnspan = 4)
        self.commands_entry = customtkinter.CTkTextbox(self, height = 100)
        self.commands_entry.insert("0.0", self.__commands)
        self.commands_entry.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky = "EW", columnspan = 4)
        self.code_entry = customtkinter.CTkTextbox(self, height=300, )
        self.code_entry.insert("0.0", self.__code)
        font = self.code_entry.cget("font")
        tab_size = font.measure('    ')
        self.code_entry.configure(tabs = tab_size)
        self.code_entry.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky = "SEW", columnspan = 4)
        self.save_button = customtkinter.CTkButton(self, text = "", image = master.save_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save(True))
        self.export_button = customtkinter.CTkButton(self, text = "", image = master.export_ico, height = 30, width = 30, fg_color = "transparent", command = lambda: self.save())
        self.delete_button = customtkinter.CTkButton(self, text = "", image = master.delete_ico, height = 30, width = 30, fg_color = "transparent", hover_color = '#880000', command = lambda: self.delete())
        self.save_button.grid(row=0, column=1, padx=10, pady=(10, 10))
        self.export_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        self.delete_button.grid(row=0, column=3, padx=10, pady=(10, 10))

        self.name_entry.bind('<FocusOut>', lambda event: self.focusoutname())
        self.commands_entry.bind('<FocusOut>', lambda event: self.focusoutcommands())
        self.code_entry.bind('<FocusOut>', lambda event: self.focusoutcode())
        self.bind('<Button-1>', lambda event: self.focus_set())
    
    @property
    def name(self):
        return self.__name.get()
    @property
    def commands(self):
        self.__commands = self.commands_entry.get('0.0', 'end')
        return self.__commands
    @property
    def code(self):
        self.__code = self.code_entry.get('0.0', 'end')
        return self.__code
    
    def focusoutname(self):
        self.__skill.name = self.name
        self.__saved = False
    
    def focusoutcommands(self):
        self.__skill.commands = self.commands.split('\n')
        self.__saved = False

    def focusoutcode(self):
        self.__skill.code = self.code
        self.__saved = False
    
    def delete(self):
        self.__skill.delete()
        del self.__skill
        self.grid_forget()
        self.master.delete(self.__idx)
    
    def save(self, ot: bool = False):
        self.__skill.name = self.name
        self.__skill.commands = self.commands.split('\n')
        self.__skill.code = self.code
        self.__skill.toPy(ot)

class APMenu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self, text = "Personal Assistant in Console. Sorry.")
        self.label.grid(column = 0, row = 0)
        self.button = customtkinter.CTkButton(self, text = "Init a new Personal Assistant", command = self.newap)
        self.button.grid(column = 0, row = 1)
    
    def newap(self):
        ma = MainAP()
        ma.main()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.__app = None

        self.title("PAC")
        self.geometry("1280x720")
        self.minsize(1280,720)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "app/images")

        #SideBar 
        self.sidebar = SideBar(self)
        self.sidebar.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        #Menus
        self.home_frame = HomeMenu(self)
        self.skill_frame = SkillMenu(self)
        self.ap_frame = APMenu(self)

        self.select_homemenu()

    def select_menu(self, name):
        self.sidebar.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.sidebar.skill_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.sidebar.ap_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "skill":
            self.skill_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.skill_frame.grid_forget()
        if name == "ap":
            self.ap_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ap_frame.grid_forget()
    
    def select_homemenu(self):
        self.select_menu('home')
    def select_skillmenu(self):
        self.select_menu('skill')
    def select_apmenu(self):
        self.select_menu('ap')

app = App()
app.mainloop()