import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Send, AlertCircle } from 'lucide-react';
import { Button } from './ui/Button';
import { bugService, BugPredictionResponse } from '@/src/services/api';

interface BugFormProps {
  onSuccess: (result: BugPredictionResponse) => void;
  key?: React.Key;
}

export const BugForm = ({ onSuccess }: BugFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await bugService.predict({ title, description });
      onSuccess(result);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError('Unable to reach the bug triage backend. Please make sure the API server is running and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100"
    >
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900">Report a Bug</h2>
        <p className="text-slate-500 mt-1">Provide details and our AI will triage it automatically.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-slate-700 mb-2">
            Bug Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Login page fails on mobile"
            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none"
            required
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-slate-700 mb-2">
            Bug Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the issue in detail..."
            rows={5}
            className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none resize-none"
            required
          />
        </div>

        {error && (
          <div className="flex items-center gap-2 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100">
            <AlertCircle className="h-5 w-5" />
            <p className="text-sm">{error}</p>
          </div>
        )}

        <Button
          type="submit"
          className="w-full py-4 text-lg"
          isLoading={isLoading}
          disabled={!title || !description}
        >
          <Send className="h-5 w-5 mr-2" />
          Analyze & Triage
        </Button>
      </form>
    </motion.div>
  );
};
