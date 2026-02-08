from flask import Flask, jsonify
from mcstatus import BedrockServer
from flask_cors import CORS

app = Flask(__name__)
# السماح للموقع بالاتصال بهذا السيرفر
CORS(app)

# إعدادات السيرفر
SERVER_IP = "mormc.ddns.net"
SERVER_PORT = 30033

@app.route('/api/status')
def get_server_status():
    try:
        # الاتصال بسيرفر بيدروك
        server = BedrockServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
        status = server.status()
        
        # محاولة جلب أسماء اللاعبين (قد لا تظهر في بيدروك دائماً حسب إعدادات السيرفر)
        # في بيدروك غالباً يعود العدد فقط، لكن سنحاول
        return jsonify({
            "online": True,
            "players_online": status.players_online,
            "players_max": status.players_max,
            "motd": status.motd,
            "latency": round(status.latency * 1000) # البينغ
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "online": False,
            "error": "Server Offline"
        })

if __name__ == '__main__':
    # تشغيل السيرفر المحلي
    print("Backend is running...")
    app.run(debug=True, port=5000)