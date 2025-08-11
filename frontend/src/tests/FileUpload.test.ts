import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import FileUpload from '@/components/FileUpload.vue'

// Mock API服务
vi.mock('@/services/api', () => ({
  ApiService: {
    uploadFile: vi.fn()
  }
}))

// Mock 通知服务
vi.mock('@/services/notification', () => ({
  notify: {
    success: vi.fn(),
    error: vi.fn()
  }
}))

describe('FileUpload组件测试', () => {
  let wrapper: any
  let pinia: any

  beforeEach(() => {
    pinia = createPinia()
    wrapper = mount(FileUpload, {
      global: {
        plugins: [pinia]
      }
    })
  })

  it('组件能够正常渲染', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.upload-zone').exists()).toBe(true)
  })

  it('显示正确的上传提示文本', () => {
    expect(wrapper.text()).toContain('点击上传或拖拽文件到此处')
    expect(wrapper.text()).toContain('支持PDF格式，最大10MB')
  })

  it('点击上传区域时触发文件选择', async () => {
    const fileInput = wrapper.find('input[type="file"]')
    const clickSpy = vi.spyOn(fileInput.element, 'click')
    
    await wrapper.find('.upload-zone').trigger('click')
    
    expect(clickSpy).toHaveBeenCalled()
  })

  it('文件输入框有正确的属性', () => {
    const fileInput = wrapper.find('input[type="file"]')
    
    expect(fileInput.attributes('accept')).toBe('.pdf,application/pdf')
    expect(fileInput.classes()).toContain('hidden')
  })

  it('拖拽进入时显示拖拽状态', async () => {
    const uploadZone = wrapper.find('.upload-zone')
    
    await uploadZone.trigger('dragenter')
    
    expect(uploadZone.classes()).toContain('upload-zone-dragover')
  })

  it('拖拽离开时移除拖拽状态', async () => {
    const uploadZone = wrapper.find('.upload-zone')
    
    await uploadZone.trigger('dragenter')
    await uploadZone.trigger('dragleave')
    
    expect(uploadZone.classes()).not.toContain('upload-zone-dragover')
  })
})