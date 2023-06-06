import customtkinter
from PIL import Image
from data import Data
from applicant import Applicant
from datetime import date
import re

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.file_path = 'applicants_data.csv'
        self.data = Data(self.file_path)  
        self.applicants_data = self.data.load_data() # stores data in a var as a list of Applicant objects  
        
        # Tk
        self.title('Kuwait Codes Summer Application')
        self.geometry('600x650')
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        customtkinter.set_default_color_theme('themes/kc.json') #theme path
       
        self.main_frame = customtkinter.CTkFrame(self,corner_radius=0)
        self.main_frame.grid(row=0,column=0,sticky='nsew')
        self.main_frame.grid_rowconfigure(7,weight=1)
        self.main_frame.grid_columnconfigure(2,weight=1)
        
        image_path = 'photos/kclogo.png' # image path

        self.logo_image = customtkinter.CTkImage(Image.open(image_path),size=(80,50))
        self.image_label = customtkinter.CTkLabel(self.main_frame,image=self.logo_image,text='')
        self.image_label.grid(row=0,column=2,padx=20,pady=20)

        self.gender_menu = customtkinter.CTkOptionMenu(self.main_frame,values=['Choose your gender','Male','Female'],
        command=self.gender_choice)
        self.gender_menu.grid(row=1,column=2,padx=20,pady=15)
        self.gender = None

        self.name_entry = customtkinter.CTkEntry(self.main_frame,placeholder_text='your name:',width=300,height=40)
        self.name_entry.grid(row=2,column=1,columnspan =2,padx=20,pady=10)

        self.email_entry = customtkinter.CTkEntry(self.main_frame,placeholder_text='your email:',width=300,height=40)
        self.email_entry.grid(row=3,column=1,columnspan =2,padx=20,pady=10)
        
        self.civilId_entry = customtkinter.CTkEntry(self.main_frame,placeholder_text='your civilId:',width=300,height=40)
        self.civilId_entry.grid(row=4,column=1,columnspan =2,padx=20,pady=10)

        self.output_textbox = customtkinter.CTkTextbox(self.main_frame,width=400)
        self.output_textbox.grid(row=5,column=1,columnspan =2,padx=20,pady=(10,5))
        self.output_textbox.insert("0.0", "Output:\n\n" )
        self.output_textbox.configure(state='disabled')

        self.next_btn = customtkinter.CTkButton(self.main_frame,text='Next',command=self.next_btn_listener)
        self.next_btn.grid(row=6,column=1,columnspan =2,padx=20,pady=20)

    def gender_choice(self,choice):
        self.gender = choice

    def next_btn_listener(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        civilId = self.civilId_entry.get().strip()
        gender = self.gender
        
        print('checking gender...\n')
        if self.gender == 'Choose your gender' or self.gender == None:
            print('gender error')
            output = 'Make sure to choose your gender!\n'
            self.display_output(output)
        else:
            output = ''
            if name == '' or email == '' or civilId == '':
                if name == '':
                    output += 'Make sure that you provided your name !\n'
                if email == '':
                    output += 'Make sure that you provided your email !\n'
                if civilId == '':
                    output += 'Make sure that you provided your civilId !\n'
                self.display_output(output)

            else:
                print('checking syntax...\n')
                if not self.check_email_syntax(email) or not self.check_civilID_syntax(civilId):
                    output = ''
                    if not self.check_email_syntax(email):
                        output += 'Make sure that you didn\'t miss type your email !\n'
                        print('email syntax error')
                    if not self.check_civilID_syntax(civilId):
                        output += 'Make sure that you didn\'t miss type your civilId !\n'
                        print('civilId syntax error')

                    self.display_output(output)

                else:
                    print('checking age...\n')
                    birth_date = self.get_birthdate(civilId)
                    age = self.get_age(birth_date)
                    if age > 18:
                        print('age > 18 error')
                        output = 'it\'s for kids only !\n'
                        self.display_output(output)
                    elif age < 13:
                        print('age > 13 error')
                        output = 'sorry kid, maybe next time\n'
                        self.display_output(output)
                    else:
                        if self.applicants_data == 'Programme running for the first time!':
                            print('running for the first time...\n')
                            self.applicants_data = self.data.create_data([name.title(),email,civilId,gender])
                        
                            self.message_based_on_gender()
                        else:
                            print('not running for the first time...\n')
                            if not self.check_if_email_is_used(email,self.applicants_data) and not self.check_if_civilID_is_used(civilId,self.applicants_data):
                                self.applicants_data.append(Applicant(name.title().strip(),email.strip(),civilId,gender))
                                self.data.update_file_data()
                                self.message_based_on_gender()
                            else:
                                output = ''
                                if self.check_if_email_is_used(email,self.applicants_data):
                                    print('Email used error')
                                    output += 'Email you provided is already used !\n'
                                

                                if self.check_if_civilID_is_used(civilId,self.applicants_data):
                                    print('CivilId used error')
                                    output += 'CivilId you provided is already used !\n'
                                
                                self.display_output(output)

        print('function ended.')

    def get_age(self,birthdate):
        today = date.today()
        today = str(today).split('-')
        current_year, current_month, current_day = int(today[0]), int(today[1]), int(today[2])

        birthdate = birthdate.split('-')
        birth_year, birth_month, birth_day = int(birthdate[0]), int(birthdate[1]), int(birthdate[2])

        age = current_year - birth_year

        if current_month < birth_month or (current_month == birth_month and current_day < birth_day):
            age -=1

        return age

    def check_email_syntax(self,email):
        pattern =  r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if re.match(pattern, email):
            return True
        else:
            return False

    def check_if_email_is_used(self,email,applicants_data):
        if email in [applicant.email for applicant in applicants_data]:
            return True
        else:
            return False

    def check_civilID_syntax(self,civilID):
        if len(civilID) == 12 and civilID[0] in ['2','3'] and int(civilID[3:5]) <= 12 and int(civilID[5:7]) <= 30:
            return True
        else:
            return False

    def check_if_civilID_is_used(self,civilID,applicants_data):
        if civilID in [applicant.civilId for applicant in applicants_data]:
            return True
        else:
            return False

    def get_birthdate(self,civilID):

        #NYYMMDD
        year = '19' + civilID[1:3] if civilID[0] == '2' else '20' + civilID[1:3]
        month = civilID[3:5]
        day = civilID[5:7]

        return f'{year}-{month}-{day}'

    def message_based_on_gender(self):
        if self.gender == 'Male':
            output = 'Thank you 💙\n'
        else:
            output = 'thank you 🩷\n'

        self.display_output(output)

    def display_output(self,output):

        self.output_textbox.configure(state='normal')
        self.output_textbox.delete('0.0','end')
        self.output_textbox.insert("0.0",text = 'Output:\n\n' + output)
        self.output_textbox.configure(state='disabled')        

if __name__ == '__main__':
    app = App()
    app.mainloop()