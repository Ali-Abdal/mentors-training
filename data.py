from applicant import Applicant
import csv

class Data:
    def __init__(self,file_path):
        self.file_path = file_path
        self.applicants_data = None

    # loads the data from the csv file and stores it in a list of Applicant objects
    def load_data(self):
        try:
            with open(self.file_path,'r') as fh:
                self.applicants_data = []

                try: 
                    next(fh)
                    for line in fh:
                        applicant_data = line.split(',')
                        name = applicant_data[0]
                        email = applicant_data[1]
                        civilId = applicant_data[2]
                        gender = applicant_data[3]

                        self.applicants_data.append(Applicant(name,email,civilId,gender.strip()))
                    print('Data has been uploaded!')
                    return self.applicants_data

                except StopIteration:
                    return 'Programme running for the first time!'

        except FileNotFoundError:
            print('Error check the file path !!!')

    def update_file_data(self):
        with open(self.file_path,'w') as fh:
            writer = csv.writer(fh)
            writer.writerow(['name','email','civilId','gender'])
            for applicant in self.applicants_data:
                writer.writerow([applicant.name,applicant.email,applicant.civilId,applicant.gender])
        print('File data has been updated!')

    def create_data(self,applicant_data):
        self.applicants_data = []
        name = applicant_data[0]
        email = applicant_data[1]
        civilId = applicant_data[2]
        gender = applicant_data[3]
        self.applicants_data.append(Applicant(name,email,civilId,gender))
        
        self.update_file_data()

        return self.applicants_data