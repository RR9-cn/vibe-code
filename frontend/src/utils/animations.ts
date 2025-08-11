// 动画工具类

// 交叉观察器配置
export interface IntersectionOptions {
  threshold?: number | number[]
  rootMargin?: string
  root?: Element | null
}

// 创建交叉观察器
export const createIntersectionObserver = (
  callback: IntersectionObserverCallback,
  options: IntersectionOptions = {}
): IntersectionObserver => {
  const defaultOptions: IntersectionOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  }

  return new IntersectionObserver(callback, { ...defaultOptions, ...options })
}

// 滚动触发动画
export const addScrollAnimation = (element: HTMLElement, animationClass: string) => {
  const observer = createIntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add(animationClass)
        observer.unobserve(entry.target)
      }
    })
  })

  observer.observe(element)
  return observer
}

// 延迟动画
export const delayedAnimation = (
  elements: NodeListOf<Element> | Element[],
  animationClass: string,
  delay: number = 100
) => {
  Array.from(elements).forEach((element, index) => {
    setTimeout(() => {
      element.classList.add(animationClass)
    }, index * delay)
  })
}

// 视差滚动效果
export const parallaxScroll = (element: HTMLElement, speed: number = 0.5) => {
  const handleScroll = () => {
    const scrolled = window.pageYOffset
    const rate = scrolled * -speed
    element.style.transform = `translateY(${rate}px)`
  }

  window.addEventListener('scroll', handleScroll)
  return () => window.removeEventListener('scroll', handleScroll)
}

// 平滑滚动到元素
export const smoothScrollTo = (
  element: HTMLElement | string,
  options: ScrollIntoViewOptions = {}
) => {
  const target = typeof element === 'string' 
    ? document.getElementById(element) 
    : element

  if (target) {
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start',
      ...options
    })
  }
}

// 动画类名常量
export const ANIMATION_CLASSES = {
  FADE_IN: 'animate-fade-in',
  FADE_UP: 'animate-fade-up',
  SLIDE_LEFT: 'animate-slide-left',
  SLIDE_RIGHT: 'animate-slide-right',
  SCALE_IN: 'animate-scale-in',
  BOUNCE_IN: 'animate-bounce-in'
} as const

// 动画持续时间常量
export const ANIMATION_DURATIONS = {
  FAST: 200,
  NORMAL: 300,
  SLOW: 500,
  SLOWER: 800
} as const

// 缓动函数
export const EASING = {
  EASE_OUT: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
  EASE_IN_OUT: 'cubic-bezier(0.4, 0, 0.2, 1)',
  BOUNCE: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
} as const

// 创建CSS动画
export const createCSSAnimation = (
  name: string,
  keyframes: string,
  duration: string = '0.3s',
  easing: string = EASING.EASE_OUT
) => {
  const style = document.createElement('style')
  style.textContent = `
    @keyframes ${name} {
      ${keyframes}
    }
    .${name} {
      animation: ${name} ${duration} ${easing} forwards;
    }
  `
  document.head.appendChild(style)
}

// 预定义动画关键帧
export const KEYFRAMES = {
  FADE_IN: `
    from { opacity: 0; }
    to { opacity: 1; }
  `,
  FADE_UP: `
    from { 
      opacity: 0; 
      transform: translateY(30px); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0); 
    }
  `,
  SLIDE_LEFT: `
    from { 
      opacity: 0; 
      transform: translateX(-50px); 
    }
    to { 
      opacity: 1; 
      transform: translateX(0); 
    }
  `,
  SLIDE_RIGHT: `
    from { 
      opacity: 0; 
      transform: translateX(50px); 
    }
    to { 
      opacity: 1; 
      transform: translateX(0); 
    }
  `,
  SCALE_IN: `
    from { 
      opacity: 0; 
      transform: scale(0.8); 
    }
    to { 
      opacity: 1; 
      transform: scale(1); 
    }
  `,
  BOUNCE_IN: `
    0% { 
      opacity: 0; 
      transform: scale(0.3); 
    }
    50% { 
      opacity: 1; 
      transform: scale(1.05); 
    }
    70% { 
      transform: scale(0.9); 
    }
    100% { 
      opacity: 1; 
      transform: scale(1); 
    }
  `
}

// 初始化预定义动画
export const initializeAnimations = () => {
  Object.entries(KEYFRAMES).forEach(([name, keyframes]) => {
    const className = name.toLowerCase().replace(/_/g, '-')
    createCSSAnimation(`animate-${className}`, keyframes)
  })
}

// 动画状态管理
export class AnimationManager {
  private observers: IntersectionObserver[] = []
  private animations: Map<string, () => void> = new Map()

  // 添加滚动动画
  addScrollAnimation(
    selector: string,
    animationClass: string,
    options?: IntersectionOptions
  ) {
    const elements = document.querySelectorAll(selector)
    elements.forEach(element => {
      const observer = addScrollAnimation(element as HTMLElement, animationClass)
      this.observers.push(observer)
    })
  }

  // 添加延迟动画
  addDelayedAnimation(
    selector: string,
    animationClass: string,
    delay: number = 100
  ) {
    const elements = document.querySelectorAll(selector)
    delayedAnimation(elements, animationClass, delay)
  }

  // 清理所有观察器
  cleanup() {
    this.observers.forEach(observer => observer.disconnect())
    this.observers = []
    this.animations.forEach(cleanup => cleanup())
    this.animations.clear()
  }
}

// 导出单例动画管理器
export const animationManager = new AnimationManager()