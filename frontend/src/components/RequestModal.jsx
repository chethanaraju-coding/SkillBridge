import React, { useState } from 'react';
import { X, Send, AlertCircle } from 'lucide-react';
import { requestsApi } from '../api/requests';

export default function RequestModal({ skill, onClose, onSuccess }) {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!skill) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await requestsApi.createRequest({
        skill_id: skill.id,
        message: message.trim() || undefined,
      });
      if (onSuccess) onSuccess();
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to submit skill request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Request Skill</h3>
          <button onClick={onClose} className="close-btn" aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        <div style={{ marginBottom: '1.25rem', padding: '0.85rem', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Target Skill:</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--primary)' }}>{skill.skill_name}</div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Provider: <strong>{skill.owner_name || 'Anonymous User'}</strong>
          </div>
        </div>

        {error && (
          <div className="alert alert-danger">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="request-message">
              Introduction & Goals (Optional):
            </label>
            <textarea
              id="request-message"
              className="form-textarea"
              placeholder="Hi, I'm interested in exchanging skills with you! Here is what I want to achieve..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={4}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              <Send size={16} />
              {loading ? 'Submitting...' : 'Send Request'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
