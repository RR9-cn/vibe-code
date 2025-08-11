<template>
  <div class="website-preview-view">
    <!-- 如果有简历数据，显示个人网站 -->
    <PersonalWebsite 
      v-if="resumeData" 
      :resume-data="resumeData" 
    />
    
    <!-- 如果没有数据，显示加载状态或示例 -->
    <div v-else class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="text-center">
        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">暂无简历数据</h2>
        <p class="text-gray-600 mb-6">请先上传并解析简历，然后查看生成的个人网站</p>
        <router-link 
          to="/upload" 
          class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          上传简历
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useResumeStore } from '@/stores/resume'
import PersonalWebsite from '@/components/PersonalWebsite.vue'
import type { ResumeData } from '@/types'

// 使用简历store
const resumeStore = useResumeStore()

// 响应式数据
const resumeData = ref<ResumeData | null>(null)

// 组件挂载时获取简历数据
onMounted(async () => {
  // 从store中获取当前简历数据
  if (resumeStore.currentResume) {
    resumeData.value = resumeStore.currentResume
  } else {
    // 如果store中没有数据，尝试从localStorage获取
    const savedResume = localStorage.getItem('currentResume')
    if (savedResume) {
      try {
        resumeData.value = JSON.parse(savedResume)
      } catch (error) {
        console.error('解析保存的简历数据失败:', error)
      }
    }
  }
  
  // 如果还是没有数据，可以加载示例数据用于演示
  if (!resumeData.value && import.meta.env.DEV) {
    resumeData.value = createSampleResumeData()
  }
})

// 创建示例简历数据（仅用于开发环境演示）
const createSampleResumeData = (): ResumeData => {
  return {
    id: 'sample-resume',
    personalInfo: {
      name: '李明',
      email: 'liming@example.com',
      phone: '13800138000',
      location: '上海市',
      summary: '拥有5年经验的全栈开发工程师，专注于现代Web技术和用户体验设计。热爱技术创新，具备强烈的学习能力和团队协作精神。',
      linkedin: 'https://linkedin.com/in/liming',
      github: 'https://github.com/liming',
      website: 'https://liming.dev'
    },
    workExperience: [
      {
        company: '阿里巴巴集团',
        position: '高级前端工程师',
        startDate: '2022-03-01',
        endDate: null,
        description: [
          '负责淘宝商家后台核心功能的前端开发，服务数百万商家用户',
          '使用React和TypeScript构建高性能、可维护的大型Web应用',
          '优化页面加载性能，首屏渲染时间减少40%',
          '参与前端架构设计，制定团队开发规范和最佳实践',
          '指导初级开发者，参与技术分享和代码评审'
        ],
        technologies: ['React', 'TypeScript', 'Ant Design', 'Webpack', 'Node.js']
      },
      {
        company: '字节跳动',
        position: '前端工程师',
        startDate: '2020-07-01',
        endDate: '2022-02-28',
        description: [
          '参与抖音创作者平台的开发，支持千万级创作者内容管理',
          '使用Vue.js开发响应式Web应用，兼容多种设备和浏览器',
          '实现复杂的数据可视化组件，提升用户数据分析体验',
          '与产品和设计团队紧密合作，快速迭代产品功能'
        ],
        technologies: ['Vue.js', 'JavaScript', 'Element UI', 'ECharts', 'Sass']
      },
      {
        company: '腾讯科技',
        position: '初级前端工程师',
        startDate: '2019-06-01',
        endDate: '2020-06-30',
        description: [
          '参与微信小程序开发工具的前端开发工作',
          '使用原生JavaScript和CSS实现用户界面组件',
          '协助完成多个小程序项目的开发和维护',
          '学习并掌握现代前端开发技术栈'
        ],
        technologies: ['JavaScript', 'CSS3', 'HTML5', '微信小程序', 'Git']
      }
    ],
    education: [
      {
        institution: '清华大学',
        degree: '计算机科学与技术学士',
        major: '计算机科学与技术',
        startDate: '2015-09-01',
        endDate: '2019-06-01',
        gpa: '3.9'
      }
    ],
    skills: [
      { category: 'technical', name: 'JavaScript', level: 'expert' },
      { category: 'technical', name: 'TypeScript', level: 'advanced' },
      { category: 'technical', name: 'React', level: 'advanced' },
      { category: 'technical', name: 'Vue.js', level: 'advanced' },
      { category: 'technical', name: 'Node.js', level: 'intermediate' },
      { category: 'technical', name: 'Python', level: 'intermediate' },
      { category: 'technical', name: 'Docker', level: 'intermediate' },
      { category: 'technical', name: 'AWS', level: 'beginner' },
      { category: 'soft', name: '团队协作', level: 'expert' },
      { category: 'soft', name: '项目管理', level: 'advanced' },
      { category: 'soft', name: '沟通能力', level: 'advanced' },
      { category: 'soft', name: '问题解决', level: 'expert' },
      { category: 'language', name: '中文', level: 'expert' },
      { category: 'language', name: '英语', level: 'advanced' },
      { category: 'language', name: '日语', level: 'beginner' }
    ],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
}
</script>

<style scoped>
.website-preview-view {
  /* 确保全屏显示 */
  min-height: 100vh;
}
</style>