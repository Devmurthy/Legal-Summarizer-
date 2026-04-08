import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import { LogIn, UserPlus, Clock, LogOut, FileText, UploadCloud, Settings, FileUp, Activity, FileSearch, FilePlus, LayoutList, Text, Hash, Gavel, Scale } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5002/api';

function Login({ setToken }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_URL}/login`, { email, password });
      setToken(res.data.token);
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="glass-panel" style={{ width: '400px', maxWidth: '90%' }}>
      <h2 style={{ marginBottom: '8px', fontSize: '2rem' }}>Welcome Back</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '32px' }}>Sign in to access your Legal Document Summarizer</p>
      
      {error && <div style={{ color: '#ef4444', marginBottom: '16px', fontSize: '0.9rem' }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <input type="email" className="input-field" placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" className="input-field" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" className="btn-primary" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          <LogIn size={20} /> Sign In
        </button>
      </form>
      <p style={{ marginTop: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        Don't have an account? <Link to="/signup" className="link">Sign up</Link>
      </p>
    </div>
  );
}

function Signup({ setToken }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_URL}/signup`, { name, email, password });
      setToken(res.data.token);
    } catch (err) {
      setError(err.response?.data?.error || 'Signup failed');
    }
  };

  return (
    <div className="glass-panel" style={{ width: '400px', maxWidth: '90%' }}>
      <h2 style={{ marginBottom: '8px', fontSize: '2rem' }}>Create Account</h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '32px' }}>Join us to analyze legal documents faster</p>
      
      {error && <div style={{ color: '#ef4444', marginBottom: '16px', fontSize: '0.9rem' }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <input type="text" className="input-field" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="email" className="input-field" placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" className="input-field" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" className="btn-primary" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          <UserPlus size={20} /> Create Account
        </button>
      </form>
      <p style={{ marginTop: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
        Already have an account? <Link to="/login" className="link">Sign in</Link>
      </p>
    </div>
  );
}

function Timeline({ token }) {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchTimeline = async () => {
      try {
        const res = await axios.get(`${API_URL}/timeline`, { headers: { Authorization: `Bearer ${token}` } });
        setEvents(res.data);
      } catch (err) {
        console.error('Error fetching timeline', err);
      }
    };
    fetchTimeline();
  }, [token]);

  return (
    <div className="timeline-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
        <div>
          <h1 style={{ marginBottom: '10px', fontSize: '2.5rem' }}>Your Journey</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>Track all your interactions and generated summaries.</p>
        </div>
        <Link to="/summarizer" className="btn-primary" style={{ width: 'auto', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <FilePlus size={20} /> New Summarization
        </Link>
      </div>

      {events.length === 0 ? (
        <div className="glass-panel" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
          No events found. Start generating summaries!
        </div>
      ) : (
        events.map((ev, index) => (
          <div className="timeline-event" key={ev.id}>
            <div className="timeline-dot">
              {index === 0 ? <Clock size={20} color="white" /> : <div style={{ width: 10, height: 10, borderRadius: '50%', background: 'white' }} />}
            </div>
            <div className="timeline-content glass-panel" style={{ padding: '24px', marginTop: '-10px' }}>
              <h3 className="timeline-title">{ev.title}</h3>
              <p className="timeline-desc">{ev.description}</p>
              <span className="timeline-date">{new Date(ev.timestamp).toLocaleString()}</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}


function Summarizer({ token }) {
  const [file, setFile] = useState(null);
  const [extNum, setExtNum] = useState(5);
  const [absMin, setAbsMin] = useState(40);
  const [absMax, setAbsMax] = useState(150);
  const [ocrMode, setOcrMode] = useState("Default");
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('entities');

  const handleSummarize = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF or Image file.");
      return;
    }
    setError('');
    setLoading(true);

    const formData = new FormData();
    formData.append("document", file);
    formData.append("ext_num", extNum);
    formData.append("abs_min", absMin);
    formData.append("abs_max", absMax);
    formData.append("ocr_mode", ocrMode);

    try {
      // Send to Flask Engine
      const res = await axios.post(`${API_URL}/summarize`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult(res.data);

      // Successfully processed, so save action to Timeline via Node.js backend
      await axios.post(`${API_URL}/timeline`, {
        title: "Generated Document Summary",
        description: `Successfully analyzed \`${file.name}\`. Detected ${res.data.entities.length} logical entities and generated summaries.`
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || "Failed to process document. Make sure the Flask server is running on port 5001.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', width: '100%', padding: '20px' }}>
       <h1 style={{ marginBottom: '10px', fontSize: '2.5rem' }}>Document Analysis Engine</h1>
       <p style={{ color: 'var(--text-secondary)', marginBottom: '30px', fontSize: '1.1rem' }}>Extract insights, entities, and summaries securely from your legal documents.</p>

       <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) 2fr', gap: '30px' }}>
          
          <div className="glass-panel" style={{ height: 'fit-content' }}>
            <h3 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}><Settings size={20}/> Configuration</h3>
            
            {error && <div style={{ color: '#ef4444', marginBottom: '16px', background: 'rgba(239, 68, 68, 0.1)', padding: '10px', borderRadius: '8px' }}>{error}</div>}

            <form onSubmit={handleSummarize}>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>Upload Document (PDF/Img)</label>
                <input 
                  type="file" 
                  onChange={(e) => setFile(e.target.files[0])}
                  className="input-field"
                  style={{ background: 'rgba(255,255,255,0.05)', padding: '12px', border: '2px dashed var(--glass-border)', cursor: 'pointer' }}
                  accept=".pdf,.png,.jpg,.jpeg"
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>Extractive Sentences: {extNum}</label>
                <input type="range" min="3" max="15" value={extNum} onChange={(e) => setExtNum(e.target.value)} style={{ width: '100%' }} />
              </div>

              <div style={{ marginBottom: '20px', display: 'flex', gap: '10px' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>Min Abs Len</label>
                  <input type="number" className="input-field" value={absMin} onChange={(e) => setAbsMin(e.target.value)} />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>Max Abs Len</label>
                  <input type="number" className="input-field" value={absMax} onChange={(e) => setAbsMax(e.target.value)} />
                </div>
              </div>

              <div style={{ marginBottom: '30px' }}>
                <label style={{ display: 'block', marginBottom: '10px', color: 'var(--text-secondary)' }}>OCR Engine Mode</label>
                <select className="input-field" value={ocrMode} onChange={(e) => setOcrMode(e.target.value)} style={{ background: '#1e293b' }}>
                  <option value="Default">Default Print</option>
                  <option value="Handwritten">Handwritten Text</option>
                </select>
              </div>

              <button type="submit" disabled={loading} className="btn-primary" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', opacity: loading ? 0.7 : 1 }}>
                {loading ? <div className="spinner" style={{ width: 20, height: 20, border: '2px solid white', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} /> : <FileSearch size={20} />}
                {loading ? 'Processing Document...' : 'Analyze Document'}
              </button>
            </form>
          </div>

          <div className="glass-panel" style={{ minHeight: '500px' }}>
            {!result && !loading && (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', textAlign: 'center' }}>
                <UploadCloud size={64} style={{ marginBottom: '20px', opacity: 0.5 }} />
                <h3>No Data Available</h3>
                <p>Upload a document and configure parameters to see intelligent insights here.</p>
              </div>
            )}
            
            {loading && (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--accent-color)' }}>
                <Activity size={48} className="pulse-anim" style={{ marginBottom: '20px' }} />
                <h3>Processing Document...</h3>
                <p style={{ color: 'var(--text-secondary)', marginTop: '10px' }}>This may take a moment depending on document size.</p>
              </div>
            )}

            {result && !loading && (
              <div>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '30px', borderBottom: '1px solid var(--glass-border)', paddingBottom: '20px' }}>
                   <div style={{ flex: 1, padding: '15px', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', textAlign: 'center' }}>
                     <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white' }}>{result.text.split(' ').length}</div>
                     <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Words Parsed</div>
                   </div>
                   <div style={{ flex: 1, padding: '15px', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', textAlign: 'center' }}>
                     <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent-color)' }}>{result.entities.length}</div>
                     <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Entities Detected</div>
                   </div>
                </div>

                <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                   <button onClick={() => setActiveTab('entities')} style={{ padding: '10px 20px', background: activeTab === 'entities' ? 'var(--accent-color)' : 'transparent', color: 'white', border: '1px solid var(--accent-color)', borderRadius: '8px', cursor: 'pointer', display: 'flex', gap: '8px' }}><Hash size={18}/> Entities</button>
                   <button onClick={() => setActiveTab('extractive')} style={{ padding: '10px 20px', background: activeTab === 'extractive' ? 'var(--accent-color)' : 'transparent', color: 'white', border: '1px solid var(--accent-color)', borderRadius: '8px', cursor: 'pointer', display: 'flex', gap: '8px' }}><LayoutList size={18}/> Extractive</button>
                   <button onClick={() => setActiveTab('abstractive')} style={{ padding: '10px 20px', background: activeTab === 'abstractive' ? 'var(--accent-color)' : 'transparent', color: 'white', border: '1px solid var(--accent-color)', borderRadius: '8px', cursor: 'pointer', display: 'flex', gap: '8px' }}><FileText size={18}/> Abstractive</button>
                   <button onClick={() => setActiveTab('legal_acts')} style={{ padding: '10px 20px', background: activeTab === 'legal_acts' ? 'var(--accent-color)' : 'transparent', color: 'white', border: '1px solid var(--accent-color)', borderRadius: '8px', cursor: 'pointer', display: 'flex', gap: '8px' }}><Scale size={18}/> Legal Acts</button>
                   <button onClick={() => setActiveTab('raw')} style={{ padding: '10px 20px', background: activeTab === 'raw' ? 'var(--accent-color)' : 'transparent', color: 'white', border: '1px solid var(--accent-color)', borderRadius: '8px', cursor: 'pointer', display: 'flex', gap: '8px' }}><Text size={18}/> Raw Text</button>
                </div>

                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '20px', borderRadius: '12px', maxHeight: '400px', overflowY: 'auto', lineHeight: '1.6' }}>
                  {activeTab === 'raw' && <div style={{ whiteSpace: 'pre-wrap' }}>{result.text}</div>}
                  {activeTab === 'extractive' && <div style={{ whiteSpace: 'pre-wrap' }}>{result.ext_summary}</div>}
                  {activeTab === 'abstractive' && <div style={{ whiteSpace: 'pre-wrap' }}>{result.abs_summary}</div>}
                  {activeTab === 'legal_acts' && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                      {result.legal_acts.length === 0 ? "No specific legal acts identified." : result.legal_acts.map((act, i) => (
                        <div key={i} style={{ padding: '15px', background: 'rgba(139, 92, 246, 0.1)', border: '1px solid rgba(139, 92, 246, 0.3)', borderRadius: '10px' }}>
                           <h4 style={{ color: '#a78bfa', marginBottom: '5px', display: 'flex', alignItems: 'center', gap: '8px' }}><Gavel size={16}/> {act.act}</h4>
                           <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>{act.suggestion}</p>
                        </div>
                      ))}
                    </div>
                  )}
                  {activeTab === 'entities' && (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                      {result.entities.length === 0 ? "No entities found." : result.entities.map((e, i) => (
                        <span key={i} style={{ padding: '5px 12px', background: 'rgba(139, 92, 246, 0.2)', border: '1px solid rgba(139, 92, 246, 0.5)', borderRadius: '20px', fontSize: '0.9rem' }}>
                          <strong style={{ color: '#fff' }}>{e[0]}</strong> <span style={{ color: '#a78bfa', fontSize: '0.8rem', marginLeft: '5px' }}>{e[1]}</span>
                        </span>
                      ))}
                    </div>
                  )}
                </div>

              </div>
            )}
          </div>
       </div>
       <style>{`
          @keyframes spin { 100% { transform: rotate(360deg); } }
          .pulse-anim { animation: pulse 2s infinite ease-in-out; }
          @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); opacity: 0.8; } 100% { transform: scale(1); } }
       `}</style>
    </div>
  )
}


function Nav({ token, handleLogout }) {
  const location = useLocation();
  return (
    <nav className="nav-header">
      <div style={{ fontSize: '1.25rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{ width: 36, height: 36, borderRadius: 12, background: 'var(--accent-color)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <FileText size={20} color="white" />
        </div>
        Legal Summarizer
      </div>
      <div style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
        <Link to="/" className="link" style={{ color: location.pathname === '/' ? 'white' : 'var(--text-secondary)' }}>Timeline</Link>
        <Link to="/summarizer" className="link" style={{ color: location.pathname === '/summarizer' ? 'white' : 'var(--text-secondary)' }}>Summarizer Hub</Link>
        <div style={{ width: '1px', height: '24px', background: 'var(--glass-border)' }}></div>
        <button onClick={handleLogout} className="btn-primary" style={{ padding: '8px 16px', borderRadius: '8px', background: 'transparent', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', gap: '8px', width: 'auto' }}>
          <LogOut size={16} /> Logout
        </button>
      </div>
    </nav>
  )
}

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <Router>
      {token && <Nav token={token} handleLogout={handleLogout} />}
      
      <div style={{ paddingTop: token ? '80px' : '0', width: '100%', minHeight: token ? 'calc(100vh - 80px)' : '100vh', display: 'flex', justifyContent: 'center', alignItems: token ? 'flex-start' : 'center' }}>
        <Routes>
          <Route path="/login" element={!token ? <Login setToken={setToken} /> : <Navigate to="/" />} />
          <Route path="/signup" element={!token ? <Signup setToken={setToken} /> : <Navigate to="/" />} />
          <Route path="/" element={token ? <Timeline token={token} /> : <Navigate to="/login" />} />
          <Route path="/summarizer" element={token ? <Summarizer token={token} /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}
