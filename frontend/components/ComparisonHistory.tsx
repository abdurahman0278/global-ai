'use client';

import { useState, useEffect } from 'react';
import { getHistory } from '@/lib/api';

export default function ComparisonHistory() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getHistory(10);
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 4) return 'bg-green-100 text-green-800';
    if (score >= 3) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  if (loading) {
    return <div className="text-center py-8">Loading history...</div>;
  }

  if (history.length === 0) {
    return <div className="text-center py-8 text-gray-400">No comparison history yet</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 border-b">
        <h2 className="text-xl font-bold">Recent Comparisons</h2>
      </div>
      <div className="divide-y">
        {history.map((item) => (
          <div key={item.id} className="px-6 py-4 hover:bg-gray-50">
            <div className="flex justify-between items-center">
              <div>
                <p className="font-medium">
                  {item.form_data.first_name} {item.form_data.last_name}
                </p>
                <p className="text-sm text-gray-500">
                  {new Date(item.timestamp).toLocaleString()}
                </p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(item.similarity_score)}`}>
                Score: {item.similarity_score}/5
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

