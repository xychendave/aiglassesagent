import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"
// import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const ToastProvider = ToastPrimitives.Provider

const ToastViewport = React.forwardRef<
  React.ElementRef<typeof ToastPrimitives.Viewport>,
  React.ComponentPropsWithoutRef<typeof ToastPrimitives.Viewport>
>(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]",
      className
    )}
    {...props}
  />
))
ToastViewport.displayName = ToastPrimitives.Viewport.displayName

export interface ToastProps extends React.ComponentPropsWithoutRef<typeof ToastPrimitives.Root> {
  title?: string | undefined; // 修改为 string | undefined 类型
  description?: React.ReactNode;
  action?: ToastActionElement;
}

export type ToastActionElement = React.ReactElement<typeof ToastPrimitives.Action>

export { ToastProvider, ToastViewport } 