import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { SubmitBugPage } from './pages/SubmitBug';
import { DashboardPage } from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<SubmitBugPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </main>
        
        <footer className="py-8 border-t border-slate-200 bg-white">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-sm text-slate-500">
              &copy; {new Date().getFullYear()} BugTriage AI. All rights reserved.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
