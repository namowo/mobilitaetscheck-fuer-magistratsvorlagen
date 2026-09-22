<template>
  <div
    v-if="!data || data.length === 0"
    class="text-gray-400 text-sm text-center flex items-center justify-center"
    :style="{ height: `${height}px` }"
  >
    Keine Daten vorhanden.
  </div>
  <div v-else ref="containerRef" class="w-full overflow-x-auto">
    <svg
      :viewBox="`0 0 ${svgWidth} ${height}`"
      :width="svgWidth"
      :height="height"
      class="block"
    >
      <!-- y-axis gridlines + ticks -->
      <g v-for="tick in yTicks" :key="tick">
        <line
          :x1="paddingLeft"
          :x2="svgWidth - paddingRight"
          :y1="yScale(tick)"
          :y2="yScale(tick)"
          stroke="currentColor"
          class="text-gray-100"
          stroke-width="1"
        />
        <text
          :x="paddingLeft - 8"
          :y="yScale(tick)"
          text-anchor="end"
          dominant-baseline="middle"
          class="fill-gray-400 text-[10px]"
        >
          {{ tick }}
        </text>
      </g>

      <!-- y-axis line -->
      <line
        :x1="paddingLeft"
        :x2="paddingLeft"
        :y1="paddingTop"
        :y2="height - paddingBottom"
        stroke="currentColor"
        class="text-gray-200"
        stroke-width="1"
      />

      <!-- bars -->
      <g v-for="(point, i) in data" :key="point.monat">
        <rect
          :x="barX(i)"
          :y="yScale(point.anzahl)"
          :width="barWidth"
          :height="Math.max(0, height - paddingBottom - yScale(point.anzahl))"
          rx="2"
          class="fill-blue-500 hover:fill-blue-600 transition-colors"
        >
          <title>{{ formatMonthFull(point.monat) }}: {{ point.anzahl }}</title>
        </rect>
        <text
          v-if="showLabel(i)"
          :x="barX(i) + barWidth / 2"
          :y="height - paddingBottom + 14"
          text-anchor="middle"
          class="fill-gray-400 text-[10px]"
        >
          {{ formatMonth(point.monat) }}
        </text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] }
})

const paddingLeft = 28
const paddingRight = 8
const paddingTop = 10
const paddingBottom = 22
const minBarWidth = 10
const maxBarWidth = 28
const barGapRatio = 0.5
const height = 180

const containerRef = ref(null)
const containerWidth = ref(300)
let resizeObserver = null

onMounted(() => {
  if (containerRef.value) {
    containerWidth.value = containerRef.value.clientWidth || 300
    resizeObserver = new ResizeObserver((entries) => {
      containerWidth.value = entries[0].contentRect.width || containerWidth.value
    })
    resizeObserver.observe(containerRef.value)
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
})

const plotWidth = computed(() => Math.max(0, containerWidth.value - paddingLeft - paddingRight))

const barWidth = computed(() => {
  const n = props.data.length || 1
  const raw = plotWidth.value / n / (1 + barGapRatio)
  return Math.min(maxBarWidth, Math.max(minBarWidth, raw))
})

const barSlot = computed(() => barWidth.value * (1 + barGapRatio))

const contentWidth = computed(
  () => paddingLeft + paddingRight + barSlot.value * props.data.length
)

const svgWidth = computed(() => Math.max(containerWidth.value, contentWidth.value))

const extraSpace = computed(() => Math.max(0, svgWidth.value - contentWidth.value))

const max = computed(() => Math.max(1, ...props.data.map((d) => d.anzahl)))

const yTicks = computed(() => {
  const niceMax = Math.ceil(max.value / 4) * 4 || 4
  const step = niceMax / 4
  return [0, step, step * 2, step * 3, step * 4].map((v) => Math.round(v))
})

const yScale = (value) => {
  const topTick = yTicks.value[yTicks.value.length - 1] || 1
  const plotHeight = height - paddingTop - paddingBottom
  return height - paddingBottom - (value / topTick) * plotHeight
}

const barX = (index) =>
  paddingLeft + extraSpace.value / 2 + index * barSlot.value + (barSlot.value - barWidth.value) / 2

const maxLabels = 12
const showLabel = (index) => {
  if (props.data.length <= maxLabels) return true
  const step = Math.ceil(props.data.length / maxLabels)
  return index % step === 0
}

const formatMonth = (isoDate) =>
  new Date(isoDate).toLocaleDateString('de-DE', { month: '2-digit', year: '2-digit' })

const formatMonthFull = (isoDate) =>
  new Date(isoDate).toLocaleDateString('de-DE', { month: 'long', year: 'numeric' })
</script>
