# Modern SaaS Marketing Website - Frontend Technical Architecture

> 🏗️ **Complete Technical Stack & Component Architecture for High-Converting SaaS Marketing Sites**

## Executive Summary

Based on the comprehensive homepage design analysis, this document outlines a modern, SEO-optimized, and performance-first technical architecture for building our SaaS marketing website. The architecture prioritizes fast loading times, excellent Core Web Vitals, conversion optimization, and seamless user experience across all devices.

---

## Recommended Tech Stack

### **Core Framework: Next.js 14 (App Router)**

**Why Next.js 14:**
- **Server-Side Rendering (SSR)**: Critical for SEO and fast first paint
- **Static Site Generation (SSG)**: Perfect for marketing pages that don't change frequently
- **App Router**: Modern file-based routing with better performance
- **Built-in optimization**: Image optimization, font optimization, automatic code splitting
- **Vercel integration**: Seamless deployment and edge functions
- **TypeScript support**: Type safety for large-scale development

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['example.com'],
    formats: ['image/webp', 'image/avif'],
  },
  async rewrites() {
    return [
      {
        source: '/blog/:slug*',
        destination: '/blog/:slug*',
      },
    ];
  },
};

module.exports = nextConfig;
```

### **Styling: Tailwind CSS + Headless UI**

**Why Tailwind CSS:**
- **Utility-first**: Rapid development with consistent design system
- **Performance**: Only includes used styles in production
- **Responsive design**: Mobile-first approach built-in
- **Dark mode**: Easy theme switching for modern UX
- **Design system**: Easy to maintain brand consistency

**Why Headless UI:**
- **Accessibility**: WAI-ARIA compliant components out of the box
- **Unstyled**: Full design control while maintaining functionality
- **TypeScript support**: Full type safety
- **Framework agnostic**: Works perfectly with Tailwind

```typescript
// tailwind.config.js
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}

export default config
```

### **State Management: Zustand + React Query**

**Why Zustand:**
- **Lightweight**: Minimal boilerplate compared to Redux
- **TypeScript-first**: Excellent TypeScript support
- **Performance**: No unnecessary re-renders
- **DevTools**: Great debugging experience

**Why React Query (TanStack Query):**
- **Server state management**: Perfect for API calls and caching
- **Background updates**: Keeps data fresh automatically
- **Optimistic updates**: Smooth UX for form submissions
- **Error handling**: Built-in retry and error boundaries

```typescript
// stores/ui-store.ts
import { create } from 'zustand'

interface UIState {
  isMenuOpen: boolean
  isDemoModalOpen: boolean
  currentIndustry: string | null
  setMenuOpen: (open: boolean) => void
  setDemoModalOpen: (open: boolean) => void
  setCurrentIndustry: (industry: string | null) => void
}

export const useUIStore = create<UIState>((set) => ({
  isMenuOpen: false,
  isDemoModalOpen: false,
  currentIndustry: null,
  setMenuOpen: (open) => set({ isMenuOpen: open }),
  setDemoModalOpen: (open) => set({ isDemoModalOpen: open }),
  setCurrentIndustry: (industry) => set({ currentIndustry: industry }),
}))
```

### **Animation: Framer Motion**

**Why Framer Motion:**
- **Performance**: GPU-accelerated animations
- **Declarative**: Easy to understand and maintain
- **Gesture support**: Touch and drag interactions
- **Layout animations**: Smooth transitions between states
- **Scroll-triggered animations**: Perfect for marketing pages

```typescript
// components/AnimatedSection.tsx
import { motion } from 'framer-motion'

