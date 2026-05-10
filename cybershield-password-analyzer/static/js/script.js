/* ═══════════════════════════════════════════
   CyberShield – Frontend Logic
   ═══════════════════════════════════════════ */

"use strict";

// ── DOM refs ──────────────────────────────────────────────────────────
const passwordInput    = document.getElementById("passwordInput");
const toggleVisBtn     = document.getElementById("toggleVisibility");
const meterFill        = document.getElementById("meterFill");
const meterGlow        = document.getElementById("meterGlow");
const scoreText        = document.getElementById("scoreText");
const entropyText      = document.getElementById("entropyText");
const lengthText       = document.getElementById("lengthText");
const strengthBadge    = document.getElementById("strengthBadge");
const recsList         = document.getElementById("recsList");
const crackTableBody   = document.getElementById("crackTableBody");
const commonWarning    = document.getElementById("commonWarning");
const genOutput        = document.getElementById("genOutput");
const btnGenerate      = document.getElementById("btnGenerate");
const btnCopy          = document.getElementById("btnCopy");
const btnUseGenerated  = document.getElementById("btnUseGenerated");
const genLengthSlider  = document.getElementById("genLength");
const lenVal           = document.getElementById("lenVal");
const modeTabs         = document.querySelectorAll(".mode-tab");
const toggleChips      = document.querySelectorAll(".toggle-chip");
const lengthRow        = document.getElementById("lengthRow");
const charToggles      = document.getElementById("charToggles");

// ── State ─────────────────────────────────────────────────────────────
let generatedPassword = "";
let currentMode       = "random";
let debounceTimer     = null;

const CHECK_KEYS = [
  "length_8", "length_12", "has_upper",
  "has_lower", "has_digit", "has_special",
  "no_repeating", "no_sequential",
];

// ── Level → CSS class map ──────────────────────────────────────────────
const LEVEL_CLASS = {
  "Weak":       "level-weak",
  "Fair":       "level-fair",
  "Good":       "level-good",
  "Strong":     "level-strong",
  "Very Strong":"level-verystrong",
};

// ── Toggle password visibility ─────────────────────────────────────────
toggleVisBtn.addEventListener("click", () => {
  const type = passwordInput.type === "password" ? "text" : "password";
  passwordInput.type = type;
});

// ── Real-time analysis ────────────────────────────────────────────────
passwordInput.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => analyzePassword(passwordInput.value), 120);
});

async function analyzePassword(password) {
  if (!password) {
    resetUI();
    return;
  }
  try {
    const res  = await fetch("/api/analyze", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ password }),
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.error("Analyze error:", err);
  }
}

