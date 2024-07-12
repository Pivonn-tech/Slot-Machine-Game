from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret' # secret key for session management 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slot_machine.db' #sqlite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #Disable modification tracking


#Initializing the database 
db = SQLAlchemy(app)

#building the database 
class Player(db.Model):
  __tablename__ = 'player'
  __table_arg__ = {'extend_existing': True} 
  
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  balance = db.Column(db.Float, default=0.0)
  
class Transaction(db.Model):
  __tablename__ = 'transaction'
  __table_arg__ = {'extend_existing': True}
  
  id = db.Column(db.Integer, primary_key=True)
  player_id = db.Column(db.String, db.ForeignKey('player.id') , nullable=False)
  amount = db.Column(db.Float, nullable=False)
  transaction_type = db.Column(db.String(50), nullable=False) #deposit, bet, loss, win
  
with app.app_context():
  db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
      
    new_player = Player(username=username, password=password)
    db.session.add(new_player)
    db.session.commit()
      
    session['username'] = username #Log in the new user automatically 
    
      
    return redirect(url_for('home'))
     
  return render_template('register.html')
    
    
@app.route('/login', methods=['GET', 'POST']) 
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
      
    player = Player.query.filter_by(username=username).first()
    
    if player and player.password == password:
      session['username'] = username
      return redirect(url_for('home'))
    else:
      return render_template('login.html', message='Invalid username or password')

  return render_template('login.html')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('home'))

@app.route('/')
def home():
  if 'username' in session:
    username = session['username']
    player = Player.query.filter_by(username=username).first()
    return render_template('home.html', player=player)
  else:
    return render_template('welcome.html') 
    
    
import random
#Defining possible symbols and their probability
symbols = ["Flowers", "Spades", "Bell", "Cherry", "Oranges", "Plum", "Lemon"]

symbol_weights = [20, 20, 20, 20, 15, 10, 5]

def spin_reels():
  reel1 = random.choices(symbols, weights = symbol_weights)[0]
  reel2 = random.choices(symbols, weights = symbol_weights)[0]
  reel3 = random.choices(symbols, weights = symbol_weights)[0]
  return [reel1, reel2, reel3]
  
  
def calculate_winnings(reels):
  if reels[0] == reels[1] == reels[2]:
    if reels[0] == "Bell":
      return 100 #Jackpot
    elif reels[0] == "Cherry":
      return 50
    elif reels[0] == "Spades":
      return 20
    else:
      return 10
  elif reels[0]==reels[1] or reels[1]==reels[2]or reels[0]==reels[2]:
    return 5
  else:
    return 0
  
@app.route('/spin', methods=['GET', 'POST'])
def spin():
  if 'username' not in session:
      return redirect(url_for('login'))
    
  username = session['username']
  player = Player.query.filter_by(username=username).first()
    
  if player is None:
        return redirect(url_for('login'))

  reels = []
  winnings = 0
  message = ''
    
  if request.method == 'POST':
      bet_amount = float(request.form['bet'])

      if player.balance < bet_amount:
          message = 'Insufficient balance'
      else:
            # Deduct the bet amount
          player.balance -= bet_amount
          new_transaction = Transaction(player_id=player.id, amount=-bet_amount, transaction_type='bet')
          db.session.add(new_transaction)
          db.session.commit()

          # Spin the reels and calculate the winnings
          reels = spin_reels()
          winnings = calculate_winnings(reels)
          player.balance += winnings

          if winnings > 0:
              new_transaction = Transaction(player_id=player.id, amount=winnings, transaction_type='win')
          else:
              new_transaction = Transaction(player_id=player.id, amount=0, transaction_type='loss')

          db.session.add(new_transaction)
          db.session.commit()

  return render_template('spin.html', reels=reels, winnings=winnings, player=player, message=message)
  
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
  if 'username' not in session:
    return redirect(url_for('login'))
  
  if request.method == 'POST':
    amount = float(request.form['amount'])
    username = session['username']
    player = Player.query.filter_by(username=username).first()
    
    player.balance += amount
    new_transaction = Transaction(player_id=player.id,amount =amount, transaction_type='deposit')
    
    db.session.add(new_transaction )
    db.session.commit() 
    
    return redirect(url_for('home'))
  
  return render_template('deposit.html')
  
  
if __name__ == '__main__':
  app.run(debug=True)
  
  