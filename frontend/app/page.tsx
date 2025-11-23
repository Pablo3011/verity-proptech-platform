"use client";

import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Search, 
  Mic, 
  Image as ImageIcon, 
  TrendingUp, 
  Shield, 
  Home,
  Building2,
  Landmark,
  Users,
  ChevronRight,
  Sparkles,
  BarChart3,
  Bot
} from 'lucide-react';
import SearchBar from '@/components/SearchBar';
import AnimatedBanner from '@/components/AnimatedBanner';
import FeatureCard from '@/components/FeatureCard';
import CategoryTabs from '@/components/CategoryTabs';

export default function HomePage() {
  const [activeTab, setActiveTab] = useState('buyers');

  const categories = [
    { id: 'buyers', label: 'Home Buyers', icon: Home },
    { id: 'brokers', label: 'Brokers & Agents', icon: Users },
    { id: 'developers', label: 'Developers', icon: Building2 },
    { id: 'banks', label: 'Banks & Lenders', icon: Landmark },
  ];

  const features = {
    buyers: [
      {
        title: 'AI-Powered Search',
        description: 'Find your perfect property using voice, image, or text search',
        icon: Sparkles,
        color: 'blue',
        features: ['Voice Search', 'Image Recognition', 'Smart Filters'],
      },
      {
        title: 'Property Valuation',
        description: 'Get instant AI-powered valuations with 94% accuracy',
        icon: TrendingUp,
        color: 'green',
        features: ['Market Analysis', 'Fair Price Report', 'Investment Score'],
      },
      {
        title: 'Mortgage Calculator',
        description: 'Calculate payments with real bank rates and check eligibility',
        icon: BarChart3,
        color: 'purple',
        features: ['Real Bank Rates', 'Eligibility Check', 'Payment Plans'],
      },
      {
        title: 'AI Investment Advisor',
        description: 'Smart recommendations based on your budget and preferences',
        icon: Bot,
        color: 'orange',
        features: ['ROI Predictions', 'Risk Assessment', 'Personalized Advice'],
      },
    ],
    brokers: [
      {
        title: 'Lead Management',
        description: 'AI-powered lead scoring and automated follow-ups',
        icon: Users,
        color: 'blue',
        features: ['Smart Matching', 'Auto Follow-up', 'CRM Integration'],
      },
      {
        title: 'Market Analytics',
        description: 'Real-time market data and predictive insights',
        icon: BarChart3,
        color: 'green',
        features: ['Price Trends', 'Demand Analysis', 'Competition Intel'],
      },
      {
        title: 'Virtual Tours',
        description: 'Create and share immersive 360° property tours',
        icon: ImageIcon,
        color: 'purple',
        features: ['3D Scanning', 'VR Compatible', 'Interactive Hotspots'],
      },
    ],
    developers: [
      {
        title: 'Project Showcase',
        description: 'Premium listing for your developments with analytics',
        icon: Building2,
        color: 'blue',
        features: ['Virtual Tours', 'Lead Tracking', 'Analytics Dashboard'],
      },
      {
        title: 'Demand Forecasting',
        description: 'AI predictions for market demand and pricing',
        icon: TrendingUp,
        color: 'green',
        features: ['Location Analysis', 'Price Optimization', 'Buyer Profiles'],
      },
      {
        title: 'Banner Advertising',
        description: 'Premium placement on high-traffic pages',
        icon: Sparkles,
        color: 'orange',
        features: ['Targeted Ads', 'Performance Metrics', 'A/B Testing'],
      },
    ],
    banks: [
      {
        title: 'Mortgage Integration',
        description: 'Direct API integration for rate updates and applications',
        icon: Landmark,
        color: 'blue',
        features: ['Real-time Rates', 'Auto Approvals', 'Document Upload'],
      },
      {
        title: 'Risk Assessment',
        description: 'AI-powered credit scoring and property valuation',
        icon: Shield,
        color: 'red',
        features: ['Credit Analysis', 'Property Appraisal', 'Fraud Detection'],
      },
      {
        title: 'Partner Program',
        description: 'Co-branded mortgage calculators and lead generation',
        icon: Users,
        color: 'green',
        features: ['Branded Tools', 'Lead Pipeline', 'Performance Dashboard'],
      },
    ],
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Animated Banner - Revenue Generator */}
      <AnimatedBanner />

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4" />
            AI-Powered PropTech Platform
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold font-display mb-6 bg-gradient-to-r from-primary-600 via-purple-600 to-accent-600 bg-clip-text text-transparent">
            Find Your Perfect Property
          </h1>
          
          <p className="text-xl text-gray-600 mb-12">
            Search across all listings, get AI valuations, calculate mortgages - all in one platform
          </p>

          {/* Main Search Bar */}
          <SearchBar />
        </motion.div>
      </section>

      {/* Category Tabs */}
      <section className="container mx-auto px-4 py-8">
        <CategoryTabs 
          categories={categories}
          activeTab={activeTab}
          onChange={setActiveTab}
        />
      </section>

      {/* Features Grid by Category */}
      <section className="container mx-auto px-4 pb-20">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {features[activeTab as keyof typeof features].map((feature, index) => (
            <FeatureCard key={index} {...feature} index={index} />
          ))}
        </motion.div>
      </section>

      {/* Trust Indicators */}
      <section className="container mx-auto px-4 py-16 border-t border-gray-200">
        <div className="grid md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">10K+</div>
            <div className="text-gray-600">Properties Listed</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">94%</div>
            <div className="text-gray-600">Valuation Accuracy</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">50+</div>
            <div className="text-gray-600">Bank Partners</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">24/7</div>
            <div className="text-gray-600">AI Support</div>
          </div>
        </div>
      </section>
    </main>
  );
}
