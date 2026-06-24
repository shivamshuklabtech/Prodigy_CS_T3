"""
  Password Complexity Checker
A single-file Flask app: Python backend serves the API and the
frontend (HTML/CSS/JS) is embedded as a template string.

Run:
    pip install flask --break-system-packages
    python password_checker_app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "letmein", "admin",
    "welcome", "123456789", "12345678", "iloveyou",
}

SYMBOL_RE = re.compile(r"""[!@#$%^&*(),.?":{}|<>_\-+=~`\[\];'/\\]""")


def evaluate_password(password: str):
    checks = {
        "length12": len(password) >= 12,
        "length8": len(password) >= 8,
        "upper": bool(re.search(r"[A-Z]", password)),
        "lower": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"[0-9]", password)),
        "symbol": bool(SYMBOL_RE.search(password)),
    }

    score = 0
    if checks["length12"]:
        score += 2
    elif checks["length8"]:
        score += 1
    score += sum([checks["upper"], checks["lower"], checks["digit"], checks["symbol"]])

    is_common = password.lower() in COMMON_PASSWORDS
    if is_common:
        score = 0

    feedback = []
    if is_common:
        feedback.append("This is a commonly leaked password. Choose something unique.")
    else:
        if not checks["length8"]:
            feedback.append("Too short — use at least 8 characters.")
        elif not checks["length12"]:
            feedback.append("Stretch it to 12+ characters for a tighter fit.")
        if not checks["upper"]:
            feedback.append("Add an uppercase letter (A–Z).")
        if not checks["lower"]:
            feedback.append("Add a lowercase letter (a–z).")
        if not checks["digit"]:
            feedback.append("Add a number (0–9).")
        if not checks["symbol"]:
            feedback.append("Add a symbol, e.g. ! @ # $.")

    if len(password) == 0:
        label = "Empty"
    elif score <= 2:
        label = "Weak"
    elif score <= 4:
        label = "Moderate"
    elif score == 5:
        label = "Strong"
    else:
        label = "Very strong"

    return {
        "checks": checks,
        "score": score,
        "max_score": 6,
        "label": label,
        "feedback": feedback,
        "length": len(password),
    }


@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str):
        return jsonify({"error": "password must be a string"}), 400
    return jsonify(evaluate_password(password))


