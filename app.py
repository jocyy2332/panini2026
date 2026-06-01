"""
Panini FIFA World Cup 2026 - Web App
Ejecutar: python app.py
Abrir en celular: http://<tu-ip>:5000
"""
from flask import Flask, jsonify, request, render_template
import json, os

app = Flask(__name__)
SAVE_FILE = "progreso.json"

# ── Datos del álbum (orden oficial Panini 2026) ──
GROUPS = [
    ("A", [("MEX","México"), ("RSA","Sudáfrica"), ("KOR","Corea del Sur"), ("CZE","Chequia")]),
    ("B", [("CAN","Canadá"), ("BIH","Bosnia y Herz."), ("QAT","Catar"), ("SUI","Suiza")]),
    ("C", [("BRA","Brasil"), ("MAR","Marruecos"), ("HAI","Haití"), ("SCO","Escocia")]),
    ("D", [("USA","EEUU"), ("PAR","Paraguay"), ("AUS","Australia"), ("TUR","Turquía")]),
    ("E", [("GER","Alemania"), ("CUW","Curazao"), ("CIV","C. de Marfil"), ("ECU","Ecuador")]),
    ("F", [("NED","Países Bajos"), ("JPN","Japón"), ("SWE","Suecia"), ("TUN","Túnez")]),
    ("G", [("BEL","Bélgica"), ("EGY","Egipto"), ("IRN","Irán"), ("NZL","Nueva Zelanda")]),
    ("H", [("ESP","España"), ("CPV","Cabo Verde"), ("KSA","Arabia Saudita"), ("URU","Uruguay")]),
    ("I", [("FRA","Francia"), ("SEN","Senegal"), ("IRQ","Irak"), ("NOR","Noruega")]),
    ("J", [("ARG","Argentina"), ("ALG","Argelia"), ("AUT","Austria"), ("JOR","Jordania")]),
    ("K", [("POR","Portugal"), ("COD","RD Congo"), ("UZB","Uzbekistán"), ("COL","Colombia")]),
    ("L", [("ENG","Inglaterra"), ("CRO","Croacia"), ("GHA","Ghana"), ("PAN","Panamá")]),
    ("FW",[("FW","Especiales FIFA")]),
]

def build_stickers():
    s = {}
    for group, teams in GROUPS:
        for code, name in teams:
            for i in range(1, 21):
                key = f"{code} {i}"
                s[key] = {"group": group, "team": name, "code": code, "num": i, "count": 0}
    return s

def load_data():
    stickers = build_stickers()
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                saved = json.load(f)
            for k, v in saved.items():
                if k in stickers:
                    stickers[k]["count"] = v
        except:
            pass
    return stickers

def save_data(stickers):
    with open(SAVE_FILE, "w") as f:
        json.dump({k: v["count"] for k, v in stickers.items()}, f)

def get_stats(stickers):
    total = len(stickers)
    have  = sum(1 for v in stickers.values() if v["count"] >= 1)
    return {
        "total":    total,
        "have":     have,
        "missing":  total - have,
        "repeated": sum(1 for v in stickers.values() if v["count"] > 1),
        "extras":   sum(max(0, v["count"]-1) for v in stickers.values()),
        "pct":      round(have / total * 100, 1) if total else 0,
    }

# ── Rutas ──
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stickers")
def api_stickers():
    return jsonify(load_data())

@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats(load_data()))

@app.route("/api/add", methods=["POST"])
def api_add():
    key = request.json.get("key","").strip().upper()
    stickers = load_data()
    if key not in stickers:
        return jsonify({"ok": False, "msg": f"Código '{key}' no encontrado."})
    stickers[key]["count"] += 1
    save_data(stickers)
    v = stickers[key]
    return jsonify({"ok": True, "key": key, "team": v["team"],
                    "count": v["count"], "repeated": v["count"] > 1})

@app.route("/api/remove", methods=["POST"])
def api_remove():
    key = request.json.get("key","").strip().upper()
    stickers = load_data()
    if key not in stickers or stickers[key]["count"] == 0:
        return jsonify({"ok": False, "msg": "No se puede quitar."})
    stickers[key]["count"] -= 1
    save_data(stickers)
    return jsonify({"ok": True, "key": key, "count": stickers[key]["count"]})

@app.route("/api/bulk", methods=["POST"])
def api_bulk():
    """Agregar múltiples figuritas de una lista de texto"""
    text = request.json.get("text","")
    stickers = load_data()
    added, not_found = [], []
    for line in text.replace(",", "\n").split("\n"):
        key = line.strip().upper()
        if not key: continue
        if key in stickers:
            stickers[key]["count"] += 1
            added.append(key)
        else:
            not_found.append(key)
    if added:
        save_data(stickers)
    return jsonify({"ok": True, "added": added, "not_found": not_found})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
