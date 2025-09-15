<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Satış Liderlik Tablosu</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN (Veri Görselleştirmesi için) -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome (Profil İkonları için) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Eski Neon Tema */
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #e0e0e0;
            position: relative;
            overflow-y: auto;
            overflow-x: hidden;
        }
        .abstract-shape {
            position: absolute;
            opacity: 0.3;
            filter: blur(80px);
            z-index: 0;
        }
        .shape-1 { top: 5%; left: 5%; width: 250px; height: 250px; background-color: #f72585; border-radius: 50%; animation: float 15s infinite ease-in-out; }
        .shape-2 { bottom: 10%; right: 15%; width: 200px; height: 200px; background-color: #4361ee; border-radius: 50%; animation: float 18s infinite reverse ease-in-out; }
        .shape-3 { top: 20%; right: 5%; width: 180px; height: 180px; background-color: #4895ef; border-radius: 40%; animation: float 17s infinite alternate-reverse ease-in-out; }
        .shape-4 { bottom: 25%; left: 10%; width: 220px; height: 220px; background-color: #4cc9f0; border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; animation: float 20s infinite alternate ease-in-out; }

        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }
        .main-content-wrapper {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 800px;
            margin-top: 20px;
            background-color: rgba(36, 36, 62, 0.9);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .leaderboard-container {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            width: 100%;
            text-align: center;
            color: #ffffff;
        }
        .leaderboard-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
            margin-top: 20px;
        }
        .leaderboard-table th, .leaderboard-table td {
            padding: 15px;
            text-align: left;
            border-radius: 10px;
            color: #e0e0e0;
            background-color: rgba(255, 255, 255, 0.1);
            border: none;
        }
        .leaderboard-table th {
            background-color: rgba(255, 255, 255, 0.2);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        .leaderboard-table tbody tr {
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out, background-color 0.3s;
            cursor: pointer;
        }
        .leaderboard-table tbody tr:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            background-color: rgba(255, 255, 255, 0.15);
        }
        .leaderboard-table td:first-child {
            font-weight: 700;
            text-align: center;
            width: 50px;
        }
        .logo-container {
            margin-bottom: 20px;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .logo-img {
            max-width: 400px;
            height: auto;
            filter: drop-shadow(0 8px 15px rgba(0,0,0,0.5));
        }
        .top-3-section {
            display: flex;
            justify-content: space-around;
            align-items: flex-end;
            gap: 25px;
            margin-top: 40px;
            margin-bottom: 50px;
            width: 100%;
        }
        .top-player-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            width: 30%;
            min-width: 150px;
            min-height: 180px;
            justify-content: center;
            position: relative;
            transform: translateY(0);
            transition: transform 0.4s ease-in-out, box-shadow 0.4s ease-in-out;
            cursor: pointer;
        }
        .top-player-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.6);
        }
        .top-player-card.rank-1 {
            background: linear-gradient(135deg, #f72585 0%, #d90429 100%);
            color: #fff;
            transform: translateY(-30px);
            box-shadow: 0 20px 40px rgba(247, 37, 133, 0.6);
            z-index: 10;
        }
        .top-player-card.rank-2 {
            background: linear-gradient(135deg, #4361ee 0%, #03045e 100%);
            color: #fff;
            transform: translateY(-15px);
        }
        .top-player-card.rank-3 {
            background: linear-gradient(135deg, #4cc9f0 0%, #00b4d8 100%);
            color: #fff;
        }
        .top-player-card .crown-icon-top {
            position: absolute;
            top: -40px;
            left: 50%;
            transform: translateX(-50%);
            width: 70px;
            height: 70px;
            filter: drop-shadow(0 8px 15px rgba(0,0,0,0.7));
        }
        .top-player-card .profile-icon {
            font-size: 4rem;
            margin-bottom: 15px;
            color: #fff;
            border: none;
            border-radius: 50%;
            padding: 0;
            background-color: transparent;
        }
        .top-player-card .player-name, .top-player-card .player-score, .top-player-card .rank-number-top {
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        }
        .top-player-card.rank-1 .player-score, .top-player-card.rank-2 .player-score, .top-player-card.rank-3 .player-score {
            color: #fff;
            text-shadow: none;
        }
        .top-player-card .player-name {
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 8px;
        }
        .top-player-card .player-score {
            font-weight: 900;
            font-size: 1.5rem;
            color: #ffffff;
        }
        .rank-number-top {
            position: absolute;
            top: 8px;
            left: 12px;
            font-size: 1.4rem;
            font-weight: 900;
            color: rgba(255,255,255,0.7);
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.6);
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
            backdrop-filter: blur(5px);
        }
        .modal-content {
            background: linear-gradient(145deg, #302b63 0%, #0f0c29 100%);
            color: #ffffff;
            padding: 40px;
            border-radius: 20px;
            width: 90%;
            max-width: 550px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
            position: relative;
            text-align: left;
            animation: fadeIn 0.4s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .close-button {
            color: #e0e0e0;
            float: right;
            font-size: 36px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }
        .close-button:hover, .close-button:focus {
            color: #fff;
        }
        .modal-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 25px;
            color: #fff;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        }
        .modal-detail-item {
            margin-bottom: 15px;
            font-size: 1.2rem;
            color: #e0e0e0;
        }
        .modal-detail-item strong {
            color: #fff;
            font-weight: 600;
        }
        .chart-container {
            width: 100%;
            max-width: 700px;
            margin-top: 40px;
            padding: 25px;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            color: #ffffff;
            height: 450px;
        }
        canvas#salesChart {
            max-height: 100%;
        }

        @media (max-width: 768px) {
            .filter-controls { flex-direction: column; gap: 10px; width: 80%; margin: 0 auto; }
            .filter-controls select, .filter-controls button { width: 100%; }
        }
        @media (max-width: 640px) {
            body { padding: 10px; }
            .main-content-wrapper { margin-top: 0; padding: 15px; }
            .logo-img { max-width: 250px; }
            .top-3-section { flex-direction: column; align-items: center; gap: 15px; }
            .top-player-card { width: 80%; transform: translateY(0) !important; }
            .top-player-card.rank-1 .crown-icon-top { top: -25px; width: 50px; height: 50px; }
            .leaderboard-table th, .leaderboard-table td { padding: 10px; font-size: 0.8rem; }
            .modal-content { padding: 20px; max-width: 95%; }
            .modal-title { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <!-- Arka plan soyut şekiller -->
    <div class="abstract-shape shape-1"></div>
    <div class="abstract-shape shape-2"></div>
    <div class="abstract-shape shape-3"></div>
    <div class="abstract-shape shape-4"></div>

    <div class="main-content-wrapper">
        <div class="logo-container">
            <img src="https://www.upload.ee/image/18584579/Ads_z_tasar_m__8_.png" 
                 onerror="this.onerror=null;this.src='https://placehold.co/400x90/E5E7EB/1F2937?text=Logo+Yuklenemedi';" 
                 alt="Liderlik Tablosu" class="logo-img">
        </div>
        
        <p class="leaderboard-date text-left text-lg font-bold mb-4" id="currentPeriodDisplay"></p>

        <div class="filter-controls flex justify-center items-center flex-wrap gap-4 my-8">
            <select id="periodSelect" class="p-2 border-gray-700 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"></select>
            <select id="sortSelect" class="p-2 border-gray-700 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400">
                <option value="totalCiro" selected>Sırala: Toplam Ciro</option>
                <option value="successfulSalesCount">Sırala: Satış Adedi</option>
                <option value="totalCalls">Sırala: Toplam Arama</option>
                <option value="saleRate">Sırala: Satış Oranı (%)</option>
            </select>
            <button id="applyFilter" class="bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-2 px-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50">
                Getir
            </button>
        </div>

        <div class="leaderboard-container">
            <div class="top-3-section">
                <div id="rank2Card" class="top-player-card rank-2"></div>
                <div id="rank1Card" class="top-player-card rank-1"></div>
                <div id="rank3Card" class="top-player-card rank-3"></div>
            </div>

            <table class="leaderboard-table">
                <thead>
                    <tr>
                        <th>Sıra</th>
                        <th>Şube Adı</th>
                        <th id="tableHeaderValue">Toplam Ciro</th>
                    </tr>
                </thead>
                <tbody id="leaderboardBody"></tbody>
            </table>
            
            <div id="totalCiroContainer" class="mt-8 pt-6 border-t border-gray-700 text-center">
                <h3 class="text-xl font-bold uppercase tracking-wider text-white">Tüm Şubeler Toplam Ciro</h3>
                <p id="totalCiroValue" class="text-4xl font-extrabold text-yellow-500 mt-2" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">0 TL</p>
            </div>

            <div id="errorMessage" class="mt-4 text-red-500 hidden"></div>
            <div id="lastUpdated" class="mt-4 text-gray-500 text-sm"></div>
        </div>
        
        <!-- Chart Container -->
        <div class="chart-container">
            <select id="chartSelect" class="p-2 border-gray-700 bg-gray-800 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400 mb-4 w-full">
                <option value="totalCiro">Grafik: Toplam Ciro</option>
                <option value="successfulSalesCount">Grafik: Satış Adedi</option>
                <option value="totalCalls">Grafik: Toplam Arama</option>
                <option value="saleRate">Grafik: Satış Oranı (%)</option>
            </select>
            <canvas id="salesChart"></canvas>
        </div>
    </div>

    <div id="branchDetailModal" class="modal">
        <div class="modal-content">
            <span class="close-button">&times;</span>
            <h2 id="modalBranchName" class="modal-title"></h2>
            <div id="modalDetails"></div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            let myChart; 
            let allBranchDataGlobal = [];
            let autoRefreshInterval;

            const GOOGLE_APPS_SCRIPT_WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbxC1gkEmz0jW7oC8mNhLHfc9nTHVTs6SlzRTRxVyIcLnL5pdtqtZNzctPk4nJiCDj_2nw/exec'; 

            const leaderboardBody = document.getElementById('leaderboardBody');
            const currentPeriodDisplay = document.getElementById('currentPeriodDisplay'); 
            const errorMessage = document.getElementById('errorMessage');
            const lastUpdatedElement = document.getElementById('lastUpdated');
            const periodSelect = document.getElementById('periodSelect');
            const sortSelect = document.getElementById('sortSelect');
            const applyFilterButton = document.getElementById('applyFilter');
            const totalCiroValueElement = document.getElementById('totalCiroValue');
            const tableHeaderValue = document.getElementById('tableHeaderValue');
            const modalBranchName = document.getElementById('modalBranchName');
            const modalDetails = document.getElementById('modalDetails');
            const closeButton = document.querySelector('.close-button');
            const chartSelect = document.getElementById('chartSelect');

            const startAutoRefresh = () => {
                if (autoRefreshInterval) clearInterval(autoRefreshInterval);
                autoRefreshInterval = setInterval(() => {
                    fetchLeaderboardData(true); // Arka planda sessiz yenileme yap
                }, 30000); // 30 saniye
            };

            const formatValue = (value, criteria) => {
                value = value === undefined || value === null || isNaN(value) ? 0 : value;
                switch (criteria) {
                    case 'totalCiro': 
                    case 'averageCiro':
                        return new Intl.NumberFormat('tr-TR', { 
                            style: 'currency', 
                            currency: 'TRY',
                            minimumFractionDigits: 0,
                            maximumFractionDigits: 0
                        }).format(value);
                    case 'successfulSalesCount': 
                    case 'totalCalls': 
                        return `${value} Adet`;
                    case 'saleRate': 
                        return `%${parseFloat(value).toFixed(2)}`;
                    default: 
                        return value;
                }
            };

            const createPlayerCardHTML = (rank, branchData, criteria) => {
                if (!branchData || branchData.branch === 'Yükleniyor...') {
                    return `<div class="flex items-center justify-center h-full"><svg class="animate-spin h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg></div>`;
                }
                const score = formatValue(branchData[criteria], criteria);
                const crownHTML = rank === 1 ? `<img src="https://www.upload.ee/image/18258333/0_12e6cc_138b775d_orig.png" alt="Kral Tacı" class="crown-icon-top">` : '';
                return `${crownHTML}<span class="rank-number-top">${rank}</span><i class="fas fa-user-circle profile-icon"></i>
                    <div class="player-name">${branchData.branch}</div><div class="player-score">${score}</div>`;
            };

            const updateDisplay = () => {
                const sortCriteria = sortSelect.value;
                const sortedData = [...allBranchDataGlobal].sort((a, b) => (b[sortCriteria] || 0) - (a[sortCriteria] || 0));
                
                const headerOption = sortSelect.querySelector(`option[value="${sortCriteria}"]`);
                tableHeaderValue.textContent = headerOption ? headerOption.textContent.replace('Sırala: ', '') : 'Değer';
                
                const rank1Data = sortedData[0] || null;
                const rank2Data = sortedData[1] || null;
                const rank3Data = sortedData[2] || null;

                document.getElementById('rank1Card').innerHTML = createPlayerCardHTML(1, rank1Data, sortCriteria);
                document.getElementById('rank2Card').innerHTML = createPlayerCardHTML(2, rank2Data, sortCriteria);
                document.getElementById('rank3Card').innerHTML = createPlayerCardHTML(3, rank3Data, sortCriteria);
                
                if (rank1Data) document.getElementById('rank1Card').onclick = () => showBranchDetails(rank1Data);
                if (rank2Data) document.getElementById('rank2Card').onclick = () => showBranchDetails(rank2Data);
                if (rank3Data) document.getElementById('rank3Card').onclick = () => showBranchDetails(rank3Data);
                
                leaderboardBody.innerHTML = '';
                if (sortedData.length === 0 && !errorMessage.textContent) {
                    leaderboardBody.innerHTML = `<tr><td colspan="3" class="text-center py-6 text-gray-400">Bu dönem için veri bulunamadı.</td></tr>`;
                } else {
                    sortedData.forEach((item, index) => {
                        const row = leaderboardBody.insertRow();
                        row.dataset.branch = item.branch;
                        row.insertCell(0).textContent = index + 1;
                        row.insertCell(1).textContent = item.branch;
                        row.insertCell(2).textContent = formatValue(item[sortCriteria], sortCriteria);
                        row.onclick = () => showBranchDetails(item);
                    });
                }
                
                const totalCiro = allBranchDataGlobal.reduce((sum, item) => sum + (item.totalCiro || 0), 0);
                totalCiroValueElement.textContent = formatValue(totalCiro, 'totalCiro');
                
                renderChart(sortedData, chartSelect.value);
                lastUpdatedElement.textContent = `Son Güncelleme: ${new Date().toLocaleString('tr-TR')}`;
            };
            
            const setLoadingState = (message = "Veriler Yükleniyor...") => {
                 errorMessage.classList.add('hidden');
                 errorMessage.textContent = '';
                 leaderboardBody.innerHTML = `<tr><td colspan="3" class="text-center py-8"><div class="flex justify-center items-center"><svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg><span>${message}</span></div></td></tr>`;
                 document.getElementById('rank1Card').innerHTML = createPlayerCardHTML(1, { branch: 'Yükleniyor...' });
                 document.getElementById('rank2Card').innerHTML = createPlayerCardHTML(2, { branch: 'Yükleniyor...' });
                 document.getElementById('rank3Card').innerHTML = createPlayerCardHTML(3, { branch: 'Yükleniyor...' });
                 if (myChart) myChart.destroy();
                 totalCiroValueElement.textContent = 'Hesaplanıyor...';
            };

            async function fetchAvailablePeriods() {
                try {
                    const response = await fetch(`${GOOGLE_APPS_SCRIPT_WEB_APP_URL}?action=getAvailablePeriods&t=${new Date().getTime()}`);
                    if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
                    const periods = await response.json();
                    if (periods.error) throw new Error(periods.error);
                    
                    const currentSelected = periodSelect.value;
                    periodSelect.innerHTML = '';
                    
                    const monthOrder = ['OCAK', 'ŞUBAT', 'MART', 'NİSAN', 'MAYIS', 'HAZİRAN', 'TEMMUZ', 'AĞUSTOS', 'EYLÜL', 'EKİM', 'KASIM', 'ARALIK'];
                    periods.sort((a, b) => {
                        const [monthA, yearA] = a.split(' ');
                        const [monthB, yearB] = b.split(' ');
                        if (parseInt(yearA) !== parseInt(yearB)) return parseInt(yearB) - parseInt(yearA);
                        return monthOrder.indexOf(monthB) - monthOrder.indexOf(monthA);
                    }).forEach(period => periodSelect.add(new Option(period, period)));
                    
                    if ([...periodSelect.options].some(opt => opt.value === currentSelected)) {
                        periodSelect.value = currentSelected;
                    }

                } catch (error) {
                    console.error(`Dönemler yüklenemedi: ${error.message}`);
                }
            }

            async function fetchLeaderboardData(isSilentRefresh = false) {
                const selectedPeriod = periodSelect.value;
                if (!selectedPeriod) {
                    errorMessage.textContent = "Lütfen bir dönem seçin.";
                    errorMessage.classList.remove('hidden');
                    return;
                }
                if (!isSilentRefresh) {
                   setLoadingState(`'${selectedPeriod}' verileri yükleniyor...`);
                }
                currentPeriodDisplay.textContent = `Dönem: ${selectedPeriod}`;
                try {
                    const url = `${GOOGLE_APPS_SCRIPT_WEB_APP_URL}?action=getLeaderboard&sheetName=${encodeURIComponent(selectedPeriod)}&t=${new Date().getTime()}`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`Sunucu hatası: ${response.status}`);
                    const data = await response.json();

                    if(data.error) throw new Error(data.error);

                    allBranchDataGlobal = data.leaderboard;
                    
                    updateDisplay();
                    
                    if (!isSilentRefresh) {
                        startAutoRefresh();
                    }

                } catch (error) {
                    errorMessage.textContent = `Veriler yüklenemedi: ${error.message}`;
                    errorMessage.classList.remove('hidden');
                    if (error.message.includes('404')) {
                        errorMessage.textContent = "Sayfa bulunamadı. Lütfen Apps Script URL'sini kontrol edin.";
                    } else if (error.message.includes('500')) {
                        errorMessage.textContent = "Sunucu tarafında bir hata oluştu. Lütfen Apps Script kodunu kontrol edin.";
                    }
                }
            }
            
            function renderChart(data, criteria) {
                const ctx = document.getElementById('salesChart').getContext('2d');
                if (myChart) myChart.destroy();

                const chartLabel = chartSelect.options[chartSelect.selectedIndex].text.replace('Grafik: ', '');
                const formattedData = data.map(item => item[criteria] || 0);
                const backgroundColor = criteria === 'saleRate' ? '#f72585' : '#4361ee';
                const borderColor = criteria === 'saleRate' ? '#f72585' : '#4361ee';
                const yAxisTitle = criteria === 'totalCiro' ? 'Ciro (TL)' : (criteria === 'saleRate' ? 'Oran (%)' : 'Adet');

                myChart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: data.map(item => item.branch), 
                        datasets: [{ 
                            label: chartLabel, 
                            data: formattedData, 
                            backgroundColor: backgroundColor, 
                            borderColor: borderColor, 
                            borderWidth: 1 
                        }] 
                    },
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { 
                            legend: { display: false }, 
                            title: { display: true, text: `Şube ${chartLabel} Karşılaştırması`, font: { size: 16 }, color: '#e0e0e0' }, 
                            tooltip: { 
                                callbacks: { 
                                    label: (context) => formatValue(context.parsed.y, criteria) 
                                } 
                            } 
                        },
                        scales: { 
                            x: { 
                                ticks: { color: '#e0e0e0' }, 
                                grid: { color: 'rgba(255, 255, 255, 0.1)' } 
                            }, 
                            y: { 
                                beginAtZero: true, 
                                title: { display: true, text: yAxisTitle, color: '#e0e0e0' }, 
                                ticks: { 
                                    color: '#e0e0e0', 
                                    callback: (value) => {
                                        if (criteria === 'totalCiro' || criteria === 'averageCiro') {
                                            return new Intl.NumberFormat('tr-TR', { notation: 'compact' }).format(value);
                                        }
                                        return value;
                                    } 
                                }, 
                                grid: { color: 'rgba(255, 255, 255, 0.1)' } 
                            } 
                        }
                    }
                });
            }

            function showBranchDetails(branchData) {
                modalBranchName.textContent = branchData.branch || 'Bilinmiyor';
                modalDetails.innerHTML = `
                    <p class="modal-detail-item"><strong>Toplam Ciro:</strong> <span>${formatValue(branchData.totalCiro, 'totalCiro')}</span></p>
                    <p class="modal-detail-item"><strong>Başarılı Satış Sayısı:</strong> <span>${formatValue(branchData.successfulSalesCount, 'successfulSalesCount')}</span></p>
                    <p class="modal-detail-item"><strong>Toplam Arama:</strong> <span>${formatValue(branchData.totalCalls, 'totalCalls')}</span></p>
                    <p class="modal-detail-item"><strong>Satış Oranı:</strong> <span>${formatValue(branchData.saleRate, 'saleRate')}</span></p>
                    <p class="modal-detail-item"><strong>Ortalama Ciro:</strong> <span>${formatValue(branchData.averageCiro, 'averageCiro')}</span></p>
                `;
                document.getElementById('branchDetailModal').style.display = 'flex';
            }
            
            // Olay Dinleyicileri
            closeButton.onclick = () => document.getElementById('branchDetailModal').style.display = 'none';
            window.onclick = (event) => { if (event.target == document.getElementById('branchDetailModal')) document.getElementById('branchDetailModal').style.display = 'none'; };
            applyFilterButton.onclick = () => fetchLeaderboardData();
            sortSelect.onchange = () => { if (allBranchDataGlobal.length > 0) updateDisplay(); };
            chartSelect.onchange = () => { if (allBranchDataGlobal.length > 0) renderChart(allBranchDataGlobal, chartSelect.value); };

            // --- HIZLI İLK YÜKLEME MANTIĞI ---
            const monthOrder = ['OCAK', 'ŞUBAT', 'MART', 'NİSAN', 'MAYIS', 'HAZİRAN', 'TEMMUZ', 'AĞUSTOS', 'EYLÜL', 'EKİM', 'KASIM', 'ARALIK'];
            const now = new Date();
            const currentMonthName = monthOrder[now.getMonth()];
            const currentYear = now.getFullYear();
            const currentPeriodName = `${currentMonthName} ${currentYear}`;
            
            // Seçim kutusuna geçici olarak mevcut dönemi ekle
            periodSelect.innerHTML = `<option value="${currentPeriodName}">${currentPeriodName}</option>`;
            periodSelect.value = currentPeriodName;

            // Mevcut ayın verilerini hemen getir
            fetchLeaderboardData(); 
            
            // Diğer tüm dönemleri arka planda getir ve seçim kutusunu doldur
            fetchAvailablePeriods();
        });
    </script>
</body>
</html>
