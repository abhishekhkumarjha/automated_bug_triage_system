import React, { useEffect, useState } from 'react';
import { Search, RefreshCw, Download, Filter } from 'lucide-react';
import { BugTable } from '../components/BugTable';
import { Button } from '../components/ui/Button';
import { bugService, BugHistoryItem } from '../services/api';

export const DashboardPage = () => {
  const [bugs, setBugs] = useState<BugHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const data = await bugService.getHistory();
      setBugs(data);
    } catch (err) {
      console.error('Failed to fetch bug history', err);
      setBugs([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const filteredBugs = bugs.filter(bug => 
    bug.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    bug.assigned_to.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Bug History</h1>
          <p className="text-slate-500 mt-1">Overview of all triaged bugs and their assignments.</p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={fetchHistory} isLoading={isLoading}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Total Bugs</p>
          <p className="text-3xl font-bold text-slate-900">{bugs.length}</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">High Priority</p>
          <p className="text-3xl font-bold text-rose-600">
            {bugs.filter(b => b.priority.toLowerCase() === 'high').length}
          </p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Avg. Confidence</p>
          <p className="text-3xl font-bold text-indigo-600">
            {bugs.length > 0 
              ? ((bugs.reduce((acc, b) => acc + b.confidence, 0) / bugs.length) * 100).toFixed(0) 
              : 0}%
          </p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
          <p className="text-sm font-medium text-slate-500 mb-1">Teams Active</p>
          <p className="text-3xl font-bold text-slate-900">
            {new Set(bugs.map(b => b.assigned_to)).size}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search by title or team..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
          />
        </div>
        <Button variant="outline">
          <Filter className="h-4 w-4 mr-2" />
          Filters
        </Button>
      </div>

      <BugTable bugs={filteredBugs} />
    </div>
  );
};
