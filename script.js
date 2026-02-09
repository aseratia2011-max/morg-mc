async function fetchServerStatus() {
        // نستخدم 127.0.0.1 لأن السيرفر يعمل على جهازك الحالي
        const API_URL = "http://127.0.0.1:5000/api/status";
        
        statusText.innerText = "جاري الاتصال...";
        statusDot.className = "dot loading";

        try {
            const response = await fetch(API_URL);
            
            // تحقق إذا كان هناك خطأ في الاتصال بالسيرفر المحلي نفسه
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Server Data:", data); // طباعة البيانات في الكونسول للتأكد

            if (data.online) {
                // السيرفر يعمل
                statusText.innerText = "Online (" + data.type + ")"; // يظهر نوع السيرفر
                statusText.style.color = "#2ecc71";
                statusDot.className = "dot online";
                
                onlineSpan.innerText = data.players_online;
                maxSpan.innerText = data.players_max;
                
                pingStats.style.display = "block";
                pingValue.innerText = data.latency;

                updatePlayerListMessage(data.players_online);
            } else {
                // السيرفر مغلق (لكن الاتصال بالبايثون نجح)
                throw new Error("Server is Offline");
            }

        } catch (error) {
            console.error("Error details:", error);
            statusText.innerText = "Offline";
            statusText.style.color = "#e74c3c";
            statusDot.className = "dot offline";
            onlineSpan.innerText = "--";
            maxSpan.innerText = "--";
            pingStats.style.display = "none";
            
            playersContainer.innerHTML = '<p style="text-align:center; color:#e74c3c;">السيرفر غير متصل</p>';
        }
    }