// 前端TypeScript类型定义

// 个人信息接口
export interface PersonalInfo {
  name: string
  email: string
  phone?: string
  location?: string
  summary?: string
  linkedin?: string
  github?: string
  website?: string
}

// 工作经历接口
export interface WorkExperience {
  company: string
  position: string
  startDate: string
  endDate?: string
  description: string[]
  technologies?: string[]
}

// 教育背景接口
export interface Education {
  institution: string
  degree: string
  major?: string
  startDate: string
  endDate?: string
  gpa?: string
}

// 技能接口
export interface Skill {
  category: 'technical' | 'soft' | 'language'
  name: string
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert'
}

// 简历数据接口
export interface ResumeData {
  id: string
  personalInfo: PersonalInfo
  workExperience: WorkExperience[]
  education: Education[]
  skills: Skill[]
  createdAt: string
  updatedAt: string
}

// 文件上传响应接口
export interface UploadResponse {
  uploadId: string
  message: string
}

// 解析状态接口
export interface ParseStatus {
  status: 'idle' | 'parsing' | 'success' | 'error'
  progress: number
  message: string
  data?: ResumeData
  websiteUrl?: string
}

// API响应接口
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

// 网站配置接口
export interface WebsiteConfig {
  id: string
  resumeId: string
  templateId: string
  colorScheme: {
    primary: string
    secondary: string
    accent: string
    background: string
    text: string
  }
  url: string
  isPublic: boolean
}