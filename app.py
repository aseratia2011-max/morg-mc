from flask import Flask, jsonify
from mcstatus import MinecraftServer, BedrockServer
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # للسماح للموقع بالاتصال بالبايثون

# الإعدادات من الصور المرفقة
SERVER_IP = "morgmc.ddns.net"
PORT = 30033

@app.route('/api/status')
def get_server_status():
    status_data = {
        "online": False,
        "players_online": 0,
        "players_max": 0,
        "version": "Unknown",
        "latency": 0,
        "platform": ""
    }

    try:
        # محاولة الاتصال كـ Java أولاً (كما في الصورة morgmc.ddns.net:30033)
        try:
            java_server = MinecraftServer.lookup(f"{SERVER_IP}:{PORT}")
            status = java_server.status()
            status_data.update({
                "online": True,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "version": status.version.name,
                "latency": round(status.latency),
                "platform": "Java"
            })
        except:
            # إذا فشل الجافا، نحاول الاتصال كـ Bedrock (morgmc.ddns.net بورت 30033)
            bedrock_server = BedrockServer.lookup(f"{SERVER_IP}:{PORT}")
            status = bedrock_server.status()
            status_data.update({
                "online": True,
                "players_online": status.players_online,
                "players_max": status.players_max,
                "version": status.version.name,
                "latency": round(status.latency * 1000),
                "platform": "Bedrock"
            })

        return jsonify(status_data)

    except Exception as e:
        return jsonify({"online": False, "error": str(e)})

if __name__ == '__main__':
    print(f"Server Checker Running for {SERVER_IP}:{PORT}...")
    app.run(debug=True, port=5000)