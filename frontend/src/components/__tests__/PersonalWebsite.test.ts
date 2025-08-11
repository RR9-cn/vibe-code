import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PersonalWebsite from '../PersonalWebsite.vue'
import type { ResumeData } from '@/types'

// 模拟数据
const mockResumeData: ResumeData = {
  id: 'test-resume-1',
  personalInfo: {
    name: '张三',
    email: 'zhangsan@example.com',
    phone: '13800138000',
    location: '北京市',
    summary: '一位充满激情的前端开发工程师，专注于Vue.js和现代Web技术。',
    linkedin: 'https://linkedin.com/in/zhangsan',
    github: 'https://github.com/zhangsan',
    website: 'https://zhangsan.dev'
  },
  workExperience: [
    {
      company: '科技有限公司',
      position: '高级前端工程师',
      startDate: '2022-01-01',
      endDate: '2024-01-01',
      description: [
        '负责公司主要产品的前端开发工作',
        '使用Vue.js和TypeScript构建现代化Web应用',
        '优化应用性能，提升用户体验'
      ],
      technologies: ['Vue.js', 'TypeScript', 'Tailwind CSS', 'Vite']
    }
  ],
  education: [
    {
      institution: '北京大学',
      degree: '计算机科学学士',
      major: '计算机科学与技术',
      startDate: '2018-09-01',
      endDate: '2022-06-01',
      gpa: '3.8'
    }
  ],
  skills: [
    {
      category: 'technical',
      name: 'Vue.js',
      level: 'advanced'
    },
    {
      category: 'technical',
      name: 'TypeScript',
      level: 'intermediate'
    },
    {
      category: 'soft',
      name: '团队协作',
      level: 'advanced'
    },
    {
      category: 'language',
      name: '英语',
      level: 'intermediate'
    }
  ],
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z'
}

describe('PersonalWebsite', () => {
  it('应该正确渲染个人网站组件', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.personal-website').exists()).toBe(true)
  })

  it('应该显示个人信息', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    expect(wrapper.text()).toContain('张三')
    expect(wrapper.text()).toContain('zhangsan@example.com')
  })

  it('应该显示工作经历', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    expect(wrapper.text()).toContain('科技有限公司')
    expect(wrapper.text()).toContain('高级前端工程师')
  })

  it('应该显示教育背景', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    expect(wrapper.text()).toContain('北京大学')
    expect(wrapper.text()).toContain('计算机科学学士')
  })

  it('应该显示技能信息', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    expect(wrapper.text()).toContain('Vue.js')
    expect(wrapper.text()).toContain('TypeScript')
    expect(wrapper.text()).toContain('团队协作')
  })

  it('应该包含所有必要的组件', () => {
    const wrapper = mount(PersonalWebsite, {
      props: {
        resumeData: mockResumeData
      }
    })

    // 检查是否包含所有主要组件
    expect(wrapper.findComponent({ name: 'HeaderSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'HeroSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'AboutSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'ExperienceSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'EducationSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'SkillsSection' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'ContactSection' }).exists()).toBe(true)
  })
})