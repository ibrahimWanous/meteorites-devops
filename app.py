from flask import Flask
import requests
from collections import Counter

app = Flask(__name__)

def get_data():
    URL = "https://dmachek.github.io/meteorites-homework/meteorite_landings.json"
    data = requests.get(URL, verify=False).json()
    return data

@app.route("/")
def index():
    data = get_data()

    total = len(data)

    with_mass = [(m["name"], float(m["mass"])) for m in data if m.get("mass")]
    heaviest = max(with_mass, key=lambda x: x[1])

    years = [m["year"][:4] for m in data if m.get("year")]
    top_year, count = Counter(years).most_common(1)[0]

    return f"""
    <html>
        <head>
            <title>Meteorite Analysis</title>
            <style>
                body {{ font-family: Arial; padding: 40px; background: #f0f0f0; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                a {{ color: #0078d4; text-decoration: none; font-size: 18px; display: block; margin-bottom: 10px; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🌠 Meteorite Landings Analysis</h1>
                <h3>Total Entries: {total}</h3>
                <h3>Most Massive: {heaviest[0]} — {heaviest[1]:,.0f} g</h3>
                <h3>Most Frequent Year: {top_year} ({count} meteorites)</h3>
            </div>
            <a href="/table">📋 View all {total} meteorites →</a>
            <a href="/quality">🔍 Data Quality Report →</a>
        </body>
    </html>
    """

@app.route("/table")
def table():
    data = get_data()

    rows = ""
    for m in data:
        name = m.get("name", "")
        mass = f"{float(m['mass']):,.0f} g" if m.get("mass") else "Unknown"
        year = m.get("year", "")[:4] if m.get("year") else "Unknown"
        fall = m.get("fall", "")
        recclass = m.get("recclass", "")
        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{mass}</td>
            <td>{year}</td>
            <td>{fall}</td>
            <td>{recclass}</td>
        </tr>
        """

    return f"""
    <html>
        <head>
            <title>All Meteorites</title>
            <style>
                body {{ font-family: Arial; padding: 40px; background: #f0f0f0; }}
                h1 {{ color: #333; }}
                input {{ padding: 10px; width: 300px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }}
                table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }}
                th {{ background: #0078d4; color: white; padding: 12px; text-align: left; cursor: pointer; }}
                td {{ padding: 10px; border-bottom: 1px solid #eee; }}
                tr:hover {{ background: #f5f5f5; }}
                a {{ color: #0078d4; }}
            </style>
        </head>
        <body>
            <h1>🌠 All Meteorites</h1>
            <a href="/">← Back to summary</a><br><br>
            <input type="text" id="search" placeholder="Search meteorites..." onkeyup="filterTable()">
            <table id="meteoriteTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Name ↕</th>
                        <th onclick="sortTable(1)">Mass ↕</th>
                        <th onclick="sortTable(2)">Year ↕</th>
                        <th onclick="sortTable(3)">Fall ↕</th>
                        <th onclick="sortTable(4)">Class ↕</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    {rows}
                </tbody>
            </table>

            <script>
                function filterTable() {{
                    const input = document.getElementById("search").value.toLowerCase();
                    const rows = document.getElementById("tableBody").getElementsByTagName("tr");
                    for (let row of rows) {{
                        const text = row.innerText.toLowerCase();
                        row.style.display = text.includes(input) ? "" : "none";
                    }}
                }}

                function sortTable(col) {{
                    const table = document.getElementById("meteoriteTable");
                    const rows = Array.from(table.rows).slice(1);
                    rows.sort((a, b) => a.cells[col].innerText.localeCompare(b.cells[col].innerText));
                    rows.forEach(row => table.appendChild(row));
                }}
            </script>
        </body>
    </html>
    """

@app.route("/quality")
def quality():
    data = get_data()

    missing_mass = sum(1 for m in data if not m.get("mass"))
    missing_year = sum(1 for m in data if not m.get("year"))
    missing_location = sum(1 for m in data if not m.get("reclat"))
    missing_name = sum(1 for m in data if not m.get("name"))

    return f"""
    <html>
        <head>
            <title>Data Quality</title>
            <style>
                body {{ font-family: Arial; padding: 40px; background: #f0f0f0; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px; }}
                .bad {{ border-left: 5px solid red; }}
                .good {{ border-left: 5px solid green; }}
                a {{ color: #0078d4; }}
            </style>
        </head>
        <body>
            <h1>🔍 Data Quality Report</h1>
            <a href="/">← Back to summary</a><br><br>

            <div class="card {'bad' if missing_mass > 0 else 'good'}">
                <h3>Missing Mass: {missing_mass} / {len(data)}</h3>
            </div>
            <div class="card {'bad' if missing_year > 0 else 'good'}">
                <h3>Missing Year: {missing_year} / {len(data)}</h3>
            </div>
            <div class="card {'bad' if missing_location > 0 else 'good'}">
                <h3>Missing Location: {missing_location} / {len(data)}</h3>
            </div>
            <div class="card {'bad' if missing_name > 0 else 'good'}">
                <h3>Missing Name: {missing_name} / {len(data)}</h3>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)