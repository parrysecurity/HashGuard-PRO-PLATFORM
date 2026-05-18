import React, { useState, useEffect } from 'react'
import Layout from '../components/Layout'
import { Activity, Hash, Users, TrendingUp, Clock, Star } from 'lucide-react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [recentHashes, setRecentHashes] = useState([])

  useEffect(() => {
    fetchStats()
    fetchRecentHashes()
  }, [])

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/admin/stats', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch stats', error)
    }
  }

  const fetchRecentHashes = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/hash/history', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setRecentHashes(response.data.slice(0, 5))
    } catch (error) {
      console.error('Failed to fetch history', error)
    }
  }

  const statCards = [
    { title: 'Total Scans', value: stats?.total_scans || 0, icon: Hash, color: 'text-blue-500' },
    { title: 'API Calls', value: stats?.api_calls || 0, icon: TrendingUp, color: 'text-green-500' },
    { title: 'Active Users', value: stats?.active_users || 0, icon: Users, color: 'text-purple-500' },
    { title: 'Unique Hashes', value: stats?.top_hashes?.length || 0, icon: Activity, color: 'text-yellow-500' },
  ]

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.username}!</h1>
          <p className="text-gray-400">Here's your hash analysis overview</p>
        </div>

        {/* Stats Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, idx) => (
            <div key={idx} className="glass-effect p-6">
              <div className="flex items-center justify-between mb-4">
                <stat.icon className={`w-8 h-8 ${stat.color}`} />
                <span className="text-2xl font-bold">{stat.value}</span>
              </div>
              <h3 className="text-gray-400">{stat.title}</h3>
            </div>
          ))}
        </div>

        {/* Recent Activity */}
        <div className="grid lg:grid-cols-2 gap-8">
          <div className="glass-effect p-6">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-primary-500" />
              <h2 className="text-xl font-semibold">Recent Hash Analysis</h2>
            </div>
            <div className="space-y-3">
              {recentHashes.map((item, idx) => (
                <div key={idx} className="border-b border-gray-700 pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <code className="text-sm font-mono text-green-400">
                        {item.hash.substring(0, 20)}...
                      </code>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(item.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <span className="px-2 py-1 bg-primary-600/20 rounded text-xs">
                      {item.type}
                    </span>
                  </div>
                </div>
              ))}
              {recentHashes.length === 0 && (
                <p className="text-gray-400 text-center py-4">No recent analyses</p>
              )}
            </div>
          </div>

          <div className="glass-effect p-6">
            <div className="flex items-center gap-2 mb-4">
              <Star className="w-5 h-5 text-yellow-500" />
              <h2 className="text-xl font-semibold">Quick Actions</h2>
            </div>
            <div className="space-y-4">
              <button
                onClick={() => window.location.href = '/identifier'}
                className="w-full cyber-button"
              >
                Analyze New Hash
              </button>
              <button
                onClick={() => window.location.href = '/bulk'}
                className="w-full px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-all"
              >
                Bulk Analysis
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Dashboard
