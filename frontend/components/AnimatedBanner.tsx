"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, X } from 'lucide-react';

const ads = [
  {
    id: 1,
    title: 'Emaar Properties',
    subtitle: 'Luxury Living in Downtown Dubai',
    image: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=1200',
    cta: 'Explore Now',
    link: '/developers/emaar',
    bgGradient: 'from-blue-600 to-purple-600',
  },
  {
    id: 2,
    title: 'Emirates NBD Mortgages',
    subtitle: 'Get Pre-Approved in 24 Hours - Rates from 3.99%',
    image: 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1200',
    cta: 'Apply Now',
    link: '/mortgage/enbd',
    bgGradient: 'from-green-600 to-teal-600',
  },
  {
    id: 3,
    title: 'Damac Hills 2',
    subtitle: 'Payment Plans Starting from 1% Monthly',
    image: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200',
    cta: 'View Details',
    link: '/developers/damac',
    bgGradient: 'from-orange-600 to-red-600',
  },
];

export default function AnimatedBanner() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % ads.length);
    }, 5000); // Auto-rotate every 5 seconds

    return () => clearInterval(timer);
  }, []);

  const next = () => setCurrentIndex((prev) => (prev + 1) % ads.length);
  const prev = () => setCurrentIndex((prev) => (prev - 1 + ads.length) % ads.length);

  if (!isVisible) return null;

  const currentAd = ads[currentIndex];

  return (
    <div className="relative w-full h-64 md:h-80 overflow-hidden bg-gradient-to-r from-gray-900 to-gray-800">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentAd.id}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.5 }}
          className="absolute inset-0"
        >
          {/* Background Image with Overlay */}
          <div
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: `url(${currentAd.image})` }}
          >
            <div className={`absolute inset-0 bg-gradient-to-r ${currentAd.bgGradient} opacity-90`} />
          </div>

          {/* Content */}
          <div className="relative h-full container mx-auto px-4 flex items-center">
            <div className="max-w-2xl text-white">
              <motion.h2
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="text-4xl md:text-5xl font-bold mb-4"
              >
                {currentAd.title}
              </motion.h2>
              
              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-xl md:text-2xl mb-6 text-white/90"
              >
                {currentAd.subtitle}
              </motion.p>

              <motion.a
                href={currentAd.link}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="inline-block px-8 py-4 bg-white text-gray-900 rounded-xl font-bold text-lg hover:shadow-2xl transition-shadow"
              >
                {currentAd.cta}
              </motion.a>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation Controls */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center gap-4">
        <button
          onClick={prev}
          className="p-2 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full transition-colors"
        >
          <ChevronLeft className="w-6 h-6 text-white" />
        </button>

        {/* Dots Indicator */}
        <div className="flex gap-2">
          {ads.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentIndex
                  ? 'w-8 bg-white'
                  : 'bg-white/50 hover:bg-white/70'
              }`}
            />
          ))}
        </div>

        <button
          onClick={next}
          className="p-2 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-full transition-colors"
        >
          <ChevronRight className="w-6 h-6 text-white" />
        </button>
      </div>

      {/* Close Button */}
      <button
        onClick={() => setIsVisible(false)}
        className="absolute top-4 right-4 p-2 bg-black/20 hover:bg-black/40 backdrop-blur-sm rounded-full transition-colors"
      >
        <X className="w-5 h-5 text-white" />
      </button>
    </div>
  );
}
