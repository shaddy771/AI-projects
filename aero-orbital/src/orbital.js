const TEMP_MIN = 16
const TEMP_MAX = 30
const TEMP_COMFORT = 22

export function createOrbitalDial(root, { onChange } = {}) {
  let temp = TEMP_COMFORT
  let dragging = false

  const svgNS = 'http://www.w3.org/2000/svg'
  const size = 320
  const cx = size / 2
  const cy = size / 2
  const radius = 118
  const stroke = 3
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
        <linearGradient id="orbital-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" class="grad-cool" />
          <stop offset="100%" class="grad-warm" />
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
    <button class="orbital-handle" type="button" data-handle aria-label="Настроить температуру">
      <span class="orbital-handle-core"></span>
    </button>
    <div class="orbital-center">
      <div class="ac-jewel" aria-hidden="true">
        <div class="ac-jewel-body">
          <span></span><span></span><span></span>
        </div>
      </div>
      <p class="orbital-value" data-value>${temp}</p>
      <p class="orbital-unit">°C</p>
      <p class="orbital-status" data-status>Комфорт</p>
    </div>
  `

  root.appendChild(shell)

  const track = shell.querySelector('[data-track]')
  const active = shell.querySelector('[data-active]')
  const comfortMark = shell.querySelector('[data-comfort]')
  const handle = shell.querySelector('[data-handle]')
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
    const point = polar(angle)
    const mood = moodForTemp(temp)

    active.setAttribute('d', arcPath(startAngle, angle))
    handle.style.left = `${(point.x / size) * 100}%`
    handle.style.top = `${(point.y / size) * 100}%`
    valueEl.textContent = String(temp)
    statusEl.textContent = mood.label
    shell.dataset.mode = mood.mode
    shell.style.setProperty('--temp-ratio', String((temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)))

    onChange?.(temp, mood)
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
    const deg = (Math.atan2(y - cy, x - cx) * 180) / Math.PI
    return deg
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
    handle.setPointerCapture?.(event.pointerId)
    setTemp(angleToTemp(angleFromEvent(event)))
    window.addEventListener('pointermove', onPointerMove, { passive: false })
    window.addEventListener('pointerup', stopDrag)
    window.addEventListener('pointercancel', stopDrag)
  }

  handle.addEventListener('pointerdown', startDrag)

  shell.querySelector('.orbital-svg').addEventListener('pointerdown', (event) => {
    if (event.target.closest('.orbital-handle')) return
    startDrag(event)
  })

  render()

  // Gentle intro spin toward comfort
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
