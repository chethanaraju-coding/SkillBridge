import React from 'react';
import { useAuth } from '../context/AuthContext';
import { BookOpen, GraduationCap, User, Calendar, Edit3, Trash2, Send } from 'lucide-react';

export default function SkillCard({ skill, onEdit, onDelete, onRequest }) {
  const { user, isAuthenticated } = useAuth();
  const isOwner = isAuthenticated && user && user.id === skill.user_id;
  const isTeach = skill.skill_type === 'teach';

  return (
    <div className="card card-hover" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '0.75rem', marginBottom: '0.75rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>{skill.skill_name}</h3>
        <span className={`badge ${isTeach ? 'badge-teach' : 'badge-learn'}`}>
          {isTeach ? <GraduationCap size={14} /> : <BookOpen size={14} />}
          {isTeach ? 'Teaching' : 'Learning'}
        </span>
      </div>

      {/* Description */}
      <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', flex: 1, marginBottom: '1.25rem', lineHeight: '1.5' }}>
        {skill.description || 'No additional description provided.'}
      </p>

      {/* Metadata */}
      <div style={{
        paddingTop: '0.85rem',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '0.82rem',
        color: 'var(--text-muted)',
        marginBottom: '1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <User size={14} />
          <span>{isOwner ? 'You' : (skill.owner_name || 'Anonymous User')}</span>
        </div>
        {skill.created_at && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Calendar size={13} />
            <span>{new Date(skill.created_at).toLocaleDateString()}</span>
          </div>
        )}
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto' }}>
        {isOwner ? (
          <>
            {onEdit && (
              <button
                onClick={() => onEdit(skill)}
                className="btn btn-secondary btn-sm"
                style={{ flex: 1 }}
              >
                <Edit3 size={14} /> Edit
              </button>
            )}
            {onDelete && (
              <button
                onClick={() => onDelete(skill.id)}
                className="btn btn-danger-outline btn-sm"
                title="Delete skill"
              >
                <Trash2 size={14} />
              </button>
            )}
          </>
        ) : (
          <button
            onClick={() => onRequest && onRequest(skill)}
            className="btn btn-primary btn-sm"
            style={{ width: '100%' }}
          >
            <Send size={14} /> Request {isTeach ? 'to Learn' : 'to Teach'}
          </button>
        )}
      </div>
    </div>
  );
}