// ── Render analysis results ───────────────────────────────────────────
function renderResults(data) {
  const { score, level, color, checks, recommendations, is_common, entropy, length, crack_times } = data;

  // Meter
  meterFill.style.width      = score + "%";
  meterGlow.style.width      = score + "%";
  meterFill.style.background = color;
  meterGlow.style.background = color;

  // Stats
  scoreText.textContent   = score + "%";
  entropyText.textContent = (entropy || 0) + " bits entropy";
  lengthText.textContent  = (length || 0) + " chars";

  // Badge
  strengthBadge.textContent = level;
  strengthBadge.className = "strength-badge " + (LEVEL_CLASS[level] || "");

  // Checklist
  CHECK_KEYS.forEach(key => {
    const el = document.getElementById("chk-" + key);
    if (!el) return;
    const icon = el.querySelector(".check-icon");
    if (checks[key]) {
      el.className = "check-item pass";
      icon.textContent = "✓";
    } else {
      el.className = "check-item fail";
      icon.textContent = "✗";
    }
  });

  // Common warning
  is_common
    ? commonWarning.classList.remove("hidden")
    : commonWarning.classList.add("hidden");

  // Recommendations
  recsList.innerHTML = "";
  (recommendations || []).forEach(rec => {
    const li = document.createElement("li");
    li.className = "rec-item";
    li.textContent = rec;
    recsList.appendChild(li);
  });

  // Crack times
  if (crack_times && Object.keys(crack_times).length) {
    crackTableBody.innerHTML = "";
    Object.entries(crack_times).forEach(([scenario, time]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${scenario}</td><td>${time}</td>`;
      crackTableBody.appendChild(tr);
    });
  }
}

// ── Reset UI to empty state ───────────────────────────────────────────
function resetUI() {
  meterFill.style.width = "0%";
  meterGlow.style.width = "0%";
  scoreText.textContent   = "0%";
  entropyText.textContent = "0 bits entropy";
  lengthText.textContent  = "0 chars";
  strengthBadge.textContent = "—";
  strengthBadge.className   = "strength-badge";

  CHECK_KEYS.forEach(key => {
    const el = document.getElementById("chk-" + key);
    if (!el) return;
    el.className = "check-item";
    el.querySelector(".check-icon").textContent = "○";
  });

  commonWarning.classList.add("hidden");

  recsList.innerHTML = `<li class="rec-item mono placeholder">Awaiting password input…</li>`;
  crackTableBody.innerHTML = `<tr><td colspan="2" class="mono placeholder">—</td></tr>`;
}

// ── Generator: mode tabs ──────────────────────────────────────────────
modeTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    modeTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    currentMode = tab.dataset.mode;

    if (currentMode === "passphrase") {
      lengthRow.style.display   = "none";
      charToggles.style.display = "none";
    } else {
      lengthRow.style.display   = "";
      charToggles.style.display = "";
    }
  });
});

// ── Generator: length slider ──────────────────────────────────────────
genLengthSlider.addEventListener("input", () => {
  lenVal.textContent = genLengthSlider.value;
});

// ── Generator: character toggles ──────────────────────────────────────
toggleChips.forEach(chip => {
  chip.addEventListener("click", () => {
    chip.classList.toggle("active");
  });
});

function getToggleState() {
  const state = {};
  toggleChips.forEach(chip => {
    state[chip.dataset.key] = chip.classList.contains("active");
  });
  return state;
}

// ── Generate password ─────────────────────────────────────────────────
btnGenerate.addEventListener("click", generatePassword);

async function generatePassword() {
  const toggleState = getToggleState();
  const body = {
    mode:    currentMode,
    length:  parseInt(genLengthSlider.value, 10),
    upper:   toggleState.upper   !== false,
    lower:   toggleState.lower   !== false,
    digits:  toggleState.digits  !== false,
    special: toggleState.special !== false,
    words:   4,
  };

  try {
    btnGenerate.disabled = true;
    btnGenerate.textContent = "…";

    const res  = await fetch("/api/generate", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(body),
    });
    const data = await res.json();

    generatedPassword = data.password || "";
    genOutput.textContent = generatedPassword;
    genOutput.classList.add("has-value");

    // Also render its analysis
    renderResults(data);

  } catch (err) {
    console.error("Generate error:", err);
    genOutput.textContent = "Error – check server";
  } finally {
    btnGenerate.disabled = false;
    btnGenerate.textContent = "⚡ Generate";
  }
}

// ── Copy to clipboard ─────────────────────────────────────────────────
btnCopy.addEventListener("click", async () => {
  if (!generatedPassword) return;
  try {
    await navigator.clipboard.writeText(generatedPassword);
    btnCopy.classList.add("copied");
    setTimeout(() => btnCopy.classList.remove("copied"), 1500);
  } catch {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = generatedPassword;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
});

// ── Use generated password ────────────────────────────────────────────
btnUseGenerated.addEventListener("click", () => {
  if (!generatedPassword) return;
  passwordInput.value = generatedPassword;
  passwordInput.type  = "text"; // show it since it was generated
  analyzePassword(generatedPassword);
  passwordInput.focus();
});
