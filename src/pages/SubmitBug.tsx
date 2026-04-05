import React, { useState } from 'react';
import { AnimatePresence } from 'motion/react';
import { BugForm } from '../components/BugForm';
import { PredictionResult } from '../components/PredictionResult';
import { BugPredictionResponse } from '../services/api';

export const SubmitBugPage = () => {
  const [prediction, setPrediction] = useState<BugPredictionResponse | null>(null);

  return (
    <div className="max-w-3xl mx-auto py-12 px-4">
      <AnimatePresence mode="wait">
        {!prediction ? (
          <BugForm key="form" onSuccess={setPrediction} />
        ) : (
          <PredictionResult 
            key="result" 
            result={prediction} 
            onReset={() => setPrediction(null)} 
          />
        )}
      </AnimatePresence>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-2xl border border-slate-100">
          <h4 className="font-bold text-slate-900 mb-2">Automated Triage</h4>
          <p className="text-sm text-slate-500">Our AI analyzes bug reports to assign them to the right team instantly.</p>
        </div>
        <div className="p-6 bg-white rounded-2xl border border-slate-100">
          <h4 className="font-bold text-slate-900 mb-2">Priority Prediction</h4>
          <p className="text-sm text-slate-500">Automatically identifies critical issues that need immediate attention.</p>
        </div>
        <div className="p-6 bg-white rounded-2xl border border-slate-100">
          <h4 className="font-bold text-slate-900 mb-2">High Confidence</h4>
          <p className="text-sm text-slate-500">Trained on thousands of bug reports to ensure accurate classifications.</p>
        </div>
      </div>
    </div>
  );
};
