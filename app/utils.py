
import re
from datetime import datetime
from flask_mail import Message

#this is the mail of the recrutor company (in our case datagram), the user of this app, it will be the sendor  to the candidats and the reciver of error and review
MAIL_USERNAME = "user@gmail.com"
MAIL_PASSWORD = "****"
#class candidat will have all atributes of columns and functionns to update and  mail sending epon a row
class Candidat:
    #a constructor containing all atributes
    def __init__( self, ID, Email, Project, Status,Mail_Sent,Test_Score):
        self.ID= ID
        self.Email=Email
        self.Project=Project
        self.Status= Status
        self.Mail_Sent=Mail_Sent
        self.Test_Score=Test_Score

  
    #asserting all error cases
    def candidature_constraints(self):
        #we make a statut list we neet the indexation for the order to test the Test score and mail sent existence

        projects=["name_1", "name_2", "name_3"]
        ordered_status=["Applied",
        "Online Test Sent",
        "Reminder Sent",
        "Submitted Test",  
        "Interview Mail Sent",
        "Refusal Mail Sent"]

        try:  
            #first constraint:ID, Email, Project and Status are required while Test Score is optional.
            assert( ('' not in (self.ID,self.Email,self.Project,self.Status)))

            #constraint2:Test Score will only appear starting from “Submitted Test”
            #constraint3: appears in the following format: “score/total”
            if(self.Test_Score==''):
                assert(ordered_status.index(self.Status)<=2)
            else:
                assert(len(self.Test_Score.split("/"))==2)
                assert(int(self.Test_Score.split("/")[1])- int(self.Test_Score.split("/")[0]) >=0)
                assert(ordered_status.index(self.Status)>2)


            #constraint4: Mail sent will only appear starting from “Online Test Sent”.
            assert((self.Mail_Sent!='') and (ordered_status.index(self.Status)>=1) or (self.Mail_Sent=='') and (ordered_status.index(self.Status)==0) )
            #all columns are filled with the right formats and values
            assert(self.Project in projects)
            assert(self.Status in ordered_status)
            assert((self.Mail_Sent=='') or (type(datetime.strptime(self.Mail_Sent, '%d/%m/%Y %H:%M:%S')== datetime)) )
            assert(bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", self.Email)))
            type(int(self.ID))==int
            return(self)
        except:
            #returning the erroned candidature's ID to make finding it easy
            return ("something is wrong with your sheetspread. please check row n°"+ str(self.ID))

    #self,mail and gsheet are passed as parameters that will be defined in the main  
    #for candidats with only application
    def test_sender(self,now,mail,gsheet):
        
        msg = Message('dont reply this mail, you have a test', sender = MAIL_USERNAME, recipients = [self.Email])
        msg.body = "Thank you for applying to "+self.Project+"."
        mail.send(msg)
        a= int(self.ID)+1
        gsheet.update_cell(a,4, 'Online Test Sent')
        gsheet.update_cell(a,5, now.strftime('%d/%m/%Y %H:%M:%S'))
    #for candidats with no score and mail sent for more than 7 days
    def reminder(self,now,mail,gsheet):
        a= int(self.ID)+1
        msg = Message('dont reply this mail, just a reminder ', sender = MAIL_USERNAME, recipients = [self.Email])
        msg.body = "You haven’t submitted your test. Everything okay?"
        mail.send(msg)
        gsheet.update_cell(a,4, 'Reminder Sent')
        gsheet.update_cell(a,5, now.strftime('%d/%m/%Y %H:%M:%S'))
    #if candidats.succeed_test()== false
    def refuser(self,now,mail,gsheet):
        a= int(self.ID)+1
   
        msg = Message('dont reply this mail', sender = MAIL_USERNAME, recipients = [self.Email])
        msg.body = "We are sorry to tell you that you did not pass the test."
        mail.send(msg)
        gsheet.update_cell(a,4, 'Refusal Mail Sent')
        gsheet.update_cell(a,5, now.strftime('%d/%m/%Y %H:%M:%S'))
        
    #if candidats.succeed_test()== true
    def interviewer(self,now,mail,gsheet):
        project_responsable={"name_1":"Alan Turing", "name_2":"Tim Berners-Lee", "name_3":"Linus Torvalds"}

        a= int(self.ID)+1
        msg = Message('dont reply this mail, good news!', sender = MAIL_USERNAME, recipients = [self.Email])
        msg.body = "Congratulations for passing the test. You’ll have an interview with: "+ project_responsable[self.Project]+"."
        mail.send(msg)
        gsheet.update_cell(a,5, now.strftime('%d/%m/%Y %H:%M:%S'))
        gsheet.update_cell(a,4, 'Interview Mail Sent')
    def succees_test(self):
        return((int(self.Test_Score.split("/")[1])/2) < (int(self.Test_Score.split("/")[0])))



# this is not a candidat methode it workes on the owner of the sreadsheet but stiln an util
#depending on review(erroned rows) it sends costumized message
def reviewer(review,mail):
        #costumized mail repending on review leghth, if it's emply, no error is detected
    if( review == "" ):
        msg = Message('Confirmation message from your auto-recrutor ', sender = MAIL_USERNAME, recipients = [MAIL_USERNAME])
        msg.body = "Just a Confirmation message: Auto Recrutor is doing great! Every thing is going well with your spreadsheet."
        mail.send(msg)

        return("Just a Confirmation message: Auto Recrutor is doing great! Every thing is going well with your spreadsheet.")
    else:
        msg = Message('Error message from your auto-recrutor', sender = MAIL_USERNAME, recipients = [MAIL_USERNAME])
        msg.body = review+"\n"+"as you can see here, some lines in your spreadsheed have erroned data, fixe it please to maintain your auto recrutor work as for the rest of your condidats don't worry, they are well handeled!"
        mail.send(msg)
        return("Oops! Something went wrong, please check your email for more information!")