@app.route("/")
def index():
    return render_template_string(PAGE_TEMPLATE)


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Tumbler — Password Strength</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --charcoal:#1c1b1a;
    --charcoal-2:#242220;
    --brass:#c8932b;
    --steel:#5c7a8a;
    --bone:#ece7dd;
    --bone-dim:#a8a299;
    --danger:#b9523f;
    --success:#6b9450;
    --line: rgba(236,231,221,0.12);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{
    background:var(--charcoal);
    color:var(--bone);
    font-family:'JetBrains Mono', monospace;
    min-height:100vh;
    -webkit-font-smoothing:antialiased;
  }
  body{
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:5vh 6vw 8vh;
    background-image:
      radial-gradient(circle at 15% 10%, rgba(200,147,43,0.06), transparent 40%),
      radial-gradient(circle at 85% 90%, rgba(92,122,138,0.07), transparent 45%);
  }
  .wrap{ width:100%; max-width:620px; }

  .eyebrow{
    font-size:11px;
    letter-spacing:0.22em;
    text-transform:uppercase;
    color:var(--brass);
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:18px;
  }
  .eyebrow::before{
    content:"";
    width:18px; height:1px;
    background:var(--brass);
    display:inline-block;
  }

  h1{
    font-family:'Fraunces', serif;
    font-weight:700;
    font-optical-sizing:auto;
    font-size:clamp(2.2rem, 6vw, 3.4rem);
    line-height:1.05;
    letter-spacing:-0.01em;
    color:var(--bone);
    margin-bottom:14px;
  }
  h1 em{
    font-style:italic;
    font-weight:400;
    color:var(--brass);
  }

  .sub{
    color:var(--bone-dim);
    font-size:14px;
    line-height:1.6;
    max-width:46ch;
    margin-bottom:48px;
  }

  .keyway{
    position:relative;
    border:1px solid var(--line);
    background:var(--charcoal-2);
    border-radius:4px;
    padding:4px;
    margin-bottom:8px;
    transition:border-color .25s ease;
  }
  .keyway:focus-within{
    border-color:var(--brass);
  }
  .keyway-inner{
    display:flex;
    align-items:center;
    gap:12px;
    padding:14px 16px;
  }
  .keyway-inner svg{ flex-shrink:0; opacity:0.55; }
  .keyway:focus-within .keyway-inner svg{ opacity:1; stroke:var(--brass); }

  input[type="password"], input[type="text"]{
    flex:1;
    background:transparent;
    border:none;
    outline:none;
    color:var(--bone);
    font-family:'JetBrains Mono', monospace;
    font-size:16px;
    letter-spacing:0.04em;
  }
  input::placeholder{ color:var(--bone-dim); opacity:0.6; }

  .toggle-vis{
    background:none;
    border:none;
    color:var(--bone-dim);
    font-size:11px;
    letter-spacing:0.08em;
    text-transform:uppercase;
    cursor:pointer;
    font-family:'JetBrains Mono', monospace;
    padding:6px 8px;
  }
  .toggle-vis:hover{ color:var(--brass); }
  *:focus-visible{ outline:2px solid var(--brass); outline-offset:2px; }

  .hint-row{
    display:flex;
    justify-content:space-between;
    font-size:11px;
    color:var(--bone-dim);
    letter-spacing:0.05em;
    margin-bottom:44px;
  }

  .lock-panel{
    display:flex;
    align-items:flex-end;
    gap:14px;
    height:120px;
    border-bottom:1px solid var(--line);
    padding-bottom:0;
    margin-bottom:18px;
  }
  .pin{
    flex:1;
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:10px;
    height:100%;
    justify-content:flex-end;
  }
  .pin-shaft{
    width:14px;
    height:84px;
    background:linear-gradient(180deg, #2c2a27, #1a1917);
    border:1px solid var(--line);
    border-bottom:none;
    border-radius:3px 3px 0 0;
    position:relative;
    overflow:hidden;
    display:flex;
    align-items:flex-end;
  }
  .pin-fill{
    width:100%;
    height:0%;
    background:linear-gradient(180deg, var(--brass), #9a6f1f);
    transition:height .5s cubic-bezier(.22,1,.36,1), background .3s ease;
  }
  .pin.set .pin-fill{ height:100%; }
  .pin.set .pin-shaft{ box-shadow:0 0 14px rgba(200,147,43,0.35); }
  .pin-label{
    font-size:9px;
    letter-spacing:0.08em;
    text-transform:uppercase;
    color:var(--bone-dim);
    text-align:center;
    line-height:1.4;
  }
  .pin.set .pin-label{ color:var(--brass); }

  .status-row{
    display:flex;
    align-items:baseline;
    justify-content:space-between;
    margin-bottom:6px;
  }
  .status-label{
    font-family:'Fraunces', serif;
    font-weight:600;
    font-size:22px;
    transition:color .3s ease;
  }
  .status-score{
    font-size:11px;
    color:var(--bone-dim);
    letter-spacing:0.05em;
  }
  .status-weak{ color:var(--danger); }
  .status-moderate{ color:var(--brass); }
  .status-strong, .status-verystrong{ color:var(--success); }

  .bar-track{
    width:100%;
    height:3px;
    background:var(--line);
    border-radius:2px;
    overflow:hidden;
    margin-bottom:28px;
  }
  .bar-fill{
    height:100%;
    width:0%;
    background:var(--danger);
    transition:width .5s cubic-bezier(.22,1,.36,1), background .4s ease;
  }

  .feedback{
    list-style:none;
    display:flex;
    flex-direction:column;
    gap:9px;
  }
  .feedback li{
    font-size:13px;
    color:var(--bone-dim);
    display:flex;
    gap:10px;
    line-height:1.5;
  }
  .feedback li::before{
    content:"—";
    color:var(--steel);
    flex-shrink:0;
  }
  .feedback.ok li{ color:var(--success); }
  .feedback.ok li::before{ content:"✓"; color:var(--success); }

  .api-note{
    margin-top:8px;
    font-size:10px;
    color:var(--bone-dim);
    opacity:0.6;
  }

  footer{
    margin-top:64px;
    font-size:10px;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color:var(--bone-dim);
    opacity:0.5;
  }

  @media (prefers-reduced-motion: reduce){
    .pin-fill, .bar-fill{ transition:none; }
  }

  @media (max-width:480px){
    .lock-panel{ gap:8px; }
    .pin-shaft{ width:10px; }
    .pin-label{ font-size:8px; }
  }
</style>
</head>
<body>
  <div class="wrap">
    <div class="eyebrow">Task 03 — Password Complexity Checker</div>
    <h1>How strong is<br/>your <em>lock?</em></h1>
    <p class="sub">Type a password below. Five pins must seat in place — length, uppercase, lowercase, a number, and a symbol — before the tumbler turns. Every check runs on the Python server.</p>

    <label class="keyway" for="pw">
      <div class="keyway-inner">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
          <rect x="3" y="11" width="18" height="10" rx="1.5"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
        <input id="pw" type="password" placeholder="Enter a password to test" autocomplete="off" spellcheck="false" />
        <button class="toggle-vis" id="toggleVis" type="button" aria-label="Show password">Show</button>
      </div>
    </label>
    <div class="hint-row">
      <span id="charCount">0 characters</span>
      <span id="netStatus">Server ready</span>
    </div>

    <div class="lock-panel" id="lockPanel" aria-hidden="true">
      <div class="pin" data-pin="length12"><div class="pin-shaft"><div class="pin-fill"></div></div><div class="pin-label">12+<br/>chars</div></div>
      <div class="pin" data-pin="upper"><div class="pin-shaft"><div class="pin-fill"></div></div><div class="pin-label">Upper</div></div>
      <div class="pin" data-pin="lower"><div class="pin-shaft"><div class="pin-fill"></div></div><div class="pin-label">Lower</div></div>
      <div class="pin" data-pin="digit"><div class="pin-shaft"><div class="pin-fill"></div></div><div class="pin-label">Number</div></div>
      <div class="pin" data-pin="symbol"><div class="pin-shaft"><div class="pin-fill"></div></div><div class="pin-label">Symbol</div></div>
    </div>

    <div class="status-row">
      <span class="status-label status-weak" id="statusLabel">Empty</span>
      <span class="status-score" id="statusScore">0 / 6 pins seated</span>
    </div>
    <div class="bar-track"><div class="bar-fill" id="barFill"></div></div>

    <ul class="feedback" id="feedback">
      <li>Start typing to test a password.</li>
    </ul>
    <div class="api-note">Checked via POST /api/check — nothing is stored.</div>

    <footer>password complexity checker</footer>
  </div>

<script>
  const pwInput = document.getElementById('pw');
  const toggleVis = document.getElementById('toggleVis');
  const charCount = document.getElementById('charCount');
  const netStatus = document.getElementById('netStatus');
  const statusLabel = document.getElementById('statusLabel');
  const statusScore = document.getElementById('statusScore');
  const barFill = document.getElementById('barFill');
  const feedbackList = document.getElementById('feedback');
  const pins = {
    length12: document.querySelector('[data-pin="length12"]'),
    upper: document.querySelector('[data-pin="upper"]'),
    lower: document.querySelector('[data-pin="lower"]'),
    digit: document.querySelector('[data-pin="digit"]'),
    symbol: document.querySelector('[data-pin="symbol"]'),
  };

  toggleVis.addEventListener('click', () => {
    const isPw = pwInput.type === 'password';
    pwInput.type = isPw ? 'text' : 'password';
    toggleVis.textContent = isPw ? 'Hide' : 'Show';
    toggleVis.setAttribute('aria-label', isPw ? 'Hide password' : 'Show password');
  });

  function render(result, length){
    charCount.textContent = `${length} character${length===1?'':'s'}`;

    Object.keys(pins).forEach(key => {
      pins[key].classList.toggle('set', !!result.checks[key]);
    });

    statusLabel.textContent = result.label;
    let cls = 'status-weak';
    if(result.label === 'Moderate') cls = 'status-moderate';
    else if(result.label === 'Strong') cls = 'status-strong';
    else if(result.label === 'Very strong') cls = 'status-verystrong';
    statusLabel.className = 'status-label ' + cls;
    statusScore.textContent = `${result.score} / ${result.max_score} pins seated`;

    const pct = Math.min(result.score, result.max_score) / result.max_score * 100;
    barFill.style.width = pct + '%';
    barFill.style.background = result.score <= 2 ? 'var(--danger)' : result.score <= 4 ? 'var(--brass)' : 'var(--success)';

    feedbackList.innerHTML = '';
    const ok = result.feedback.length === 0 && length > 0;
    feedbackList.classList.toggle('ok', ok);
    if(length === 0){
      const li = document.createElement('li');
      li.textContent = 'Start typing to test a password.';
      feedbackList.appendChild(li);
      feedbackList.classList.remove('ok');
      return;
    }
    const items = ok ? ['All five pins are seated. Strong lock.'] : result.feedback;
    items.forEach(text => {
      const li = document.createElement('li');
      li.textContent = text;
      feedbackList.appendChild(li);
    });
  }

  let debounceTimer = null;
  pwInput.addEventListener('input', e => {
    const password = e.target.value;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => checkPassword(password), 120);
  });

  async function checkPassword(password){
    if(password.length === 0){
      render({checks:{}, score:0, max_score:6, label:'Empty', feedback:[]}, 0);
      netStatus.textContent = 'Server ready';
      return;
    }
    try{
      netStatus.textContent = 'Checking…';
      const res = await fetch('/api/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });
      const data = await res.json();
      render(data, password.length);
      netStatus.textContent = 'Server ready';
    }catch(err){
      netStatus.textContent = 'Offline — check server';
    }
  }

  render({checks:{}, score:0, max_score:6, label:'Empty', feedback:[]}, 0);
</script>
</body>
</html>
"""


if __name__ == "__main__":
  # On Windows the reloader can sometimes cause issues; disable it and
  # bind explicitly to localhost. This makes running `python app.py`
  # more reliable in common environments.
  app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)