import React from 'react';
import { motion } from 'motion/react';
import { CheckCircle2, Users, ShieldAlert, Zap } from 'lucide-react';
import { Badge } from './ui/Badge';
import { BugPredictionResponse } from '@/src/services/api';

interface PredictionResultProps {
  result: BugPredictionResponse;
  onReset: () => void;
  key?: React.Key;
}

export const PredictionResult = ({ result, onReset }: PredictionResultProps) => {
  const overallConfidence = Math.max(result.assignment_confidence, result.priority_confidence);

  const getPriorityVariant = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-indigo-600 p-8 rounded-2xl shadow-xl text-white relative overflow-hidden"
    >
      {/* Background decoration */}
      <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-white/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-40 h-40 bg-indigo-400/20 rounded-full blur-3xl" />

      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-white/20 p-2 rounded-full">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <h2 className="text-2xl font-bold">Triage Successful</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <div className="flex items-center gap-2 text-indigo-100 mb-2">
              <Users className="h-4 w-4" />
              <span className="text-xs font-semibold uppercase tracking-wider">Assigned To</span>
            </div>
            <p className="text-xl font-bold">{result.assigned_to}</p>
            <p className="text-sm text-indigo-100 mt-2">
              {(result.assignment_confidence * 100).toFixed(0)}% routing confidence
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <div className="flex items-center gap-2 text-indigo-100 mb-2">
              <ShieldAlert className="h-4 w-4" />
              <span className="text-xs font-semibold uppercase tracking-wider">Priority</span>
            </div>
            <div className="flex items-center gap-2">
              <p className="text-xl font-bold">{result.priority}</p>
              <Badge variant={getPriorityVariant(result.priority)} className="bg-white/20 text-white border-none">
                {result.priority}
              </Badge>
            </div>
            <p className="text-sm text-indigo-100 mt-2">
              {(result.priority_confidence * 100).toFixed(0)}% priority confidence
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <div className="flex items-center gap-2 text-indigo-100 mb-2">
              <Zap className="h-4 w-4" />
              <span className="text-xs font-semibold uppercase tracking-wider">Overall Confidence</span>
            </div>
            <div className="flex items-end gap-2">
              <p className="text-3xl font-bold">{(overallConfidence * 100).toFixed(0)}%</p>
              <div className="flex-1 h-2 bg-white/20 rounded-full mb-2 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${overallConfidence * 100}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  className="h-full bg-white"
                />
              </div>
            </div>
          </div>
        </div>

        {result.is_duplicate && result.duplicate_info?.title ? (
          <div className="mb-8 rounded-xl border border-white/15 bg-white/10 p-4">
            <p className="text-sm font-semibold uppercase tracking-wider text-indigo-100">Possible Duplicate</p>
            <p className="mt-2 text-lg font-semibold">{result.duplicate_info.title}</p>
            <p className="mt-1 text-sm text-indigo-100">
              Similarity score: {((result.duplicate_info.similarity ?? 0) * 100).toFixed(0)}%
            </p>
          </div>
        ) : null}

        <button
          onClick={onReset}
          className="w-full py-3 bg-white text-indigo-600 font-bold rounded-xl hover:bg-indigo-50 transition-colors shadow-lg"
        >
          Submit Another Bug
        </button>
      </div>
    </motion.div>
  );
};
