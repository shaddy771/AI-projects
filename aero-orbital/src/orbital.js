export const TEMP_MIN = 16
export const TEMP_MAX = 30
export const TEMP_COMFORT = 22

export function applyTemperatureTheme(ratio) {
  const t = Math.min(1, Math.max(0, ratio))

  const lerp = (a, b) => Math.round(a + (b - a) * t)
  const rgb = (r, g, b) => `rgb(${r} ${g} ${b})`
  const rgba = (r, g, b, a) => `rgb(${r} ${g} ${b} / ${a})`

  // Cold: dull blue · Warm: dull orange
  const bg = [lerp(22, 32, t), lerp(28, 24, t), lerp(38, 20, t)]
  const bgSoft = [lerp(28, 40, t), lerp(36, 30, t), lerp(46, 26, t)]
  const accent = [lerp(58, 118, t), lerp(82, 88, t), lerp(104, 62, t)]
  const accentDeep = [lerp(42, 92, t), lerp(62, 68, t), lerp(78, 48, t)]
  const ink = [lerp(214, 236, t), lerp(222, 228, t), lerp(232, 214, t)]
  const inkSoft = [lerp(130, 168, t), lerp(148, 152, t), lerp(168, 132, t)]
  const glow = [lerp(48, 108, t), lerp(72, 78, t), lerp(96, 52, t)]

  const root = document.documentElement
  root.style.setProperty('--bg', rgb(...bg))
  root.style.setProperty('--bg-soft', rgb(...bgSoft))
  root.style.setProperty('--accent', rgb(...accent))
  root.style.setProperty('--accent-deep', rgb(...accentDeep))
  root.style.setProperty('--ink', rgb(...ink))
  root.style.setProperty('--ink-soft', rgb(...inkSoft))
  root.style.setProperty('--glow', rgba(...glow, 0.35))
  root.style.setProperty('--line', rgba(...ink, 0.1))
  root.style.setProperty('--temp-ratio', String(t))
}

