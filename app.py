from flask import Flask, render_template, request
from random import randint
app = Flask(__name__)

@app.route('/')
def student():
   return render_template('student.html')

def generate_password(minlen, maxlen, isLower, isUpper, isNumber, symbol_list):
   words = ["one", "two", "word", "doritos"]
   pwd = ""
   
   if (isNumber and len(symbol_list) > 0):
      maxlen -= 3
   elif (isNumber or len(symbol_list) == 0):
      maxlen -= 2

   while (len(pwd)-1 < minlen or len(pwd) < maxlen):
      pwd_index = randint(0, len(words)-1)
      next_word = words[pwd_index]
      if (len(pwd) + (len(next_word) + 1) > maxlen):
         break
      pwd += next_word + "-"
   pwd = pwd[:-1]

   if (isUpper and isLower):
      pwd.title()
   elif (isUpper):
      pwd.upper()
   elif (isLower):
      pwd.lower()

   if (isNumber or len(symbol_list) > 0):
      pwd += "-"
      if (len(symbol_list) > 0):
         pwd += symbol_list[randint(0, len(symbol_list)-1)]
      if (isNumber):
         pwd += str(randint(0, 9))

   return pwd
      
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      #get the int for min length
      pass_len_min = request.form["pass_len_min"]
      pass_len_min = int(pass_len_min)

      #get the int for max length
      pass_len_max = request.form["pass_len_max"]
      pass_len_max = int(pass_len_max)
            
      #get if lowercase is allowed
      if ("pass_lowercase" in request.form):
         isLower = request.form["pass_lowercase"]
         if (isLower == "on"):
            isLower = True
         else:
            isLower = False
      else:
         isLower = False

      #get if uppercase is allowed
      if ("pass_uppercase" in request.form):
         isUpper = request.form["pass_uppercase"]
         if (isUpper == "on"):
            isUpper = True
         else:
            isUpper = False
      else:
         isUpper = False

      #get if numbers are allowed
      if ("pass_number" in request.form):
         isNumber = request.form["pass_number"]
         if (isNumber == "on"):
            isNumber = True
         else:
            isNumber = False
      else:
         isNumber = False

      #get list of usable symbols
      symbol_list = request.form["pass_symbol"]
      if (len(symbol_list) > 0):
         symbol_list = list(symbol_list)

      password = generate_password(pass_len_min, pass_len_max, isLower, isUpper, isNumber, symbol_list)
      
      result = request.form
      return render_template("result.html", password = password, result=result)

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
