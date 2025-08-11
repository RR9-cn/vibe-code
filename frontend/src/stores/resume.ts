import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ResumeData } from '@/types'

// 简历数据状态管理
export const useResumeStore = defineStore('resume', () => {
  // 状态
  const currentResume = ref<ResumeData | null>(null)
  const isLoading = ref<boolean>(false)
  const error = ref<string>('')

  // 动作
  const setCurrentResume = (resume: ResumeData) => {
    currentResume.value = resume
  }

  const setLoading = (status: boolean) => {
    isLoading.value = status
  }

  const setError = (errorMessage: string) => {
    error.value = errorMessage
  }

  const clearResume = () => {
    currentResume.value = null
    error.value = ''
  }

  const updatePersonalInfo = (personalInfo: ResumeData['personalInfo']) => {
    if (currentResume.value) {
      currentResume.value.personalInfo = personalInfo
      currentResume.value.updatedAt = new Date().toISOString()
    }
  }

  const updateWorkExperience = (workExperience: ResumeData['workExperience']) => {
    if (currentResume.value) {
      currentResume.value.workExperience = workExperience
      currentResume.value.updatedAt = new Date().toISOString()
    }
  }

  const updateEducation = (education: ResumeData['education']) => {
    if (currentResume.value) {
      currentResume.value.education = education
      currentResume.value.updatedAt = new Date().toISOString()
    }
  }

  const updateSkills = (skills: ResumeData['skills']) => {
    if (currentResume.value) {
      currentResume.value.skills = skills
      currentResume.value.updatedAt = new Date().toISOString()
    }
  }

  return {
    // 状态
    currentResume,
    isLoading,
    error,
    
    // 动作
    setCurrentResume,
    setLoading,
    setError,
    clearResume,
    updatePersonalInfo,
    updateWorkExperience,
    updateEducation,
    updateSkills
  }
})