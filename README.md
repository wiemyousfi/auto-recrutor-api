# Auto_Recrutor

A minimal one route api app developed with [Flask](http://flask.pocoo.org/) framework. 

The main purpose is retrieving data from a Google sheet and updating it with an api web application with Flask, this includes

- connecting to a Google Sheets Spreadsheet on a Gmail account

- authorize to access the Google Sheet we want to modify from our API
 
- read and modify an entry row

- send mails

- Error Handling

- Template



For a tutorial of integrating the Google Sheets API With Python Flask, you can refer to [a tutorial on Creating a Google API service allowing drive and sheet](https://betterprogramming.pub/integrating-google-sheets-api-with-python-flask-987d48b7674e/).

Also if you have the 2 steps security in your google account security settings you need to disable it:

or allow less secured apps to acceed:


![](https://i.postimg.cc/FRPjwkHN/allow-less-secured-apps-to-access.png)





## How to Run

- Step 1: Make sure you have Python

- Step 2: Install the requirements: `pip install -r requirements.txt`

- Step 3: add your api key: credentials.json to the project and set your email address and password , mine have bean removed!

- Step 4: Go to this app's directory and run `python app.py`





## Details about This auto_recrutor App

There is only one route in this api app, it returns a message a costumised mail to the user plus the candidature handeling, the route returnes one template:

 this is a review page which can be accessed by route after the work on sheet and mail sending are done.
 
 
 
 
- **case1**:


![](https://i.postimg.cc/VLm7xngP/confirmaion.png)





- **case2**: 


![](https://i.postimg.cc/rpqjbrLY/error.png)










## Testing





**for  testing I used a randomly filled google sheet on my drive**



![](https://i.postimg.cc/wvrJT88m/cases.png)




**and TEMPMAILS**



![](https://i.postimg.cc/x8hL1rmZ/temp-mail.png)








## mail sending




-**candidat**


![](https://i.postimg.cc/G2JLq6dy/interv.png)


-**user(recrutor)**


![](https://i.postimg.cc/yxMSzm44/error-message.png)








## References

- http://flask.pocoo.org/


- https://betterprogramming.pub/integrating-google-sheets-api-with-python-flask-987d48b7674e/
