from flask import Flask
from flask_mail import Mail
from flask import render_template

import gspread
from oauth2client.service_account import ServiceAccountCredentials


from datetime import datetime

from utils import reviewer, Candidat


app = Flask(__name__)

# Google Sheets API Setup and connecting to sheet
#added the credentials file to .gitignore to not push it to my github

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",                                                            ["https://spreadsheets.google.com/feeds",                                                               "https://www.googleapis.com/auth/spreadsheets",                                                        "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)

#open the sheet by the name given to it on your drive
gsheet = client.open("Candidats_data").sheet1

MAIL_USERNAME = "user@gmail.com"
MAIL_PASSWORD = "****"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME']=MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


        

@app.route('/')
def api_work():
    cols = gsheet.col_values(1)
    review= ""

    for i in range(len(cols)-1):
        #redefining now for every row to be seconde precise
        now = datetime.now()
        #first row is for the columns headers
        row = gsheet.row_values(i+2)
        #since our columns names are defined with spaces we can't use the autofill method from the dictionnaire gsheet.get_all_records
        if len(row)<6:
            for i in range(0,6-len(row)):
                row.append('')
        #a row is a list of cell values that will be passed as candidat constructor parametres
        candidat= Candidat(*row)
        
        
        #asserting each candidat cinstraints, this function will return the error message with the candidat ID if something is wrong and the candidat object if everything goes well
        candidat= candidat.candidature_constraints()

        #depending on the return of constraints test we we detect an irroned row
        if (type(candidat)==str):
            review= review + candidat + '\n'
        # if the row is well filled the right function is called depending on the row condition
        else:
            if(candidat.Status=="Applied"):
                candidat.test_sender(now,mail,gsheet)



            elif (   (candidat.Status== "Online Test Sent")    and    ((now- datetime.strptime(candidat.Mail_Sent, '%d/%m/%Y %H:%M:%S')).days >= 7)   and   ( candidat.Test_Score=='' )  ):
                candidat.reminder(now,mail,gsheet)

        
            elif(  candidat.Status == "Submitted Test" ):
                if (candidat.succees_test()== True):
                    candidat.interviewer(now,mail,gsheet)
                else:
                    candidat.refuser(now,mail,gsheet) 
    # costumized review message after all rows have been checked
    # iven if some rows present problems the rest of the rows will be handeled
    return render_template('affichage.html', title='Your Auto-Recrutor', view=reviewer(review,mail))
if __name__ == "__main__":
    app.run()
