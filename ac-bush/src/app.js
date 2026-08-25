export function mountApp(root) {
  root.innerHTML = `
    <div class="heat-alert" data-alert>
      <span class="heat-alert-dot"></span>
      <span>Жара <strong>+38°</strong> — монтаж сегодня, доставка за 2 часа</span>
    </div>

    <header class="site-header">
      <a class="logo" href="#top">FROST<span>BITE</span></a>
      <nav class="nav">
        <a href="#typhoon">Мощность</a>
        <a href="#models">Модели</a>
        <a class="nav-cta" href="#order">Заморозить цену</a>
      </nav>
    </header>

    <main id="top">
      <section class="hero" aria-label="Жара против холода">
        <div class="compare" data-compare style="--pos: 58%">
          <div class="compare-layer compare-cold">
            <img src="/hero-cold.png" alt="Комната после кондиционера — прохладно и комфортно" draggable="false" />
            <span class="tag tag-cold">Холод</span>
          </div>
          <div class="compare-layer compare-hot" data-hot>
            <img src="/hero-hot.png" alt="Комната в жару — душно и некомфортно" draggable="false" />
            <span class="tag tag-hot">Жара</span>
          </div>
          <div class="compare-divider" aria-hidden="true">
            <button class="compare-handle" type="button" data-handle aria-label="Сравнить жару и холод">
              <span aria-hidden="true">⇄</span>
            </button>
          </div>
          <input class="compare-range" data-range type="range" min="4" max="96" value="58" aria-label="Сравнение жары и холода" />
        </div>

        <div class="hero-overlay">
          <p class="hero-brand">FROSTBITE</p>
          <h1>Жара сгорит сегодня</h1>
          <p class="hero-lede">Сдвинь линию — и почувствуй, как комната выдыхает. Кондиционеры с монтажом в день заказа.</p>
          <div class="hero-cta">
            <a class="btn btn-fire" href="#order">Заморозить цену −30%</a>
            <a class="btn btn-ghost" href="#typhoon">Выдуй жару</a>
          </div>
        </div>

        <div class="hero-hint" aria-hidden="true">ТЯНИ <span>→</span></div>
      </section>

      <section class="section typhoon" id="typhoon" aria-label="Мощность охлаждения">
        <div class="section-inner typhoon-grid">
          <div class="typhoon-copy">
            <p class="eyebrow eyebrow-ice">Typhoon Cool</p>
            <h2>Выдуй жару за окно</h2>
            <p class="section-lede">
              Сплит-система FROSTBITE Arctic 12 — до 35 м², охлаждение за 8 минут.
              Нажми «Включить холод» и смотри, как падает температура.
            </p>
            <button class="btn btn-ice" type="button" data-blast>Включить холод</button>
            <ul class="specs">
              <li><strong>12 000 BTU</strong> мощность</li>
              <li><strong>A++</strong> класс</li>
              <li><strong>19 dB</strong> ночной режим</li>
            </ul>
          </div>

          <div class="typhoon-stage" data-stage>
            <div class="ac-unit" aria-hidden="true">
              <div class="ac-body">
                <div class="ac-vent"></div>
                <div class="ac-vent"></div>
                <div class="ac-vent"></div>
              </div>
              <div class="ac-glow"></div>
            </div>
            <div class="cold-blast" data-blast-visual aria-hidden="true">
              ${Array.from({ length: 14 }, (_, i) => `<span class="streak" style="--i:${i}"></span>`).join('')}
            </div>
            <div class="thermo" data-thermo aria-live="polite">
              <div class="thermo-bar">
                <div class="thermo-fill" data-thermo-fill></div>
              </div>
              <div class="thermo-readout">
                <span class="thermo-value" data-thermo-value>38</span>
                <span class="thermo-unit">°C</span>
              </div>
              <p class="thermo-label">в комнате</p>
            </div>
            <div class="price-tag">
              <span class="price-old">28 990 ₽</span>
              <span class="price-new">19 990 ₽</span>
              <span class="price-note">монтаж в подарок</span>
            </div>
          </div>
        </div>
      </section>

      <section class="section models" id="models">
        <div class="section-inner">
          <p class="eyebrow">Модели</p>
          <h2>Выбери свой холод</h2>
          <ul class="model-list">
            <li>
              <span class="model-name">Arctic 09</span>
              <span class="model-area">до 25 м²</span>
              <span class="model-price">16 990 ₽</span>
            </li>
            <li class="model-hit">
              <span class="model-badge">Хит</span>
              <span class="model-name">Arctic 12</span>
              <span class="model-area">до 35 м²</span>
              <span class="model-price">19 990 ₽</span>
            </li>
            <li>
              <span class="model-name">Arctic 18</span>
              <span class="model-area">до 50 м²</span>
              <span class="model-price">27 990 ₽</span>
            </li>
          </ul>
        </div>
      </section>

      <section class="section order" id="order">
        <div class="section-inner order-panel">
          <p class="eyebrow eyebrow-fire">Заморозка цены</p>
          <h2>Забронируй холод на сегодня</h2>
          <p class="section-lede">Оставь номер — перезвоним за 5 минут и зафиксируем скидку −30%.</p>
          <form class="order-form" data-form>
            <label>
              <span>Телефон</span>
              <input type="tel" name="phone" placeholder="+7 (___) ___-__-__" required />
            </label>
            <label>
              <span>Площадь</span>
              <select name="area" required>
                <option value="" disabled selected>Комната</option>
                <option value="25">до 25 м²</option>
                <option value="35">до 35 м²</option>
                <option value="50">до 50 м²</option>
              </select>
            </label>
            <button class="btn btn-fire" type="submit">Заморозить −30%</button>
          </form>
          <p class="form-note" data-note hidden>Готово! Мастер уже морозит вашу заявку.</p>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <span>FROSTBITE</span>
      <span>Кондиционеры · монтаж · сервис</span>
    </footer>
  `

  initCompare(root)
  initTyphoon(root)
  initForm(root)
  initReveal(root)
}

