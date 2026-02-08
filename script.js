document.addEventListener('DOMContentLoaded', function() {
    
    const API_URL = "http://127.0.0.1:5000/api/status";
    
    // عناصر DOM التي سيتم تحديثها
    const onlineSpan = document.getElementById('online-players');
    const maxSpan = document.getElementById('max-players');
    const statusText = document.getElementById('status-text');
    const statusDot = document.querySelector('.status-indicator .dot');
    const pingStats = document.getElementById('ping-stats');
    const pingValue = document.getElementById('ping-value');
    const playersContainer = document.getElementById('players-container');

    // دالة جلب البيانات من البايثون
    async function fetchServerStatus() {
        try {
            const response = await fetch(API_URL);
            const data = await response.json();

            if (data.online) {
                // السيرفر يعمل
                statusText.innerText = "Online";
                statusText.style.color = "#2ecc71";
                statusDot.className = "dot online";
                
                onlineSpan.innerText = data.players_online;
                maxSpan.innerText = data.players_max;
                
                pingStats.style.display = "block";
                pingValue.innerText = data.latency;

                // تحديث قائمة اللاعبين
                // ملاحظة: بيدروك غالباً لا يرسل قائمة الأسماء، لكننا سنضع العدد الحقيقي
                updatePlayerListMessage(data.players_online);

            } else {
                throw new Error("Server Offline");
            }

        } catch (error) {
            console.error("Error fetching status:", error);
            statusText.innerText = "Offline";
            statusText.style.color = "#e74c3c";
            statusDot.className = "dot offline";
            onlineSpan.innerText = "0";
            maxSpan.innerText = "0";
            pingStats.style.display = "none";
            
            playersContainer.innerHTML = '<p style="text-align:center; color:#e74c3c;">السيرفر غير متصل</p>';
        }
    }

    // دالة مساعدة لعرض رسالة اللاعبين
    function updatePlayerListMessage(count) {
        if (count > 0) {
            playersContainer.innerHTML = `
                <div style="text-align:center; padding: 20px;">
                    <i class="fas fa-users" style="font-size: 2rem; color: var(--primary); margin-bottom:10px;"></i>
                    <p>يوجد حالياً <strong>${count}</strong> لاعبين في السيرفر.</p>
                    <p style="font-size:0.8rem; color:#888;">(قائمة الأسماء مخفية لخصوصية اللاعبين في بيدروك)</p>
                </div>
            `;
        } else {
            playersContainer.innerHTML = '<p style="text-align:center; color:#888; padding:20px;">لا يوجد لاعبين حالياً.</p>';
        }
    }

    // نسخ الآي بي
    window.copyIP = function() {
        const ipText = document.getElementById('ip-text').innerText;
        navigator.clipboard.writeText(ipText).then(() => {
            alert("تم نسخ الآي بي بنجاح: " + ipText);
        });
    }

    // تشغيل التحديث فوراً ثم كل 30 ثانية
    fetchServerStatus();
    setInterval(fetchServerStatus, 30000);
});