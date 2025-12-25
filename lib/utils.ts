import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date | string): string {
  const d = new Date(date)
  return d.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

export function formatDateTime(date: Date | string): string {
  const d = new Date(date)
  return d.toLocaleString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Asia/Kolkata'
  })
}

export function getISTTime(): Date {
  return new Date(new Date().toLocaleString("en-US", {timeZone: "Asia/Kolkata"}))
}

export function isWithinTimeWindow(sessionType: 'FIRST_HALF' | 'SECOND_HALF'): boolean {
  const now = getISTTime()
  const currentHour = now.getHours()
  const currentMinute = now.getMinutes()
  const currentTime = currentHour * 60 + currentMinute

  if (sessionType === 'FIRST_HALF') {
    // 1:00 PM to 2:30 PM (13:00 to 14:30)
    const startTime = 13 * 60 // 13:00
    const endTime = 14 * 60 + 30 // 14:30
    return currentTime >= startTime && currentTime <= endTime
  } else if (sessionType === 'SECOND_HALF') {
    // 6:00 PM to 7:30 PM (18:00 to 19:30)
    const startTime = 18 * 60 // 18:00
    const endTime = 19 * 60 + 30 // 19:30
    return currentTime >= startTime && currentTime <= endTime
  }

  return false
}

export function generateApprovalCode(): string {
  return Math.floor(100000 + Math.random() * 900000).toString()
}

export function getEditableUntil(createdAt: Date): Date {
  const editableUntil = new Date(createdAt)
  editableUntil.setMinutes(editableUntil.getMinutes() + 10)
  return editableUntil
}

export function isEditable(createdAt: Date): boolean {
  const now = new Date()
  const editableUntil = getEditableUntil(createdAt)
  return now <= editableUntil
}