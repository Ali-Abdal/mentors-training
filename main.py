from data import Data
from applicant import Applicant
from datetime import date
import re


def main():

    file_path = 'applicants_data.csv'
    data = Data(file_path)
    applicants_data = data.load_data()

    while True:
        name = input('What is your name?\n a:')
        email = input('What is your email?\n a:')
        gender = input('What is your gender?\n a:')
        civilId = input('What is your civilId\n a:')

        print('checking syntax...\n')
        if not check_email_syntax(email) or not check_civilID_syntax(civilId):
            if not check_email_syntax(email):
                print('Make sure that you didn\'t miss type your email!')
            if not check_civilID_syntax(civilId):
                print('Make sure that you didn\'t miss type your civilId')

        else:
            print('checking age...\n')
            birth_date = get_birthdate(civilId)
            age = get_age(birth_date)
            if age > 18:
                print('it\'s for kids only!')

            elif age < 13:
                print('sorry kid, maybe next time')
            
            else:
                if applicants_data == 'Programme running for the first time!':
                    print('running for the first time...\n')
                    applicants_data = data.create_data([name.title().strip(),email.strip(),civilId,gender])
                    
                    message_based_on_gender(gender)

                else:
                    print('not running for the first time...\n')
                    if not check_if_email_is_used(email,applicants_data) and not check_if_civilID_is_used(civilId,applicants_data):
                        applicants_data.append(Applicant(name.title().strip(),email.strip(),civilId,gender))
                        data.update_file_data()
                        message_based_on_gender(gender)
                    else:
                        if check_if_email_is_used(email,applicants_data):
                            print('Email your provided is already used!')

                        if check_if_civilID_is_used(civilId,applicants_data):
                            print('CivilId you provided is already used!')

        print('\n\nnew loop')

def get_age(birthdate):
    today = date.today()
    today = str(today).split('-')
    current_year, current_month, current_day = int(today[0]), int(today[1]), int(today[2])

    birthdate = birthdate.split('-')
    birth_year, birth_month, birth_day = int(birthdate[0]), int(birthdate[1]), int(birthdate[2])

    age = current_year - birth_year

    if current_month < birth_month or (current_month == birth_month and current_day < birth_day):
        age -=1

    return age

def check_email_syntax(email):
    pattern =  r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False

def check_if_email_is_used(email,applicants_data):
    if email in [applicant.email for applicant in applicants_data]:
        return True
    else:
        return False

def check_civilID_syntax(civilID):
    if len(civilID) == 12 and civilID[0] in ['2','3'] and int(civilID[3:5]) <= 12 and int(civilID[5:7]) <= 30:
        return True
    else:
        return False

def check_if_civilID_is_used(civilID,applicants_data):
    if civilID in [applicant.civilId for applicant in applicants_data]:
        return True
    else:
        return False

def get_birthdate(civilID):

    #NYYMMDD
    
    year = '19' + civilID[1:3] if civilID[0] == '2' else '20' + civilID[1:3]
    month = civilID[3:5]
    day = civilID[5:7]

    return f'{year}-{month}-{day}'

def message_based_on_gender(gender):
    if gender == 'Male':
        print('Male Blue')
    else:
        print('Female pink')

if __name__ == '__main__':
    main()