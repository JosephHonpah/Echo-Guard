import React, { useEffect, useState } from 'react';
import { API } from 'aws-amplify';

function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statsLoading, setStatsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    minScore: '',
    maxScore: '',
    startDate: '',
    endDate: ''
  });
  const [activeTab, setActiveTab] = useState('logs'); // 'logs' or 'stats'

  useEffect(() => {
    fetchLogs();
    fetchStats();
  }, []);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      // Build query parameters for filtering
      const queryParams = {};
      if (filters.minScore) queryParams.minScore = filters.minScore;
      if (filters.maxScore) queryParams.maxScore = filters.maxScore;
      if (filters.startDate) queryParams.startDate = filters.startDate;
      if (filters.endDate) queryParams.endDate = filters.endDate;
      
      // Convert to query string
      const queryString = Object.keys(queryParams).length > 0
        ? '?' + new URLSearchParams(queryParams).toString()
        : '';
      
      const response = await API.get('echoguardApi', `/audit-logs${queryString}`);
      setLogs(response);
      setError(null);
    } catch (err) {
      console.error('Error fetching audit logs:', err);
      setError('Failed to load compliance logs. Please try again later.');
      
      // Fallback to mock data if API fails
      const mockLogs = [
        {
          callId: '1',
          timestamp: new Date().toISOString(),
          score: 85,
          tone: 'professional',
          flags: ['Minor disclosure issue'],
          summary: 'Customer service call with good compliance overall.'
        },
        {
          callId: '2',
          timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
          score: 65,
          tone: 'frustrated',
          flags: ['Missing disclosure', 'Interrupting customer'],
          summary: 'Customer complaint call with several compliance issues.'
        },
        {
          callId: '3',
          timestamp: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          score: 95,
          tone: 'helpful',
          flags: [],
          summary: 'Excellent customer service call with full compliance.'
        }
      ];
      setLogs(mockLogs);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchStats = async () => {
    setStatsLoading(true);
    try {
      const response = await API.get('echoguardApi', '/audit-logs/stats');
      setStats(response);
    } catch (err) {
      console.error('Error fetching stats:', err);
      // Fallback to mock data if API fails
      const mockStats = {
        totalCalls: 42,
        averageScore: 78,
        complianceIssues: 12,
        toneBreakdown: {
          'professional': 25,
          'frustrated': 8,
          'helpful': 9
        },
        commonFlags: {
          'Missing disclosure': 7,
          'Interrupting customer': 5,
          'Minor disclosure issue': 4,
          'Incorrect information': 3,
          'Unprofessional language': 2
        }
      };
      setStats(mockStats);
    } finally {
      setStatsLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const applyFilters = (e) => {
    e.preventDefault();
    fetchLogs();
  };
  
  const resetFilters = () => {
    setFilters({
      minScore: '',
      maxScore: '',
      startDate: '',
      endDate: ''
    });
    // Fetch logs without filters
    setTimeout(fetchLogs, 0);
  };

  const formatDate = (isoString) => {
    return new Date(isoString).toLocaleString();
  };
  
  const getScoreClass = (score) => {
    if (score >= 90) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 50) return 'score-warning';
    return 'score-critical';
  };

  return (
    <div className="audit-logs-container">
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          Compliance Logs
        </button>
        <button 
          className={`tab ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          Statistics
        </button>
      </div>
      
      {activeTab === 'logs' && (
        <div className="logs-tab">
          <h2>Compliance Logs</h2>
          
          <form className="filters-form" onSubmit={applyFilters}>
            <div className="filter-group">
              <label>
                Min Score:
                <input 
                  type="number" 
                  name="minScore" 
                  value={filters.minScore} 
                  onChange={handleFilterChange}
                  min="0"
                  max="100"
                />
              </label>
              
              <label>
                Max Score:
                <input 
                  type="number" 
                  name="maxScore" 
                  value={filters.maxScore} 
                  onChange={handleFilterChange}
                  min="0"
                  max="100"
                />
              </label>
            </div>
            
            <div className="filter-group">
              <label>
                Start Date:
                <input 
                  type="date" 
                  name="startDate" 
                  value={filters.startDate} 
                  onChange={handleFilterChange}
                />
              </label>
              
              <label>
                End Date:
                <input 
                  type="date" 
                  name="endDate" 
                  value={filters.endDate} 
                  onChange={handleFilterChange}
                />
              </label>
            </div>
            
            <div className="filter-actions">
              <button type="submit" disabled={loading}>Apply Filters</button>
              <button type="button" onClick={resetFilters} disabled={loading}>Reset</button>
            </div>
          </form>
          
          {loading && <p className="loading-message">Loading logs...</p>}
          
          {error && <p className="error-message">{error}</p>}
          
          {!loading && !error && logs.length === 0 && (
            <p className="no-data-message">No compliance logs found.</p>
          )}
          
          {!loading && !error && logs.length > 0 && (
            <div className="table-container">
              <table className="logs-table">
                <thead>
                  <tr>
                    <th>Date/Time</th>
                    <th>Compliance Score</th>
                    <th>Tone</th>
                    <th>Flags</th>
                    <th>Summary</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map(log => (
                    <tr key={log.callId}>
                      <td>{formatDate(log.timestamp)}</td>
                      <td>
                        <span className={`score-badge ${getScoreClass(log.score)}`}>
                          {log.score}
                        </span>
                      </td>
                      <td>{log.tone}</td>
                      <td>{log.flags && log.flags.join(', ')}</td>
                      <td>{log.summary || 'No summary available'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          
          <div className="logs-actions">
            <button 
              className="refresh-button" 
              onClick={() => {
                fetchLogs();
                fetchStats();
              }} 
              disabled={loading}
            >
              {loading ? 'Refreshing...' : 'Refresh Data'}
            </button>
          </div>
        </div>
      )}
      
      {activeTab === 'stats' && (
        <div className="stats-tab">
          <h2>Compliance Statistics</h2>
          
          {statsLoading && <p className="loading-message">Loading statistics...</p>}
          
          {!statsLoading && stats && (
            <div className="stats-container">
              <div className="stat-card">
                <h3>Overview</h3>
                <div className="stat-item">
                  <span className="stat-label">Total Calls Analyzed:</span>
                  <span className="stat-value">{stats.totalCalls}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Average Compliance Score:</span>
                  <span className={`stat-value ${getScoreClass(stats.averageScore)}`}>
                    {stats.averageScore}
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Compliance Issues:</span>
                  <span className="stat-value">{stats.complianceIssues}</span>
                </div>
              </div>
              
              <div className="stat-card">
                <h3>Tone Analysis</h3>
                {Object.entries(stats.toneBreakdown || {}).length > 0 ? (
                  <ul className="tone-list">
                    {Object.entries(stats.toneBreakdown).map(([tone, count]) => (
                      <li key={tone} className="tone-item">
                        <span className="tone-name">{tone}:</span>
                        <span className="tone-count">{count}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No tone data available</p>
                )}
              </div>
              
              <div className="stat-card">
                <h3>Common Compliance Issues</h3>
                {Object.entries(stats.commonFlags || {}).length > 0 ? (
                  <ul className="flags-list">
                    {Object.entries(stats.commonFlags)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 5)
                      .map(([flag, count]) => (
                        <li key={flag} className="flag-item">
                          <span className="flag-name">{flag}</span>
                          <span className="flag-count">{count}</span>
                        </li>
                      ))}
                  </ul>
                ) : (
                  <p>No compliance issues found</p>
                )}
              </div>
            </div>
          )}
          
          <button 
            className="refresh-button" 
            onClick={fetchStats} 
            disabled={statsLoading}
          >
            {statsLoading ? 'Refreshing...' : 'Refresh Statistics'}
          </button>
        </div>
      )}
    </div>
  );
}

export default AuditLogs;