function initCompare(root) {
  const compare = root.querySelector('[data-compare]')
  const range = root.querySelector('[data-range]')
  const handle = root.querySelector('[data-handle]')
  if (!compare || !range) return

  const setPos = (value) => {
    const clamped = Math.min(96, Math.max(4, Number(value)))
    compare.style.setProperty('--pos', `${clamped}%`)
    range.value = String(clamped)
    compare.dataset.mode = clamped < 35 ? 'cold' : clamped > 65 ? 'hot' : 'mid'
  }

  setPos(range.value)

  range.addEventListener('input', (e) => setPos(e.target.value))

  let dragging = false
  const posFromEvent = (event) => {
    const rect = compare.getBoundingClientRect()
    const x = 'touches' in event ? event.touches[0].clientX : event.clientX
    return ((x - rect.left) / rect.width) * 100
  }

  const onMove = (event) => {
    if (!dragging) return
    event.preventDefault()
    setPos(posFromEvent(event))
  }

  const stop = () => {
    dragging = false
    compare.classList.remove('is-dragging')
  }

  const start = (event) => {
    if (event.target.closest('.hero-overlay a, .hero-cta')) return
    dragging = true
    compare.classList.add('is-dragging')
    setPos(posFromEvent(event))
  }

  handle?.addEventListener('pointerdown', (e) => {
    handle.setPointerCapture?.(e.pointerId)
    start(e)
  })

  compare.addEventListener('pointerdown', (e) => {
    if (e.target === range) return
    start(e)
  })

  window.addEventListener('pointermove', onMove, { passive: false })
  window.addEventListener('pointerup', stop)
  window.addEventListener('pointercancel', stop)

  requestAnimationFrame(() => {
    compare.classList.add('is-ready')
    let frame = 0
    const from = 82
    const to = 58
    const tick = () => {
      frame += 1
      const t = Math.min(1, frame / 40)
      const eased = 1 - (1 - t) ** 3
      setPos(from + (to - from) * eased)
      if (t < 1) requestAnimationFrame(tick)
    }
    setTimeout(() => requestAnimationFrame(tick), 400)
  })
}

function initTyphoon(root) {
  const btn = root.querySelector('[data-blast]')
  const stage = root.querySelector('[data-stage]')
  const visual = root.querySelector('[data-blast-visual]')
  const valueEl = root.querySelector('[data-thermo-value]')
  const fillEl = root.querySelector('[data-thermo-fill]')
  if (!btn || !stage || !valueEl || !fillEl) return

  let running = false

  const runBlast = () => {
    if (running) return
    running = true
    stage.classList.add('is-blasting')
    visual?.classList.add('is-active')

    const from = 38
    const to = 22
    const duration = 2200
    const start = performance.now()

    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration)
      const eased = 1 - (1 - t) ** 3
      const temp = Math.round(from + (to - from) * eased)
      valueEl.textContent = String(temp)
      fillEl.style.height = `${100 - ((temp - 18) / 22) * 100}%`
      if (t < 1) {
        requestAnimationFrame(tick)
      } else {
        running = false
      }
    }

    requestAnimationFrame(tick)
  }

  btn.addEventListener('click', runBlast)

  fillEl.style.height = `${100 - ((38 - 18) / 22) * 100}%`

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(runBlast, 600)
            io.disconnect()
          }
        })
      },
      { threshold: 0.45 }
    )
    io.observe(stage)
  }
}

function initForm(root) {
  const form = root.querySelector('[data-form]')
  const note = root.querySelector('[data-note]')
  if (!form) return

  form.addEventListener('submit', (e) => {
    e.preventDefault()
    form.hidden = true
    if (note) note.hidden = false
  })
}

function initReveal(root) {
  const items = root.querySelectorAll('.section, .model-list li')
  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-visible'))
    return
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          io.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.15 }
  )

  items.forEach((el) => io.observe(el))
}
