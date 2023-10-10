from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app1=Flask(__name__)

ENV='dev'

if ENV=='dev':
   app1.debug=True
   app1.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:arunima@localhost/lexus' 
else:
   app1.debug=False
   app1.config['SQLALCHEMY_DATABASE_URI']=''

app1.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app1)

class Feedback(db.Model):
   __tablename__= 'feedback'
   id=db.Column(db.Integer, primary_key=True)
   customer=db.Column(db.String(200),unique=True)
   dealer=db.Column(db.String(200))
   rating=db.Column(db.Integer)
   comments=db.Column(db.Text())

   #constructor
   def __init__(self,customer,dealer,rating,comments):
      self.customer=customer
      self.dealer=dealer
      self.rating=rating
      self.comments=comments

@app1.route('/')
def index():
    return render_template('index.html')

@app1.route('/submit', methods=['POST'])
def submit():
   if request.method=='POST':
      customer=request.form['customer']
      dealer=request.form['dealer']
      rating=request.form['rating']
      comments=request.form['comments']
      # print(customer, dealer, rating, comments)
      if customer == '' or dealer == '':
         return render_template('index.html',message='Please enter required fields')
      #customer does not exist
      if db.session.query(Feedback).filter(Feedback.customer==customer).count()==0:
         data=Feedback(customer,dealer,rating,comments)
         db.session.add(data)
         db.session.commit()
         send_mail(customer,dealer,rating,comments)
         return render_template('success.html')
      return render_template('index.html',message='You have already submitted the form')

if(__name__=="__main__") :
  app1.run(debug= True , port = 8000)