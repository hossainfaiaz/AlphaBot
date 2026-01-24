from flask import Flask, render_template, request
#import AlphaBot
import AlphaBot
import time


bot = AlphaBot.AlphaBot()
app = Flask(__name__)
bot.stop()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == 'POST':
        request.form.get('command')
        if request.form.get('command') == 'a':
            bot.left()
            return render_template('index.html')
        if request.form.get('command') == 'w':
            bot.forward()
            return render_template('index.html')
        if request.form.get('command') == 's':
            bot.backward()
            return render_template('index.html')
        if request.form.get('command') == 'd':
            bot.right()
            return render_template('index.html')
        else:
            bot.stop()
            return render_template('index.html')
        
    else: return render_template('index.html')

""" if __name__ == "__main__":
    app.run(debug=False) """


if __name__ == '__main__':
    # Change host to your desired IP or '0.0.0.0' for all interfaces
    app.run(host='192.168.1.114', port=5005, debug=False)

    #app.run(host='192.168.1.114', port=5005, debug=True)