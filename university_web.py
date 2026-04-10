from flask import Flask, render_template_string, request, jsonify
from enhanced_university_bot import EnhancedUniversityBot
import json

app = Flask(__name__)
bot = EnhancedUniversityBot()

# HTML Template with Modern UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>University Search India - Find Your Dream College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        /* Header */
        .header {
            background: rgba(255,255,255,0.95);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
        }

        .logo span {
            color: #764ba2;
        }

        .nav-links {
            display: flex;
            gap: 1.5rem;
        }

        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: #667eea;
        }

        /* Main Container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            color: white;
            padding: 3rem 1rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .hero p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        /* Search Box */
        .search-container {
            background: white;
            border-radius: 50px;
            padding: 0.5rem;
            display: flex;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 2rem;
        }

        .search-input {
            flex: 1;
            padding: 1rem 1.5rem;
            border: none;
            outline: none;
            font-size: 1.1rem;
            border-radius: 50px;
        }

        .search-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            transition: transform 0.3s;
        }

        .search-btn:hover {
            transform: scale(1.05);
        }

        /* Filters */
        .filters {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 2rem 0;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .filter-btn {
            padding: 0.5rem 1.5rem;
            border: 2px solid #667eea;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
        }

        .filter-btn:hover, .filter-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: transparent;
        }

        /* Results Section */
        .results-section {
            margin-top: 2rem;
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            color: white;
        }

        .results-count {
            font-size: 1.1rem;
        }

        .view-toggle {
            display: flex;
            gap: 0.5rem;
        }

        .toggle-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            cursor: pointer;
            color: white;
            transition: background 0.3s;
        }

        .toggle-btn.active {
            background: white;
            color: #667eea;
        }

        /* Cards Grid */
        .universities-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }

        /* University Card */
        .university-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }

        .university-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
        }

        .card-header h3 {
            font-size: 1.2rem;
            margin-bottom: 0.3rem;
        }

        .card-header p {
            font-size: 0.85rem;
            opacity: 0.9;
        }

        .card-body {
            padding: 1rem;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.8rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
        }

        .info-label {
            font-weight: bold;
            color: #666;
        }

        .info-value {
            color: #333;
            font-weight: 500;
        }

        .placement-badge {
            background: #4caf50;
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 5px;
            font-size: 0.75rem;
            display: inline-block;
        }

        .rating {
            color: #ffc107;
            font-size: 0.9rem;
        }

        /* Detailed View */
        .university-detail {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
            display: none;
        }

        .detail-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }

        .detail-title h2 {
            color: #667eea;
            margin-bottom: 0.5rem;
        }

        .close-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            cursor: pointer;
        }

        .detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .detail-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
        }

        .detail-section h4 {
            color: #667eea;
            margin-bottom: 1rem;
        }

        /* Reviews Section */
        .reviews-section {
            margin-top: 1.5rem;
        }

        .review-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }

        .review-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }

        .add-review {
            margin-top: 1rem;
            padding: 1rem;
            background: #e9ecef;
            border-radius: 10px;
        }

        .add-review input, .add-review textarea {
            width: 100%;
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        /* Loading Animation */
        .loading {
            text-align: center;
            padding: 3rem;
            color: white;
        }

        .spinner {
            border: 3px solid rgba(255,255,255,0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .universities-grid {
                grid-template-columns: 1fr;
            }
            
            .hero h1 {
                font-size: 1.8rem;
            }
            
            .nav-container {
                flex-direction: column;
                gap: 1rem;
            }
        }

        /* Scroll to top */
        .scroll-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #667eea;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            display: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: all 0.3s;
        }

        .scroll-top:hover {
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="nav-container">
            <div class="logo">
                🎓 <span>UniversitySearch</span>.in
            </div>
            <div class="nav-links">
                <a href="#" onclick="showHome()">Home</a>
                <a href="#" onclick="showCompare()">Compare</a>
                <a href="#" onclick="showTopUniversities()">Top Universities</a>
                <a href="#" onclick="showHelp()">Help</a>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="hero">
            <h1>🔍 Find Your Dream University in India</h1>
            <p>Search from 50+ universities • Compare • Read Reviews • Get Cutoff Ranks</p>
            
            <div class="search-container">
                <input type="text" class="search-input" id="searchInput" placeholder="Search by university name (e.g., LPU, IIT Bombay, Sharda, VIT)..." onkeypress="handleKeyPress(event)">
                <button class="search-btn" onclick="searchUniversities()">🔍 Search</button>
            </div>
        </div>

        <div class="filters">
            <button class="filter-btn active" onclick="filterByCategory('all')">🎓 All</button>
            <button class="filter-btn" onclick="filterByCategory('IIT')">🏆 IITs</button>
            <button class="filter-btn" onclick="filterByCategory('NIT')">⭐ NITs</button>
            <button class="filter-btn" onclick="filterByCategory('IIIT')">💻 IIITs</button>
            <button class="filter-btn" onclick="filterByCategory('Private')">🏛️ Private</button>
            <button class="filter-btn" onclick="filterByCategory('Central')">🏢 Central</button>
        </div>

        <div class="results-section">
            <div class="results-header">
                <div class="results-count" id="resultsCount">Showing 0 universities</div>
                <div class="view-toggle">
                    <button class="toggle-btn active" onclick="setView('grid')">📱 Grid</button>
                    <button class="toggle-btn" onclick="setView('list')">📋 List</button>
                </div>
            </div>
            <div id="resultsContainer" class="universities-grid"></div>
        </div>

        <div id="detailView" class="university-detail"></div>
    </div>

    <div class="scroll-top" onclick="scrollToTop()">↑</div>

    <script>
        let currentView = 'grid';
        let currentUniversities = [];
        let currentFilter = 'all';

        async function searchUniversities() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) return;
            
            showLoading();
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query})
                });
                const data = await response.json();
                currentUniversities = data.results;
                displayResults(currentUniversities);
            } catch (error) {
                console.error('Error:', error);
                showError();
            }
        }

        async function filterByCategory(category) {
            currentFilter = category;
            
            // Update active button
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.includes(category.toUpperCase()) || (category === 'all' && btn.textContent === '🎓 All')) {
                    btn.classList.add('active');
                }
            });
            
            showLoading();
            
            try {
                const response = await fetch('/api/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({category: category})
                });
                const data = await response.json();
                currentUniversities = data.results;
                displayResults(currentUniversities);
            } catch (error) {
                console.error('Error:', error);
                showError();
            }
        }

        async function showTopUniversities() {
            showLoading();
            try {
                const response = await fetch('/api/top');
                const data = await response.json();
                currentUniversities = data.results;
                displayResults(currentUniversities);
            } catch (error) {
                console.error('Error:', error);
            }
        }

        async function showUniversityDetail(university) {
            try {
                const response = await fetch('/api/detail', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: university})
                });
                const data = await response.json();
                displayDetail(data.detail);
                document.getElementById('detailView').style.display = 'block';
                window.scrollTo({top: document.getElementById('detailView').offsetTop, behavior: 'smooth'});
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function displayResults(universities) {
            const container = document.getElementById('resultsContainer');
            const countDisplay = document.getElementById('resultsCount');
            
            countDisplay.textContent = `Showing ${universities.length} universities`;
            
            if (universities.length === 0) {
                container.innerHTML = '<div class="loading"><p>No universities found. Try a different search!</p></div>';
                return;
            }
            
            if (currentView === 'grid') {
                container.innerHTML = universities.map(uni => `
                    <div class="university-card" onclick="showUniversityDetail('${uni.name}')">
                        <div class="card-header">
                            <h3>${uni.name}</h3>
                            <p>📍 ${uni.location}</p>
                        </div>
                        <div class="card-body">
                            <div class="info-row">
                                <span class="info-label">💰 Avg Package</span>
                                <span class="info-value">${uni.placement_average}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">📝 Exam</span>
                                <span class="info-value">${uni.exam}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">🏷️ Type</span>
                                <span class="info-value">${uni.type}</span>
                            </div>
                            <div>
                                <span class="placement-badge">✅ ${uni.placement_rate} Placement</span>
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = universities.map(uni => `
                    <div class="university-card" onclick="showUniversityDetail('${uni.name}')">
                        <div class="card-header">
                            <h3>${uni.name}</h3>
                            <p>📍 ${uni.location}</p>
                        </div>
                        <div class="card-body">
                            <div class="info-row">
                                <span class="info-label">💰 Avg Package:</span>
                                <span class="info-value">${uni.placement_average}</span>
                                <span class="info-label">📝 Exam:</span>
                                <span class="info-value">${uni.exam}</span>
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        }

        function displayDetail(detail) {
            const detailDiv = document.getElementById('detailView');
            detailDiv.innerHTML = detail;
        }

        function setView(view) {
            currentView = view;
            document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            if (currentUniversities.length > 0) {
                displayResults(currentUniversities);
            }
        }

        function showHome() {
            document.getElementById('searchInput').value = '';
            filterByCategory('all');
            document.getElementById('detailView').style.display = 'none';
        }

        function showCompare() {
            alert('Compare feature: Type "compare IIT Delhi and IIT Bombay" in search');
        }

        function showHelp() {
            alert('💡 Tips:\\n\\n• Search by university name: "LPU", "IIT Bombay"\\n• Filter by category using buttons above\\n• Click on any card to see detailed info\\n• Try "Top 10 IITs" in search');
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                searchUniversities();
            }
        }

        function showLoading() {
            const container = document.getElementById('resultsContainer');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Searching...</p></div>';
        }

        function showError() {
            const container = document.getElementById('resultsContainer');
            container.innerHTML = '<div class="loading"><p>❌ Something went wrong. Please try again.</p></div>';
        }

        function scrollToTop() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        // Show/hide scroll button
        window.addEventListener('scroll', () => {
            const scrollBtn = document.querySelector('.scroll-top');
            if (window.scrollY > 300) {
                scrollBtn.style.display = 'flex';
            } else {
                scrollBtn.style.display = 'none';
            }
        });

        // Load top universities on start
        showTopUniversities();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    results = bot.search_university(query)
    
    output = []
    for uni in results:
        output.append({
            'name': uni.get('name', 'N/A'),
            'location': uni.get('location', 'N/A'),
            'placement_average': uni.get('placement', {}).get('average', 'N/A'),
            'placement_rate': uni.get('placement', {}).get('rate', 'N/A'),
            'exam': uni.get('admission', {}).get('exam', 'N/A'),
            'type': uni.get('type', 'N/A')
        })
    
    return jsonify({'results': output})

@app.route('/api/filter', methods=['POST'])
def filter_by_category():
    data = request.json
    category = data.get('category', 'all')
    
    if category == 'all':
        results = bot.universities
    else:
        results = [u for u in bot.universities if category.lower() in u.get('category', '').lower() or category.lower() in u.get('type', '').lower()]
    
    output = []
    for uni in results[:20]:
        output.append({
            'name': uni.get('name', 'N/A'),
            'location': uni.get('location', 'N/A'),
            'placement_average': uni.get('placement', {}).get('average', 'N/A'),
            'placement_rate': uni.get('placement', {}).get('rate', 'N/A'),
            'exam': uni.get('admission', {}).get('exam', 'N/A'),
            'type': uni.get('type', 'N/A')
        })
    
    return jsonify({'results': output})

@app.route('/api/top')
def top_universities():
    results = bot.universities[:15]
    output = []
    for uni in results:
        output.append({
            'name': uni.get('name', 'N/A'),
            'location': uni.get('location', 'N/A'),
            'placement_average': uni.get('placement', {}).get('average', 'N/A'),
            'placement_rate': uni.get('placement', {}).get('rate', 'N/A'),
            'exam': uni.get('admission', {}).get('exam', 'N/A'),
            'type': uni.get('type', 'N/A')
        })
    return jsonify({'results': output})

@app.route('/api/detail', methods=['POST'])
def university_detail():
    data = request.json
    name = data.get('name', '')
    
    for uni in bot.universities:
        if uni.get('name') == name:
            detail_html = f"""
            <div class="detail-header">
                <div class="detail-title">
                    <h2>📚 {uni.get('name', 'N/A')}</h2>
                    <p>📍 {uni.get('location', 'N/A')} | 🏷️ {uni.get('category', 'N/A')} - {uni.get('type', 'N/A')}</p>
                </div>
                <button class="close-btn" onclick="document.getElementById('detailView').style.display='none'">✕ Close</button>
            </div>
            
            <div class="detail-grid">
                <div class="detail-section">
                    <h4>💰 Fee Structure</h4>
                    <p><strong>B.Tech:</strong> {uni.get('fees', {}).get('btech', 'N/A')}</p>
                    <p><strong>Hostel:</strong> {uni.get('fees', {}).get('hostel', 'N/A')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>💼 Placements</h4>
                    <p><strong>Average Package:</strong> {uni.get('placement', {}).get('average', 'N/A')}</p>
                    <p><strong>Highest Package:</strong> {uni.get('placement', {}).get('highest', 'N/A')}</p>
                    <p><strong>Placement Rate:</strong> {uni.get('placement', {}).get('rate', 'N/A')}</p>
                    <p><strong>Top Recruiters:</strong> {', '.join(uni.get('placement', {}).get('top_recruiters', ['Various'])[:3])}</p>
                </div>
                
                <div class="detail-section">
                    <h4>📝 Admission</h4>
                    <p><strong>Entrance Exam:</strong> {uni.get('admission', {}).get('exam', 'N/A')}</p>
                    <p><strong>Deadline:</strong> {uni.get('admission', {}).get('deadline', 'N/A')}</p>
                    <p><strong>Process:</strong> {uni.get('admission', {}).get('process', 'N/A')}</p>
                </div>
                
                <div class="detail-section">
                    <h4>🎓 Courses Offered</h4>
                    <p>{', '.join(uni.get('courses', ['B.Tech', 'M.Tech'])[:6])}</p>
                </div>
            </div>
            """
            
            # Add cutoff info
            cutoff = uni.get('cutoff', {})
            if cutoff:
                detail_html += f"""
                <div class="detail-section" style="margin-top: 1rem;">
                    <h4>📊 Cutoff Ranks</h4>
                    <div class="detail-grid" style="margin-top: 0.5rem;">
                """
                if 'general' in cutoff:
                    detail_html += f"<p><strong>General:</strong> {cutoff['general']}</p>"
                if 'obc' in cutoff:
                    detail_html += f"<p><strong>OBC:</strong> {cutoff['obc']}</p>"
                if 'sc' in cutoff:
                    detail_html += f"<p><strong>SC:</strong> {cutoff['sc']}</p>"
                if 'st' in cutoff:
                    detail_html += f"<p><strong>ST:</strong> {cutoff['st']}</p>"
                if 'bitsat_score' in cutoff:
                    detail_html += f"<p><strong>BITSAT Score:</strong> {cutoff['bitsat_score']}+</p>"
                detail_html += "</div></div>"
            
            return jsonify({'detail': detail_html})
    
    return jsonify({'detail': '<p>University not found</p>'})

if __name__ == '__main__':
    print("="*60)
    print("🌐 University Search Web Interface")
    print("="*60)
    print("📍 Open in browser: http://localhost:5000")
    print("🔍 Search for: LPU, IIT Bombay, Sharda, VIT, etc.")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)