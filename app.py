from flask import Flask, jsonify
from mcstatus import JavaServer, BedrockServer
from flask_cors import CORS
import sys

app = Flask(__name__)
# السماح للاتصال من أي مصدر (حل مشكلة CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# إعدادات السيرفر
SERVER_IP = "morgmc.ddns.net"
SERVER_PORT = 30033

@app.route('/api/status', methods=['GET'])
def get_server_status():
    print(f"--> جاري فحص السيرفر: {SERVER_IP}:{SERVER_PORT}...", file=sys.stderr)
    
    response_data = {
        "online": False,
        "players_online": 0,
        "players_max": 0,
        "latency": 0,
        "version": "Unknown",
        "type": "Offline"
    }

    # المحاولة الأولى: اتصال Bedrock (الأكثر احتمالاً لهذا البورت)
    try:
        print("   [1] محاولة اتصال Bedrock...", file=sys.stderr)
        server = BedrockServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
        status = server.status()
        
        response_data = {
            "online": True,
            "players_online": status.players_online,
            "players_max": status.players_max,
            "latency": round(status.latency * 1000), # تحويل للـ ms
            "version": status.version.name,
            "type": "Bedrock"
        }
        print("   ✓ تم الاتصال بنجاح (Bedrock)!", file=sys.stderr)
        return jsonify(response_data)

    except Exception as e_bedrock:
        print(f"   X فشل Bedrock: {e_bedrock}", file=sys.stderr)

    # المحاولة الثانية: اتصال Java (في حال كان سيرفر جافا ببورت مخصص)
    try:
        print("   [2] محاولة اتصال Java...", file=sys.stderr)
        server = JavaServer.lookup(f"{SERVER_IP}:{SERVER_PORT}")
        status = server.status()
        
        response_data = {
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "latency": round(status.latency),
            "version": status.version.name,
            "type": "Java"
        }
        print("   ✓ تم الاتصال بنجاح (Java)!", file=sys.stderr)
        return jsonify(response_data)

    except Exception as e_java:
        print(f"   X فشل Java: {e_java}", file=sys.stderr)

    # إذا فشل الاثنين
    print("--> السيرفر يبدو مغلقاً أو العنوان خاطئ.", file=sys.stderr)
    return jsonify(response_data)

if __name__ == '__main__':
    print("=========================================")
    print(f"Server Monitor Running on port 5000")
    print(f"Targeting: {SERVER_IP}:{SERVER_PORT}")
    print("=========================================")
    app.run(debug=True, port=5000)