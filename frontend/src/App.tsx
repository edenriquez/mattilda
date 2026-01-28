import { useState, useEffect } from 'react'
import axios from 'axios'
import { School, FileText, ChevronRight, Activity } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5001/api'

interface SchoolData {
  id: number
  name: string
  createdAt: string
}

interface Statement {
  total_billed: number
  total_paid: number
  total_unpaid: number
}

interface SchoolStatement {
  school: SchoolData
  statement: Statement
  invoices: any[]
}

function App() {
  const [schools, setSchools] = useState<SchoolData[]>([])
  const [selectedSchool, setSelectedSchool] = useState<SchoolStatement | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchSchools()
  }, [])

  const fetchSchools = async () => {
    try {
      const response = await axios.get(`${API_BASE}/schools/`)
      setSchools(response.data.data)
      setLoading(false)
    } catch (err) {
      setError('Failed to fetch schools. Make sure the backend is running on port 5001.')
      setLoading(false)
    }
  }

  const fetchSchoolStatement = async (id: number) => {
    try {
      const response = await axios.get(`${API_BASE}/schools/${id}/statement`)
      setSelectedSchool(response.data)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="container">
      <header style={{ marginBottom: '3rem' }}>
        <h1>Mattilda Dashboard</h1>
        <p style={{ color: '#94a3b8' }}>Manage schools and financial statements with ease.</p>
      </header>

      {error && (
        <div className="card" style={{ border: '1px solid #ef4444', marginBottom: '1.5rem', color: '#f87171' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        <section>
          <h2>Schools</h2>
          <div className="grid" style={{ gridTemplateColumns: '1fr' }}>
            {loading ? (
              <p>Loading schools...</p>
            ) : (
              schools.map(school => (
                <div
                  key={school.id}
                  className="card"
                  style={{
                    cursor: 'pointer',
                    background: selectedSchool?.school.id === school.id ? 'rgba(59, 130, 246, 0.2)' : undefined,
                    borderColor: selectedSchool?.school.id === school.id ? '#3b82f6' : undefined
                  }}
                  onClick={() => fetchSchoolStatement(school.id)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                      <School size={20} color="#60a5fa" />
                      <span style={{ fontWeight: 500 }}>{school.name}</span>
                    </div>
                    <ChevronRight size={16} color="#94a3b8" />
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        <section>
          <h2>Statement Details</h2>
          {selectedSchool ? (
            <div className="card" style={{ background: 'rgba(30, 41, 59, 0.4)' }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', marginBottom: '2rem' }}>
                <Activity size={20} color="#a855f7" />
                <h3 style={{ margin: 0 }}>{selectedSchool.school.name} Overview</h3>
              </div>

              <div className="grid">
                <div className="card" style={{ background: 'rgba(255, 255, 255, 0.03)' }}>
                  <div className="stat-label">Total Billed</div>
                  <div className="stat-value" style={{ fontSize: '1.5rem', color: '#f8fafc' }}>
                    ${selectedSchool.statement.total_billed.toLocaleString()}
                  </div>
                </div>
                <div className="card" style={{ background: 'rgba(255, 255, 255, 0.03)' }}>
                  <div className="stat-label">Total Paid</div>
                  <div className="stat-value" style={{ fontSize: '1.5rem', color: '#4ade80' }}>
                    ${selectedSchool.statement.total_paid.toLocaleString()}
                  </div>
                </div>
                <div className="card" style={{ background: 'rgba(255, 255, 255, 0.03)' }}>
                  <div className="stat-label">Total Unpaid</div>
                  <div className="stat-value" style={{ fontSize: '1.5rem', color: '#f87171' }}>
                    ${selectedSchool.statement.total_unpaid.toLocaleString()}
                  </div>
                </div>
              </div>

              <div style={{ marginTop: '3rem' }}>
                <h4>Recent Invoices</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {selectedSchool.invoices.map((invoice: any) => (
                    <div key={invoice.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      background: 'rgba(0,0,0,0.2)',
                      padding: '1rem',
                      borderRadius: '8px'
                    }}>
                      <div>
                        <div style={{ fontWeight: 500 }}>{invoice.name}</div>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>ID: {invoice.id}</div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div style={{ fontWeight: 600 }}>${invoice.amount}</div>
                        <span className={`badge ${invoice.paid ? 'badge-paid' : 'badge-unpaid'}`}>
                          {invoice.paid ? 'Paid' : 'Unpaid'}
                        </span>
                      </div>
                    </div>
                  ))}
                  {selectedSchool.invoices.length === 0 && (
                    <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No invoices found.</p>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="card" style={{ textAlign: 'center', padding: '4rem', color: '#94a3b8', borderStyle: 'dashed' }}>
              <FileText size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
              <p>Select a school to view its financial highlights and invoices.</p>
            </div>
          )}
        </section>
      </div>
    </div>
  )
}

export default App
