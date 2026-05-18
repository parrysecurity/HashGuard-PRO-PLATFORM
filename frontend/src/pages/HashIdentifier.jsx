import React, { useState } from 'react'
import Layout from '../components/Layout'
import axios from 'axios'
import toast from 'react-hot-toast'
import { Copy, Check, AlertCircle } from 'lucide-react'

const HashIdentifier = () => {
  const [hashInput, setHashInput] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const identifyHash = async () => {
    if (!hashInput.trim()) {
      toast.error('Please enter a hash value')
      return
    }

    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post('/api/hash/identify', 
        { hash: hashInput },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setResults(response.data)
      toast.success('Hash identified successfully!')
    } catch (error) {
      toast.error('Failed to identify hash')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    toast.success('Copied to clipboard!')
    setTimeout(() => setCopied(false), 2000)
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return 'text-green-500'
    if (confidence >= 70) return 'text-yellow-500'
    return 'text-red-500'
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Hash Identifier</h1>
          <p className="text-gray-400">Analyze cryptographic hashes and identify their algorithms</p>
        </div>

        {/* Input Section */}
        <div className="glass-effect p-6 mb-8">
          <label className="block text-sm font-medium mb-2">Enter Hash Value</label>
          <textarea
            value={hashInput}
            onChange={(e) => setHashInput(e.target.value)}
            placeholder="5d41402abc4b2a76b9719d911017c592"
            className="cyber-input font-mono"
            rows="3"
          />
          <div className="flex gap-4 mt-4">
            <button
              onClick={identifyHash}
              disabled={loading}
              className="cyber-button flex-1"
            >
              {loading ? 'Analyzing...' : 'Identify Hash'}
            </button>
            <button
              onClick={() => setHashInput('')}
              className="px-6 py-3 bg-gray-800 rounded-lg hover:bg-gray-700 transition-all"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results && (
          <div className="space-y-6">
            <div className="glass-effect p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-semibold">Detection Results</h2>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(results, null, 2))}
                  className="p-2 hover:bg-gray-700 rounded-lg transition-all"
                >
                  {copied ? <Check className="w-5 h-5 text-green-500" /> : <Copy className="w-5 h-5" />}
                </button>
              </div>

              <div className="space-y-4">
                {results.identifications.map((result, idx) => (
                  <div key={idx} className="border border-gray-700 rounded-lg p-4 hover:border-primary-500 transition-all">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="text-lg font-semibold text-primary-400">{result.type}</h3>
                        <p className="text-sm text-gray-400">Bit Length: {result.bit_length}</p>
                      </div>
                      <div className={`text-2xl font-bold ${getConfidenceColor(result.confidence)}`}>
                        {result.confidence}%
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4 mt-4">
                      <div>
                        <p className="text-sm text-gray-400 mb-1">Common Uses</p>
                        <ul className="list-disc list-inside text-sm">
                          {result.common_uses.map((use, i) => (
                            <li key={i}>{use}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <p className="text-sm text-gray-400 mb-1">Cracking Tools</p>
                        <div className="flex gap-2 flex-wrap">
                          <span className="px-2 py-1 bg-gray-800 rounded text-xs">
                            Hashcat Mode: {result.tools.hashcat}
                          </span>
                          <span className="px-2 py-1 bg-gray-800 rounded text-xs">
                            John: {result.tools.john}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="mt-3 pt-3 border-t border-gray-700">
                      <div className={`text-sm font-medium ${result.security_rating.includes('SECURE') ? 'text-green-500' : 'text-red-500'}`}>
                        Security Rating: {result.security_rating}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Original Hash */}
            <div className="glass-effect p-6">
              <h3 className="text-lg font-semibold mb-3">Original Hash</h3>
              <code className="block p-3 bg-gray-900 rounded-lg font-mono text-sm break-all">
                {results.hash}
              </code>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default HashIdentifier
