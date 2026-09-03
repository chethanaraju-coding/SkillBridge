import React, { useState } from 'react';
import { X, Calendar, Clock, Video, AlertCircle } from 'lucide-react';
import { sessionsApi } from '../api/sessions';

export default function ScheduleSessionModal({ initialData, onClose, onSuccess }) {
  // initialData may contain { teacher_id, learner_id, skill_id, partner_name, skill_name }
  const [formData, setFormData] = useState({
    teacher_id: initialData?.teacher_id || '',
    learner_id: initialData?.learner_id || '',
    skill_id: initialData?.skill_id || '',
    session_date: '',
    start_time: '10:00',
    end_time: '11:00',
    meeting_link: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await sessionsApi.createSession({
        teacher_id: Number(formData.teacher_id),
        learner_id: Number(formData.learner_id),
        skill_id: Number(formData.skill_id),
        session_date: formData.session_date,
        start_time: formData.start_time,
        end_time: formData.end_time || undefined,
        meeting_link: formData.meeting_link.trim() || undefined,
      });

      if (onSuccess) onSuccess();
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to schedule learning session.');
    } finally {
      setLoading(false);
    }
  };

  // Minimum date is today
  const todayStr = new Date().toISOString().split('T')[0];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">Schedule Learning Session</h3>
          <button onClick={onClose} className="close-btn" aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        {initialData?.partner_name && (
          <div style={{ marginBottom: '1.25rem', padding: '0.85rem', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Partner: <strong>{initialData.partner_name}</strong>
            </div>
            {initialData.skill_name && (
              <div style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--primary)', marginTop: '0.2rem' }}>
                Skill: {initialData.skill_name}
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="alert alert-danger">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="session_date">
              <Calendar size={14} style={{ display: 'inline', marginRight: '4px' }} />
              Date:
            </label>
            <input
              type="date"
              id="session_date"
              name="session_date"
              min={todayStr}
              required
              className="form-input"
              value={formData.session_date}
              onChange={handleChange}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="start_time">
                <Clock size={14} style={{ display: 'inline', marginRight: '4px' }} />
                Start Time:
              </label>
              <input
                type="time"
                id="start_time"
                name="start_time"
                required
                className="form-input"
                value={formData.start_time}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="end_time">
                End Time:
              </label>
              <input
                type="time"
                id="end_time"
                name="end_time"
                className="form-input"
                value={formData.end_time}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="meeting_link">
              <Video size={14} style={{ display: 'inline', marginRight: '4px' }} />
              Meeting Link (Optional):
            </label>
            <input
              type="url"
              id="meeting_link"
              name="meeting_link"
              placeholder="e.g. https://meet.google.com/xyz or leave empty for auto-generated room"
              className="form-input"
              value={formData.meeting_link}
              onChange={handleChange}
            />
            <small style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.25rem', display: 'block' }}>
              Leave blank to automatically create a secure virtual meeting room.
            </small>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              <Calendar size={16} />
              {loading ? 'Scheduling...' : 'Schedule Session'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