export function createOrbitalDial(root, { onChange } = {}) {
  let temp = TEMP_COMFORT
  let dragging = false

  const size = 320
  const cx = size / 2
  const cy = size / 2
  const radius = 118
  const startAngle = 135
  const endAngle = 405
  const span = endAngle - startAngle

  const polar = (angleDeg, r = radius) => {
    const rad = (angleDeg * Math.PI) / 180
    return {
      x: cx + r * Math.cos(rad),
      y: cy + r * Math.sin(rad),
    }
  }

  const tempToAngle = (value) => startAngle + ((value - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)) * span

  const angleToTemp = (angle) => {
    let a = angle
    while (a < startAngle) a += 360
    while (a > endAngle) {
      const distStart = Math.abs(a - startAngle)
      const distEnd = Math.abs(a - endAngle)
      a = distStart < distEnd ? startAngle : endAngle
    }
    const ratio = (a - startAngle) / span
    return Math.round(TEMP_MIN + ratio * (TEMP_MAX - TEMP_MIN))
  }

  const arcPath = (fromAngle, toAngle, r = radius) => {
    const start = polar(fromAngle, r)
    const end = polar(toAngle, r)
    const large = toAngle - fromAngle > 180 ? 1 : 0
    return `M ${start.x} ${start.y} A ${r} ${r} 0 ${large} 1 ${end.x} ${end.y}`
  }

  const shell = document.createElement('div')
  shell.className = 'orbital'
  shell.innerHTML = `
    <svg class="orbital-svg" viewBox="0 0 ${size} ${size}" aria-hidden="true">
      <defs>
        <linearGradient id="orbital-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="var(--accent-deep)" />
          <stop offset="100%" stop-color="var(--accent)" />
        </linearGradient>
        <filter id="orbital-glow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <circle class="orbital-track-bg" cx="${cx}" cy="${cy}" r="${radius}" />
      <path class="orbital-track" data-track />
      <path class="orbital-active" data-active filter="url(#orbital-glow)" />
      <circle class="orbital-comfort-mark" data-comfort r="4" />
    </svg>

    <button class="orbital-knob" type="button" data-knob aria-label="Крутите для настройки температуры">
      <span class="orbital-knob-dial" data-knob-dial>
        <span class="orbital-knob-notch" aria-hidden="true"></span>
        ${Array.from({ length: 24 }, (_, i) => `<span class="orbital-knob-tick" style="--i:${i}"></span>`).join('')}
      </span>
      <span class="orbital-knob-readout">
        <span class="orbital-value" data-value>${temp}</span>
        <span class="orbital-unit">°C</span>
      </span>
    </button>

    <p class="orbital-status" data-status>Комфорт</p>
  `

  root.appendChild(shell)

  const track = shell.querySelector('[data-track]')
  const active = shell.querySelector('[data-active]')
  const comfortMark = shell.querySelector('[data-comfort]')
  const knob = shell.querySelector('[data-knob]')
  const knobDial = shell.querySelector('[data-knob-dial]')
  const valueEl = shell.querySelector('[data-value]')
  const statusEl = shell.querySelector('[data-status]')

  const comfortPoint = polar(tempToAngle(TEMP_COMFORT), radius)
  track.setAttribute('d', arcPath(startAngle, endAngle))
  comfortMark.setAttribute('cx', comfortPoint.x)
  comfortMark.setAttribute('cy', comfortPoint.y)

  const moodForTemp = (value) => {
    if (value <= 19) return { label: 'Прохладно', mode: 'cool' }
    if (value <= 23) return { label: 'Комфорт', mode: 'comfort' }
    if (value <= 26) return { label: 'Тепло', mode: 'warm' }
    return { label: 'Жарко', mode: 'hot' }
  }

  const render = () => {
    const angle = tempToAngle(temp)
    const ratio = (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)
    const mood = moodForTemp(temp)
    const knobRotation = angle - 270

    active.setAttribute('d', arcPath(startAngle, angle))
    knobDial.style.transform = `rotate(${knobRotation}deg)`
    valueEl.textContent = String(temp)
    statusEl.textContent = mood.label
    shell.dataset.mode = mood.mode

    applyTemperatureTheme(ratio)
    onChange?.(temp, mood, ratio)
  }

  const setTemp = (next) => {
    temp = Math.min(TEMP_MAX, Math.max(TEMP_MIN, next))
    render()
  }

  const angleFromEvent = (event) => {
    const rect = shell.getBoundingClientRect()
    const scale = size / rect.width
    const x = (event.clientX - rect.left) * scale
    const y = (event.clientY - rect.top) * scale
    return (Math.atan2(y - cy, x - cx) * 180) / Math.PI
  }

  const onPointerMove = (event) => {
    if (!dragging) return
    event.preventDefault()
    setTemp(angleToTemp(angleFromEvent(event)))
  }

  const stopDrag = () => {
    dragging = false
    shell.classList.remove('is-dragging')
    window.removeEventListener('pointermove', onPointerMove)
    window.removeEventListener('pointerup', stopDrag)
    window.removeEventListener('pointercancel', stopDrag)
  }

  const startDrag = (event) => {
    dragging = true
    shell.classList.add('is-dragging')
    knob.setPointerCapture?.(event.pointerId)
    setTemp(angleToTemp(angleFromEvent(event)))
    window.addEventListener('pointermove', onPointerMove, { passive: false })
    window.addEventListener('pointerup', stopDrag)
    window.addEventListener('pointercancel', stopDrag)
  }

  knob.addEventListener('pointerdown', startDrag)

  shell.addEventListener(
    'wheel',
    (event) => {
      event.preventDefault()
      setTemp(temp + (event.deltaY > 0 ? 1 : -1))
    },
    { passive: false }
  )

  render()

  requestAnimationFrame(() => {
    shell.classList.add('is-ready')
    let frame = 0
    const from = 28
    const tick = () => {
      frame += 1
      const t = Math.min(1, frame / 50)
      const eased = 1 - (1 - t) ** 3
      setTemp(Math.round(from + (TEMP_COMFORT - from) * eased))
      if (t < 1) requestAnimationFrame(tick)
    }
    setTimeout(() => requestAnimationFrame(tick), 500)
  })

  return { setTemp, getTemp: () => temp, shell }
}
