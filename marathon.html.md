```
<!DOCTYPE html>
<html lang="ja">

```
```
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>50km Challenge</title>
    <!-- iOS用の設定: アプリのように見せる -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="50kmラン">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .progress-ring { transition: stroke-dashoffset 0.35s; transform: rotate(-90deg); transform-origin: 50% 50%; }
        body { 
            background-color: #f8fafc; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        /* アプリ風の全画面表示調整 */
        .safe-area-top { padding-top: env(safe-area-inset-top); }
    </style>
</head>
<body class="p-4 pb-20 safe-area-top">
    <div class="max-w-md mx-auto space-y-6">
        <!-- Header -->
        <header class="text-center py-4">
            <h1 class="text-2xl font-bold text-slate-800">50km Challenge</h1>
            <p id="currentDayText" class="text-slate-500 text-sm">目標達成まであと少し！</p>
        </header>

        <!-- Progress Card -->
        <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-lg font-semibold text-slate-700">進捗状況</h2>
                <span id="percentageText" class="text-blue-600 font-bold text-xl">0%</span>
            </div>
            <div class="relative flex justify-center items-center">
                <svg class="w-48 h-48">
                    <circle class="text-slate-100" stroke-width="12" stroke="currentColor" fill="transparent" r="80" cx="96" cy="96" />
                    <circle id="progressCircle" class="text-blue-500 progress-ring" stroke-width="12" stroke-dasharray="502.6" stroke-dashoffset="502.6" stroke-linecap="round" stroke="currentColor" fill="transparent" r="80" cx="96" cy="96" />
                </svg>
                <div class="absolute text-center">
                    <span id="totalDist" class="text-3xl font-bold text-slate-800">0.0</span>
                    <span class="text-slate-500"> / 50km</span>
                </div>
            </div>
            <div class="mt-4 text-center">
                <button onclick="resetData()" class="text-xs text-slate-400 underline">データをリセット</button>
            </div>
        </div>

        <!-- Log Entry -->
        <div class="bg-white rounded-3xl p-6 shadow-sm border border-slate-100">
            <h2 class="text-lg font-semibold text-slate-700 mb-4">本日のラン記録 (km)</h2>
            <div class="flex gap-2">
                <input type="number" id="distInput" inputmode="decimal" placeholder="0.0" step="0.1" class="flex-1 bg-slate-50 border-none rounded-2xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none text-lg">
                <button onclick="addLog()" class="bg-blue-600 text-white px-6 py-3 rounded-2xl font-bold active:scale-95 transition-transform">記録</button>
            </div>
        </div>

        <!-- AI Coaching Section -->
        <div class="bg-indigo-900 rounded-3xl p-6 shadow-lg text-white">
            <div class="flex items-center gap-2 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <h2 class="text-lg font-semibold">AIコーチ & Python相談</h2>
            </div>
            <div id="aiChat" class="text-indigo-100 text-sm mb-4 min-h-[60px] leading-relaxed italic">
                「お疲れ様です！今日のランニングやPython学習について教えてください。」
            </div>
            <div class="flex gap-2">
                <input type="text" id="aiInput" placeholder="メッセージを入力..." class="flex-1 bg-indigo-800 border-none rounded-xl px-4 py-2 text-sm focus:ring-1 focus:ring-indigo-400 outline-none placeholder-indigo-400">
                <button onclick="askAI()" id="aiBtn" class="bg-indigo-500 hover:bg-indigo-400 px-4 py-2 rounded-xl text-sm font-bold transition-colors">送信</button>
            </div>
        </div>
    </div>

    <script>
        let totalDistance = parseFloat(localStorage.getItem('marathon_total')) || 0;
        const targetDistance = 50;
        const apiKey = ""; 

        // 初期表示
        window.onload = updateUI;

        function updateUI() {
            document.getElementById('totalDist').innerText = totalDistance.toFixed(1);
            const percentage = Math.min((totalDistance / targetDistance) * 100, 100);
            document.getElementById('percentageText').innerText = Math.round(percentage) + '%';
            
            const circle = document.getElementById('progressCircle');
            const radius = 80;
            const circumference = 2 * Math.PI * radius;
            const offset = circumference - (percentage / 100) * circumference;
            circle.style.strokeDashoffset = offset;

            // データの保存
            localStorage.setItem('marathon_total', totalDistance);
        }

        function addLog() {
            const input = document.getElementById('distInput');
            const val = parseFloat(input.value);
            if (!isNaN(val) && val > 0) {
                totalDistance += val;
                updateUI();
                input.value = '';
                document.getElementById('aiChat').innerText = `素晴らしい！記録しました。あと ${(targetDistance - totalDistance).toFixed(1)}km です。`;
            }
        }

        function resetData() {
            if (confirm("記録をリセットしますか？")) {
                totalDistance = 0;
                localStorage.removeItem('marathon_total');
                updateUI();
            }
        }

        async function askAI() {
            const input = document.getElementById('aiInput');
            const btn = document.getElementById('aiBtn');
            const chat = document.getElementById('aiChat');
            const prompt = input.value;

            if (!prompt) return;

            btn.disabled = true;
            input.disabled = true;
            chat.innerText = "考え中...";

            const systemInstruction = `あなたはプロのマラソンコーチ兼Python講師です。
            現在の進捗は ${totalDistance}km / 50km です。
            ユーザーの問いかけに、励ましやアドバイスを3行以内で伝えてください。
            Pythonの質問があれば、iPhoneのPythonistaアプリやPytoで使える短いコードを提示してください。`;

            try {
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], systemInstruction: { parts: [{ text: systemInstruction }] } })
                });
                const result = await response.json();
                chat.innerText = result.candidates?.[0]?.content?.parts?.[0]?.text || "もう一度お願いします。";
            } catch (error) {
                chat.innerText = "エラーが起きました。ネット接続を確認してください。";
            } finally {
                btn.disabled = false;
                input.disabled = false;
                input.value = '';
            }
        }
    </script>
</body>
</html>

```
