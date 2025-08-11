import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import ParseStatus from '@/components/ParseStatus.vue'
import { useUploadStore } from '@/stores/upload'

// Mock API服务
vi.mock('@/services/api', () => ({
  ApiService: {
    getParseStatus: vi.fn(),
    parseResume: vi.fn(),
    generateWebsite: vi.fn()
  }
}))

// Mock 通知服务
vi.mock('@/services/notification', () => ({
  notify: {
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn()
  }
}))

describe('ParseStatus组件测试', () => {
  let wrapper: any
  let pinia: any
  let uploadStore: any

  beforeEach(() => {
    pinia = createPinia()
    wrapper = mount(ParseStatus, {
      props: {
        uploadId: 'test-upload-id',
        autoRefresh: false // 禁用自动刷新以便测试
      },
      global: {
        plugins: [pinia]
      }
    })
    uploadStore = useUploadStore()
  })

  it('组件能够正常渲染', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.status-card').exists()).toBe(true)
  })

  it('显示正确的空闲状态', () => {
    uploadStore.setParseStatus({
      status: 'idle',
      progress: 0,
      message: ''
    })

    expect(wrapper.text()).toContain('等待解析')
    expect(wrapper.text()).toContain('准备开始解析简历内容')
  })

  it('显示正确的解析中状态', async () => {
    uploadStore.setParseStatus({
      status: 'parsing',
      progress: 50,
      message: '正在解析...'
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('正在解析')
    expect(wrapper.text()).toContain('正在解析...')
    expect(wrapper.find('.progress-bar-fill').exists()).toBe(true)
  })

  it('显示正确的成功状态', async () => {
    const mockResumeData = {
      id: 'test-id',
      personalInfo: {
        name: '张三',
        email: 'zhangsan@example.com'
      },
      workExperience: [{ company: '测试公司', position: '开发工程师', startDate: '2020-01', description: ['工作描述'] }],
      education: [{ institution: '测试大学', degree: '本科', startDate: '2016-09', endDate: '2020-06' }],
      skills: [],
      createdAt: '2023-01-01',
      updatedAt: '2023-01-01'
    }

    uploadStore.setParseStatus({
      status: 'success',
      progress: 100,
      message: '解析完成',
      data: mockResumeData
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('解析完成')
    expect(wrapper.text()).toContain('张三')
    expect(wrapper.text()).toContain('zhangsan@example.com')
    expect(wrapper.find('button').text()).toContain('生成个人网站')
  })

  it('显示正确的错误状态', async () => {
    uploadStore.setParseStatus({
      status: 'error',
      progress: 0,
      message: '解析失败'
    })

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('解析失败')
    expect(wrapper.find('button').text()).toContain('重试解析')
  })

  it('点击重试按钮时触发重试事件', async () => {
    uploadStore.setParseStatus({
      status: 'error',
      progress: 0,
      message: '解析失败'
    })

    await wrapper.vm.$nextTick()

    const retryButton = wrapper.find('button')
    await retryButton.trigger('click')

    expect(wrapper.emitted('retry')).toBeTruthy()
  })
})