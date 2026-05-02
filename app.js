/**
 * Карточки: нечётный файл — вопрос, следующий чётный — ответ.
 * Маршрут: #/ — список; #/s/<индекс> — учёба.
 */

const els = {
  main: document.getElementById("main"),
  title: document.getElementById("page-title"),
  back: document.getElementById("btn-back"),
};

let manifest = null;

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function parseHash() {
  const h = window.location.hash.replace(/^#/, "") || "/";
  const parts = h.split("/").filter(Boolean);
  if (parts[0] === "s" && parts[1] !== undefined) {
    const si = parseInt(parts[1], 10);
    const ci = parts[2] !== undefined ? parseInt(parts[2], 10) : 0;
    return { view: "study", sectionIndex: si, cardIndex: Number.isFinite(ci) ? ci : 0 };
  }
  return { view: "home" };
}

function setHash(route) {
  window.location.hash = route;
}

function imgSrc(relPath) {
  const segments = relPath.split("/").map(encodeURIComponent);
  return segments.join("/");
}

async function loadManifest() {
  const res = await fetch("manifest.json", { cache: "no-store" });
  if (!res.ok) throw new Error("manifest");
  return res.json();
}

function renderHome() {
  els.title.textContent = "Разделы";
  els.back.classList.add("hidden");

  if (!manifest?.sections?.length) {
    els.main.innerHTML =
      '<div class="empty-state">Нет разделов. Запустите build_manifest.py</div>';
    return;
  }

  const list = document.createElement("div");
  list.className = "section-list";
  manifest.sections.forEach((sec, i) => {
    const n = sec.pairs?.length ?? 0;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "section-card";
    btn.innerHTML = `<h2>${esc(sec.title)}</h2><div class="meta">${n} карточек</div>`;
    btn.addEventListener("click", () => setHash(`/s/${i}/0`));
    list.appendChild(btn);
  });
  els.main.innerHTML = "";
  els.main.appendChild(list);
}

function renderStudy(sectionIndex, cardIndex) {
  const sec = manifest?.sections?.[sectionIndex];
  if (!sec || !sec.pairs?.length) {
    setHash("/");
    return;
  }

  const pairs = sec.pairs;
  let idx = Math.max(0, Math.min(cardIndex, pairs.length - 1));
  const pair = pairs[idx];

  els.title.textContent = sec.title;
  els.back.classList.remove("hidden");

  const total = pairs.length;
  const pct = ((idx + 1) / total) * 100;

  const qUrl = imgSrc(pair.q);
  const hasAnswer = pair.a != null;
  const aUrl = hasAnswer ? imgSrc(pair.a) : "";

  const wrap = document.createElement("div");
  wrap.className = "study";

  wrap.innerHTML = `
    <div class="progress-wrap">
      <div class="progress-bar" aria-hidden="true"><div class="progress-fill" style="width:${pct}%"></div></div>
      <span class="progress-text">${idx + 1} / ${total}</span>
    </div>
    <div class="flip-scene" id="flip-scene" role="button" tabindex="0" aria-label="Перевернуть карточку">
      <div class="flip-card" id="flip-card">
        <div class="flip-face front">
          <div class="face-label">Вопрос</div>
          <div class="img-wrap"><img src="${esc(qUrl)}" alt="Вопрос" loading="eager" decoding="async" /></div>
        </div>
        <div class="flip-face back">
          <div class="face-label answer">Ответ</div>
          <div class="img-wrap">
            ${
              hasAnswer
                ? `<img src="${esc(aUrl)}" alt="Ответ" loading="lazy" decoding="async" />`
                : '<p class="hint" style="padding:24px">Нет пары для этого файла</p>'
            }
          </div>
        </div>
      </div>
    </div>
    <p class="hint">Нажмите на карточку или «Ответ», чтобы перевернуть</p>
    <div class="controls">
      <button type="button" class="btn btn-secondary" id="btn-prev" ${idx <= 0 ? "disabled" : ""}>← Назад</button>
      <button type="button" class="btn btn-primary" id="btn-next" ${idx >= total - 1 ? "disabled" : ""}>Далее →</button>
      <button type="button" class="btn btn-flip btn-flip-row" id="btn-flip">Показать ответ</button>
    </div>
  `;

  els.main.innerHTML = "";
  els.main.appendChild(wrap);

  const flipCard = wrap.querySelector("#flip-card");
  const flipScene = wrap.querySelector("#flip-scene");
  let flipped = false;

  function setFlipped(on) {
    flipped = on;
    flipCard.classList.toggle("is-flipped", on);
    const bf = wrap.querySelector("#btn-flip");
    if (bf) bf.textContent = on ? "Показать вопрос" : "Показать ответ";
  }

  function toggleFlip() {
    setFlipped(!flipped);
  }

  flipScene.addEventListener("click", toggleFlip);
  flipScene.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      toggleFlip();
    }
  });

  wrap.querySelector("#btn-flip").addEventListener("click", (e) => {
    e.stopPropagation();
    toggleFlip();
  });

  wrap.querySelector("#btn-prev").addEventListener("click", () => {
    if (idx > 0) setHash(`/s/${sectionIndex}/${idx - 1}`);
  });
  wrap.querySelector("#btn-next").addEventListener("click", () => {
    if (idx < total - 1) setHash(`/s/${sectionIndex}/${idx + 1}`);
  });

  // Свайп
  let tx = 0;
  let startX = 0;
  flipScene.addEventListener(
    "touchstart",
    (e) => {
      startX = e.changedTouches[0].screenX;
    },
    { passive: true }
  );
  flipScene.addEventListener(
    "touchend",
    (e) => {
      tx = e.changedTouches[0].screenX - startX;
      if (Math.abs(tx) > 56) {
        if (tx < 0 && idx < total - 1) setHash(`/s/${sectionIndex}/${idx + 1}`);
        if (tx > 0 && idx > 0) setHash(`/s/${sectionIndex}/${idx - 1}`);
      }
    },
    { passive: true }
  );
}

function route() {
  const r = parseHash();
  if (r.view === "home") renderHome();
  else renderStudy(r.sectionIndex, r.cardIndex);
}

els.back.addEventListener("click", () => setHash("/"));

window.addEventListener("hashchange", route);

(async () => {
  try {
    manifest = await loadManifest();
  } catch {
    els.main.innerHTML =
      '<div class="error-state">Не найден manifest.json.<br />Запустите в этой папке:<br /><code style="font-size:0.85em">python build_manifest.py</code><br />и откройте сайт через локальный сервер (не file://).</div>';
    els.title.textContent = "Ошибка";
    els.back.classList.add("hidden");
    return;
  }
  route();
})();
