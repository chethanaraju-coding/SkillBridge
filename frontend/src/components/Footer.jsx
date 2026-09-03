import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer style={{
      borderTop: '1px solid var(--border-subtle)',
      background: 'var(--bg-surface)',
      padding: '3rem 1.5rem 2rem',
      marginTop: 'auto'
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem' }}>
        <div>
          <div className="brand-logo" style={{ marginBottom: '1rem' }}>
            <div className="brand-icon" style={{ width: '28px', height: '28px' }}>
              <Sparkles size={16} />
            </div>
            <span>SkillBridge</span>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.6' }}>
            The academic e-learning and peer-to-peer skill-sharing platform. Learn, teach, exchange, and connect.
          </p>
        </div>

        <div>
          <h4 style={{ fontSize: '0.95rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Explore</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }}>
            <li><Link to="/skills" style={{ color: 'var(--text-muted)' }}>Browse Skills</Link></li>
            <li><Link to="/matches" style={{ color: 'var(--text-muted)' }}>Skill Exchange Matches</Link></li>
            <li><Link to="/skills?type=teach" style={{ color: 'var(--text-muted)' }}>Find Mentors</Link></li>
          </ul>
        </div>

        <div>
          <h4 style={{ fontSize: '0.95rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Platform</h4>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem' }}>
            <li><Link to="/register" style={{ color: 'var(--text-muted)' }}>Create Account</Link></li>
            <li><Link to="/login" style={{ color: 'var(--text-muted)' }}>Sign In</Link></li>
            <li><Link to="/dashboard" style={{ color: 'var(--text-muted)' }}>User Dashboard</Link></li>
          </ul>
        </div>

        <div>
          <h4 style={{ fontSize: '0.95rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Concept</h4>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
            LEARN + TEACH + EXCHANGE + CONNECT. Be both a learner and a skill provider in a collaborative academic community.
          </p>
        </div>
      </div>

      <div style={{
        maxWidth: '1280px',
        margin: '2rem auto 0',
        paddingTop: '1.5rem',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        fontSize: '0.85rem',
        color: 'var(--text-muted)'
      }}>
        <div>&copy; {new Date().getFullYear()} SkillBridge Platform. All rights reserved.</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          Built for peer-to-peer education & skill exchange
        </div>
      </div>
    </footer>
  );
}
