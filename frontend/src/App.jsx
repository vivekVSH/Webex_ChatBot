import { useEffect, useState } from 'react';

export default function App() {
  const [status, setStatus] = useState('Stopped');
  const [log, setLog] = useState('Ready');

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/status');
      const data = await res.json();
      setStatus(data.status);
      setLog(`Last text: ${data.last_text || '<none>'}`);
    } catch (error) {
      setStatus('Error');
      setLog('Could not reach backend: ' + error.message);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const startBot = async () => {
    await fetch('/api/start', { method: 'POST' });
    fetchStatus();
  };

  const stopBot = async () => {
    await fetch('/api/stop', { method: 'POST' });
    fetchStatus();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Auto Reply ChatBot</h1>
        <div className="mb-4">
          <div className="flex items-center justify-between">
            <span className="text-lg font-medium text-gray-700">Status:</span>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              status === 'Running' ? 'bg-green-100 text-green-800' :
              status === 'Stopped' ? 'bg-red-100 text-red-800' :
              status === 'Processing' ? 'bg-yellow-100 text-yellow-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {status}
            </span>
          </div>
        </div>
        <div className="flex space-x-3 mb-6">
          <button
            onClick={startBot}
            className="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            Start
          </button>
          <button
            onClick={stopBot}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
          >
            Stop
          </button>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Info</h2>
          <p className="text-gray-600 text-sm">{log}</p>
        </div>
      </div>
    </div>
  );
}
