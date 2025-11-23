"use client";

import { useState } from 'react';
import { Search, Mic, Image as ImageIcon, MapPin } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SearchBar() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const handleVoiceSearch = () => {
    setIsVoiceActive(true);
    // Implement Web Speech API for voice search
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setSearchQuery(transcript);
        handleSearch(transcript);
      };
      recognition.start();
    }
  };

  const handleImageSearch = () => {
    // Trigger file upload for image search
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e: any) => {
      const file = e.target.files[0];
      if (file) {
        // Call image search API
        console.log('Image search:', file);
      }
    };
    input.click();
  };

  const handleSearch = async (query: string = searchQuery) => {
    if (!query.trim()) return;
    
    // Call search API
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/search/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location: query,
          property_type: null,
          min_price: null,
          max_price: null,
        }),
      });
      
      const data = await response.json();
      console.log('Search results:', data);
      // Navigate to results page or show results
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  return (
    <div className="relative max-w-4xl mx-auto">
      <div className="flex items-center gap-3 bg-white rounded-2xl shadow-2xl p-2 border border-gray-200">
        {/* Location prefix */}
        <div className="flex items-center gap-2 px-4 text-gray-500">
          <MapPin className="w-5 h-5" />
        </div>

        {/* Search Input */}
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Search by city, area, or property type..."
          className="flex-1 px-4 py-4 text-lg outline-none border-none focus:ring-0"
        />

        {/* Voice Search Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleVoiceSearch}
          className={`p-4 rounded-xl transition-colors ${
            isVoiceActive
              ? 'bg-red-100 text-red-600'
              : 'hover:bg-gray-100 text-gray-600'
          }`}
          title="Voice Search"
        >
          <Mic className={`w-5 h-5 ${
            isVoiceActive ? 'animate-pulse' : ''
          }`} />
        </motion.button>

        {/* Image Search Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleImageSearch}
          className="p-4 rounded-xl hover:bg-gray-100 text-gray-600 transition-colors"
          title="Image Search"
        >
          <ImageIcon className="w-5 h-5" />
        </motion.button>

        {/* Search Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => handleSearch()}
          className="px-8 py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-shadow"
        >
          <Search className="w-5 h-5" />
        </motion.button>
      </div>

      {/* Quick Filters */}
      <div className="flex flex-wrap gap-2 mt-4 justify-center">
        {['Dubai', 'Abu Dhabi', 'Riyadh', 'Doha'].map((city) => (
          <button
            key={city}
            onClick={() => {
              setSearchQuery(city);
              handleSearch(city);
            }}
            className="px-4 py-2 bg-white rounded-full text-sm font-medium text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-colors shadow-sm"
          >
            {city}
          </button>
        ))}
      </div>
    </div>
  );
}
