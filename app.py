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

    # Total entries
    total = len(data)

    # Most massive
    with_mass = [(m["name"], float(m["mass"])) for m in data if m.get("mass")]
    heaviest = max(with_mass, key=lambda x: x[1])

    # Most frequent year
    years = [m["year"][:4] for m in data if m.get("year")]
    top_year, count = Counter(years).most_common(1)[0]

    return f"""
    <html>
        <body style="font-family: Arial; padding: 40px; background: #f0f0f0;">
            <h1>🌠 Meteorite Landings Analysis</h1>
            <h3>Total Entries: {total}</h3>
            <h3>Most Massive: {heaviest[0]} — {heaviest[1]:,.0f} g</h3>
            <h3>Most Frequent Year: {top_year} ({count} meteorites)</h3>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)