const AnimatedSection = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.section
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      viewport={{ once: true, margin: '-100px' }}
    >
      {children}
    </motion.section>
  )
}
```

### **Content Management: MDX + Contentlayer**

**Why MDX:**
- **Markdown + React**: Rich content with interactive components
- **Version control**: Content lives in git with code
- **Type safety**: Frontmatter validation
- **Developer experience**: Syntax highlighting and validation

**Why Contentlayer:**
- **Build-time processing**: Fast runtime performance
- **Type generation**: Automatic TypeScript types for content
- **Validation**: Ensures content structure consistency
- **Flexible**: Works with various content sources

```typescript
// contentlayer.config.ts
import { defineDocumentType, makeSource } from 'contentlayer/source-files'

export const CaseStudy = defineDocumentType(() => ({
  name: 'CaseStudy',
  filePathPattern: `case-studies/**/*.mdx`,
  contentType: 'mdx',
  fields: {
    title: { type: 'string', required: true },
    industry: { type: 'string', required: true },
    company: { type: 'string', required: true },
    results: { type: 'string', required: true },
    publishedAt: { type: 'date', required: true },
  },
  computedFields: {
    url: {
      type: 'string',
      resolve: (post) => `/case-studies/${post._raw.flattenedPath}`,
    },
  },
}))

export default makeSource({
  contentDirPath: 'content',
  documentTypes: [CaseStudy],
})
```

### **Analytics & Tracking: Vercel Analytics + PostHog**

**Why Vercel Analytics:**
- **Privacy-first**: No cookies required
- **Performance insights**: Core Web Vitals tracking
- **Real user monitoring**: Actual user experience data
- **Zero configuration**: Works out of the box with Vercel

**Why PostHog:**
- **Product analytics**: User behavior tracking
- **Feature flags**: A/B testing capabilities
- **Session replay**: Debug user issues
- **Open source**: Data ownership and privacy control

### **Form Handling: React Hook Form + Zod**

**Why React Hook Form:**
- **Performance**: Minimal re-renders
- **Bundle size**: Lightweight library
- **Validation**: Works well with validation libraries
- **TypeScript**: Excellent TypeScript support

**Why Zod:**
- **Type safety**: Runtime and compile-time validation
- **Schema validation**: Consistent validation across frontend/backend
- **Error messages**: User-friendly error handling
- **Developer experience**: Great autocomplete and IntelliSense

```typescript
// lib/validations.ts
import { z } from 'zod'

export const ContactFormSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  company: z.string().min(2, 'Company name is required'),
  industry: z.enum(['fashion', 'homeDecor', 'electronics', 'hospitality', 'other']),
  message: z.string().min(10, 'Message must be at least 10 characters'),
})

export type ContactFormData = z.infer<typeof ContactFormSchema>
```

---

## Complete Component Architecture

### **Project Structure**

```
src/
├── app/                          # Next.js App Router
│   ├── (marketing)/             # Marketing pages group
│   │   ├── page.tsx            # Homepage
│   │   ├── pricing/            
│   │   ├── case-studies/       
│   │   ├── about/              
│   │   └── contact/            
│   ├── blog/                   # Blog section
│   ├── docs/                   # Documentation
│   ├── legal/                  # Legal pages
│   ├── globals.css             
│   ├── layout.tsx              # Root layout
│   └── not-found.tsx           
├── components/                  # Reusable components
│   ├── ui/                     # Base UI components
│   ├── marketing/              # Marketing-specific components
│   ├── forms/                  # Form components
│   └── layout/                 # Layout components
├── lib/                        # Utilities and configurations
├── hooks/                      # Custom React hooks
├── stores/                     # Zustand stores
├── content/                    # MDX content
└── public/                     # Static assets
    ├── images/
    ├── icons/
    └── videos/
```

### **Core UI Components**

#### **Button Component**
```typescript
// components/ui/Button.tsx
import { forwardRef } from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button'
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'

export { Button, buttonVariants }
```

#### **Interactive Demo Component**
```typescript
// components/marketing/InteractiveDemo.tsx
'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, Search, Zap } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface DemoStep {
  id: string
  title: string
  description: string
  icon: React.ReactNode
}

