import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Shield, Zap, Database, Lock, TrendingUp, Users, Activity } from 'lucide-react'

const LandingPage = () => {
  const [typedText, setTypedText] = useState('')
  const fullText = 'hash-identifier > analyze_hash("5d41402abc4b2a76b9719d911017c592")'

  useEffect(() => {
    let i = 0
    const interval = setInterval(() => {
      setTypedText(fullText.slice(0, i))
      i++
      if (i > fullText.length) clearInterval(interval)
    }, 50)
    return () => clearInterval(interval)
  }, [])

  const features = [
    { icon: Shield, title: '60+ Hash Types', description: 'Support for MD5, SHA, bcrypt, Argon2, and more' },
    { icon: Zap, title: 'Real-time Analysis', description: 'Instant hash detection with confidence scores' },
    { icon: Database, title: 'Bulk Processing', description: 'Analyze thousands of hashes simultaneously' },
    { icon: Lock, title: 'Enterprise Security', description: 'Bank-grade encryption and security practices' },
    { icon: TrendingUp, title: 'API Access', description: 'RESTful API with rate limiting and API keys' },
    { icon: Users, title: 'Team Collaboration', description: 'Share results and collaborate with your team' },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600/20 via-transparent to-transparent" />
        
        <div className="container mx-auto px-6 py-20 relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <div className="inline-flex items-center gap-2 bg-primary-600/20 rounded-full px-4 py-2 mb-8">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm font-mono text-primary-400">SYSTEM ONLINE</span>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-primary-400 to-white bg-clip-text text-transparent">
              Hash Identifier
            </h1>
            
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Advanced cryptographic hash detection and analysis tool for security professionals
            </p>
            
            <div className="bg-gray-800/50 rounded-lg p-4 mb-8 max-w-2xl mx-auto border border-primary-500/30">
              <code className="text-green-400 font-mono text-sm">
                {typedText}<span className="animate-pulse">_</span>
              </code>
            </div>
            
            <div className="flex gap-4 justify-center">
              <Link to="/register" className="cyber-button">
                Get Started Free
              </Link>
              <Link to="/login" className="px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-all">
                Sign In
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
      
      {/* Features Grid */}
      <div className="container mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Enterprise-Grade Features</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Everything you need for professional hash analysis and cybersecurity operations
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="hash-card"
            >
              <feature.icon className="w-12 h-12 text-primary-500 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
      
      {/* Statistics */}
      <div className="bg-gradient-to-r from-primary-600/10 to-transparent py-16">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-500">60+</div>
              <div className="text-gray-400 mt-2">Hash Types</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-500">99.9%</div>
              <div className="text-gray-400 mt-2">Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-500">50ms</div>
              <div className="text-gray-400 mt-2">Response Time</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-500">24/7</div>
              <div className="text-gray-400 mt-2">Uptime</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
