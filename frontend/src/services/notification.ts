import { ref } from 'vue'
import type { NotificationType } from '@/components/ui/NotificationToast.vue'

// 通知实例引用
const notificationInstance = ref<any>(null)

// 通知服务类
export class NotificationService {
  // 设置通知实例
  static setInstance(instance: any) {
    notificationInstance.value = instance
  }

  // 显示成功通知
  static success(message: string, title?: string, duration?: number) {
    this.show('success', message, title, duration)
  }

  // 显示错误通知
  static error(message: string, title?: string, duration?: number) {
    this.show('error', message, title, duration)
  }

  // 显示警告通知
  static warning(message: string, title?: string, duration?: number) {
    this.show('warning', message, title, duration)
  }

  // 显示信息通知
  static info(message: string, title?: string, duration?: number) {
    this.show('info', message, title, duration)
  }

  // 显示通知
  private static show(
    type: NotificationType,
    message: string,
    title?: string,
    duration?: number
  ) {
    if (notificationInstance.value) {
      notificationInstance.value.addNotification({
        type,
        message,
        title,
        duration
      })
    } else {
      // 如果通知实例不存在，使用console输出
      console.log(`[${type.toUpperCase()}] ${title ? title + ': ' : ''}${message}`)
    }
  }
}

// 导出便捷方法
export const notify = NotificationService