const demoSteps: DemoStep[] = [
  {
    id: 'upload',
    title: 'Upload Image',
    description: 'Drag & drop or select from camera',
    icon: <Upload className="w-6 h-6" />,
  },
  {
    id: 'analyze',
    title: 'AI Analysis',
    description: 'Advanced visual AI processes the image',
    icon: <Search className="w-6 h-6" />,
  },
  {
    id: 'results',
    title: 'Perfect Matches',
    description: 'Get ranked results in 0.3 seconds',
    icon: <Zap className="w-6 h-6" />,
  },
]

export function InteractiveDemo() {
  const [currentStep, setCurrentStep] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleDemo = async (industry: string) => {
    setIsProcessing(true)
    // Simulate API call
    for (let i = 0; i <= 2; i++) {
      await new Promise(resolve => setTimeout(resolve, 800))
      setCurrentStep(i)
    }
    setIsProcessing(false)
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl p-8">
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          See visual search in action
        </h3>
        <p className="text-gray-600">
          Try these examples or upload your own image
        </p>
      </div>

      {/* Industry Examples */}
      <div className="flex flex-wrap gap-3 justify-center mb-8">
        {['Fashion', 'Home Decor', 'Electronics'].map((industry) => (
          <Button
            key={industry}
            variant="outline"
            onClick={() => handleDemo(industry.toLowerCase())}
            disabled={isProcessing}
            className="bg-white hover:bg-gray-50"
          >
            {industry}
          </Button>
        ))}
      </div>

      {/* Demo Process */}
      <div className="flex items-center justify-center space-x-8 mb-8">
        {demoSteps.map((step, index) => (
          <motion.div
            key={step.id}
            className={`flex flex-col items-center space-y-2 ${
              index <= currentStep ? 'text-blue-600' : 'text-gray-400'
            }`}
            animate={{
              scale: index === currentStep && isProcessing ? 1.1 : 1,
            }}
          >
            <div
              className={`p-3 rounded-full border-2 ${
                index <= currentStep
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-300 bg-gray-50'
              }`}
            >
              {step.icon}
            </div>
            <div className="text-center">
              <div className="font-medium">{step.title}</div>
              <div className="text-sm opacity-75">{step.description}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Results */}
      <AnimatePresence>
        {currentStep === 2 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-white rounded-lg p-6 border"
          >
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600 mb-2">
                Found 12 similar items in 0.3 seconds
              </div>
              <div className="text-gray-600 mb-4">
                94% style match accuracy • Available in your size and budget
              </div>
              <Button>See Full Results</Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
```

### **Marketing Page Components**

#### **Hero Section**
```typescript
// components/marketing/HeroSection.tsx
'use client'

import { motion } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { InteractiveDemo } from './InteractiveDemo'
import { CustomerLogos } from './CustomerLogos'

export function HeroSection() {
  return (
    <section className="relative pt-20 pb-16 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Turn browsers into{' '}
              <span className="text-blue-600">buyers</span> with visual search
            </h1>
            
            <p className="text-xl text-gray-600 mb-8">
              Your customers see what they want on Instagram. 
              Help them find it in your store.
            </p>

            {/* Benefit points */}
            <div className="space-y-3 mb-8">
              {[
                '73% higher conversion than text search',
                'Works with any e-commerce platform',
                'Setup in under 5 minutes'
              ].map((benefit, index) => (
                <motion.div
                  key={benefit}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="flex items-center space-x-3"
                >
                  <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700">{benefit}</span>
                </motion.div>
              ))}
            </div>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" className="text-lg px-8 py-4">
                See Live Demo
              </Button>
              <Button variant="outline" size="lg" className="text-lg px-8 py-4">
                View Pricing
              </Button>
            </div>
          </motion.div>

          {/* Demo */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <InteractiveDemo />
          </motion.div>
        </div>

        {/* Social proof */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-16"
        >
          <CustomerLogos />
        </motion.div>
      </div>
    </section>
  )
}
```

#### **Industry Solutions Grid**
```typescript
// components/marketing/IndustrySolutions.tsx
'use client'

import { motion } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { 
  Shirt, 
  Home, 
  Laptop, 
  Hotel, 
  UtensilsCrossed, 
  Dumbbell,
  Crown,
  ShoppingBag 
} from 'lucide-react'

interface Industry {
  id: string
  name: string
  icon: React.ReactNode
  description: string
  features: string[]
  successStory: string
  color: string
}

const industries: Industry[] = [
  {
    id: 'fashion',
    name: 'Fashion & Apparel',
    icon: <Shirt className="w-8 h-8" />,
    description: 'Perfect for fashion forward brands',
    features: [
      'Instagram/TikTok style matching',
      'Seasonal trend detection',
      'Size and fit recommendations'
    ],
    successStory: 'Thread Theory increased sales by 89%',
    color: 'from-pink-500 to-rose-500'
  },
  {
    id: 'homeDecor',
    name: 'Home Decor & Furniture',
    icon: <Home className="w-8 h-8" />,
    description: 'Transform home shopping experience',
    features: [
      'Room style matching',
      'Furniture and decor coordination',
      'Pinterest-style discovery'
    ],
    successStory: 'Casa Moderna hit 4.2% conversion rate',
    color: 'from-amber-500 to-orange-500'
  },
  // ... other industries
]

export function IndustrySolutions() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Built for your industry
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Tailored solutions that understand the unique needs of your business
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {industries.map((industry, index) => (
            <motion.div
              key={industry.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow group cursor-pointer"
            >
              {/* Icon with gradient background */}
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${industry.color} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform`}>
                {industry.icon}
              </div>

              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {industry.name}
              </h3>
              
              <p className="text-gray-600 mb-4">
                {industry.description}
              </p>

              {/* Features */}
              <ul className="space-y-2 mb-6">
                {industry.features.map((feature) => (
                  <li key={feature} className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-sm text-gray-600">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* Success story */}
              <div className="border-t pt-4">
                <p className="text-sm font-medium text-gray-900 mb-3">
                  <strong>Success Story:</strong> {industry.successStory}
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  Learn More →
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

### **All Essential SaaS Pages Components**

#### **1. Pricing Page**
```typescript
// app/pricing/page.tsx
import { Metadata } from 'next'
import { PricingPlans } from '@/components/marketing/PricingPlans'
import { ROICalculator } from '@/components/marketing/ROICalculator'
import { PricingFAQ } from '@/components/marketing/PricingFAQ'

export const metadata: Metadata = {
  title: 'Pricing - NLyzer Visual Search',
  description: 'Transparent pricing for visual search that pays for itself. Start with our free trial.',
}

export default function PricingPage() {
  return (
    <div className="min-h-screen">
      <PricingPlans />
      <ROICalculator />
      <PricingFAQ />
    </div>
  )
}
```

#### **2. Case Studies Page**
```typescript
// app/case-studies/page.tsx
import { Metadata } from 'next'
import { allCaseStudies } from 'contentlayer/generated'
import { CaseStudyGrid } from '@/components/marketing/CaseStudyGrid'
import { IndustryFilter } from '@/components/marketing/IndustryFilter'

export const metadata: Metadata = {
  title: 'Case Studies - Real Results from NLyzer Customers',
  description: 'See how businesses across industries increased conversions with visual search.',
}

export default function CaseStudiesPage() {
  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Real Results from Real Customers
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See how businesses across industries increased conversions and revenue with visual search
          </p>
        </div>
        
        <IndustryFilter />
        <CaseStudyGrid caseStudies={allCaseStudies} />
      </div>
    </div>
  )
}
```

#### **3. About Page**
```typescript
// app/about/page.tsx
import { Metadata } from 'next'
import { TeamSection } from '@/components/marketing/TeamSection'
import { CompanyStats } from '@/components/marketing/CompanyStats'
import { CompanyTimeline } from '@/components/marketing/CompanyTimeline'

export const metadata: Metadata = {
  title: 'About Us - The Visual Search Revolution',
  description: 'Learn about NLyzer\'s mission to revolutionize e-commerce with visual search technology.',
}

export default function AboutPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="pt-20 pb-16 bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Revolutionizing E-commerce with Visual Search
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            We believe every customer should find exactly what they're looking for, 
            and visual search makes that possible.
          </p>
        </div>
      </section>

      <CompanyStats />
      <CompanyTimeline />
      <TeamSection />
    </div>
  )
}
```

#### **4. Contact Page**
```typescript
// app/contact/page.tsx
import { Metadata } from 'next'
import { ContactForm } from '@/components/forms/ContactForm'
import { ContactInfo } from '@/components/marketing/ContactInfo'

export const metadata: Metadata = {
  title: 'Contact Us - Get Started with Visual Search',
  description: 'Ready to transform your e-commerce experience? Contact our team for a personalized demo.',
}

export default function ContactPage() {
  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-6">
              Let's Transform Your Customer Experience
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Ready to see how visual search can increase your conversions? 
              Let's schedule a personalized demo with your products.
            </p>
            <ContactInfo />
          </div>
          <div>
            <ContactForm />
          </div>
        </div>
      </div>
    </div>
  )
}
```

#### **5. Documentation Hub**
```typescript
// app/docs/page.tsx
import { Metadata } from 'next'
import { DocsSidebar } from '@/components/docs/DocsSidebar'
import { DocsContent } from '@/components/docs/DocsContent'

export const metadata: Metadata = {
  title: 'Documentation - NLyzer Developer Resources',
  description: 'Complete guides, API references, and tutorials for integrating visual search.',
}

export default function DocsPage() {
  return (
    <div className="min-h-screen pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <DocsSidebar />
          </div>
          <div className="lg:col-span-3">
            <DocsContent />
          </div>
        </div>
      </div>
    </div>
  )
}
```

#### **6. Blog**
```typescript
// app/blog/page.tsx
import { Metadata } from 'next'
import { allPosts } from 'contentlayer/generated'
import { BlogGrid } from '@/components/blog/BlogGrid'
import { BlogCategories } from '@/components/blog/BlogCategories'

export const metadata: Metadata = {
  title: 'Blog - Visual Search Insights & E-commerce Tips',
  description: 'Latest insights on visual search, e-commerce optimization, and customer experience.',
}

export default function BlogPage() {
  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Visual Commerce Insights
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Latest insights on visual search, e-commerce optimization, and creating exceptional customer experiences
          </p>
        </div>
        
        <div className="grid lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <BlogCategories />
          </div>
          <div className="lg:col-span-3">
            <BlogGrid posts={allPosts} />
          </div>
        </div>
      </div>
    </div>
  )
}
```

#### **7. Legal Pages (Privacy, Terms, etc.)**
```typescript
// app/legal/privacy/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Privacy Policy - NLyzer',
  description: 'How we collect, use, and protect your data.',
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="prose prose-lg max-w-none">
          <h1>Privacy Policy</h1>
          <p className="lead">
            Last updated: {new Date().toLocaleDateString()}
          </p>
          {/* Privacy policy content */}
        </div>
      </div>
    </div>
  )
}
```

---

## SEO Optimization Strategy

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"id": "1", "content": "Analyze existing homepage design and documentation", "status": "completed", "priority": "high"}, {"id": "2", "content": "Define modern tech stack recommendations", "status": "completed", "priority": "high"}, {"id": "3", "content": "Create component architecture for all SaaS pages", "status": "completed", "priority": "high"}, {"id": "4", "content": "Define SEO optimization strategy", "status": "in_progress", "priority": "medium"}, {"id": "5", "content": "Document performance and deployment considerations", "status": "pending", "priority": "medium"}]