import React, { useState } from 'react';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import UploadAudio from './components/UploadAudio';
import AuditLogs from './components/AuditLogs';
import './styles.css';

// Import Amplify configuration
import awsconfig from './aws-exports';

// Configure Amplify
Amplify.configure(awsconfig);

// Create a context for refreshing data
export const RefreshContext = React.createContext(null);

function App({ signOut, user }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  
  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };
  
  return (
    <RefreshContext.Provider value={{ refreshTrigger, triggerRefresh }}>
      <div className="app-container">
        <header className="app-header">
          <div className="header-content">
            <div className="logo-container">
              <h1>EchoGuard</h1>
              <h2>Voice-to-Text Compliance Logger</h2>
            </div>
            <div className="user-info">
              <p>Welcome, <span className="username">{user.attributes.email}</span></p>
              <button className="sign-out-button" onClick={signOut}>Sign Out</button>
            </div>
          </div>
        </header>
        
        <main className="app-main">
          <div className="dashboard-container">
            <section className="upload-section">
              <UploadAudio onUploadComplete={triggerRefresh} />
            </section>
            
            <section className="logs-section">
              <AuditLogs />
            </section>
          </div>
        </main>
        
        <footer className="app-footer">
          <p>&copy; {new Date().getFullYear()} EchoGuard - AI-powered compliance monitoring</p>
          <p className="version">Version 1.0.0</p>
        </footer>
      </div>
    </RefreshContext.Provider>
  );
}

export default withAuthenticator(App);