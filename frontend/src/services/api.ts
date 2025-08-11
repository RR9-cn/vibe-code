import axios from 'axios'
import type { UploadResponse, ParseStatus, ResumeData, WebsiteConfig, ApiResponse } from '@/types'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// API服务类
export class ApiService {
  // 文件上传
  static async uploadFile(file: File, onProgress?: (progress: number) => void): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post<any, ApiResponse<UploadResponse>>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })

    if (!response.success) {
      throw new Error(response.message || '文件上传失败')
    }

    return response.data!
  }

  // 解析简历
  static async parseResume(uploadId: string): Promise<ParseStatus> {
    const response = await api.post<any, ApiResponse<ParseStatus>>(`/parse/${uploadId}`)
    
    if (!response.success) {
      throw new Error(response.message || '简历解析失败')
    }

    return response.data!
  }

  // 获取解析状态
  static async getParseStatus(uploadId: string): Promise<ParseStatus> {
    const response = await api.get<any, ApiResponse<ParseStatus>>(`/parse/${uploadId}/status`)
    
    if (!response.success) {
      throw new Error(response.message || '获取解析状态失败')
    }

    return response.data!
  }

  // 生成网站
  static async generateWebsite(resumeData: ResumeData, templateId: string = 'default'): Promise<WebsiteConfig> {
    const response = await api.post<any, ApiResponse<WebsiteConfig>>('/generate-website', {
      resume_data: resumeData,
      template_id: templateId
    })

    if (!response.success) {
      throw new Error(response.message || '网站生成失败')
    }

    return response.data!
  }

  // 更新网站
  static async updateWebsite(websiteId: string, resumeData: ResumeData): Promise<WebsiteConfig> {
    const response = await api.put<any, ApiResponse<WebsiteConfig>>(`/website/${websiteId}`, {
      resume_data: resumeData
    })

    if (!response.success) {
      throw new Error(response.message || '网站更新失败')
    }

    return response.data!
  }

  // 获取网站信息
  static async getWebsite(websiteId: string): Promise<WebsiteConfig> {
    const response = await api.get<any, ApiResponse<WebsiteConfig>>(`/website/${websiteId}`)
    
    if (!response.success) {
      throw new Error(response.message || '获取网站信息失败')
    }

    return response.data!
  }
}

export default api