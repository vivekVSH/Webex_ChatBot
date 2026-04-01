from flask import Flask, jsonify
from bot import AutoReplyBot

app = Flask(__name__)
bot = AutoReplyBot()

@app.route('/start', methods=['POST'])
def start_bot():
    if bot.get_status() == 'Running':
        return jsonify({'status': 'already running'})
    bot.start()
    return jsonify({'status': 'started'})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot.stop()
    return jsonify({'status': 'stopped'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': bot.get_status(), 'last_text': bot.last_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
