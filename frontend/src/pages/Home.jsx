import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Sparkles,
  ArrowRight,
  Repeat,
  GraduationCap,
  Users,
  Video,
  CheckCircle2,
  BookOpen,
  Compass
} from 'lucide-react';

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-pill">
          <Sparkles size={16} />
          <span>The Academic Skill Exchange Platform</span>
        </div>

        <h1 className="hero-title">
          Learn, Teach, and <span className="gradient-text">Exchange Skills</span> Peer-to-Peer
        </h1>

        <p className="hero-desc">
          SkillBridge bridges the gap between learners and knowledge sharers. Offer skills you excel at, find peers to teach you what you want to master, and collaborate in real-time.
        </p>

        <div className="hero-actions">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="btn btn-primary btn-lg">
                Go to Dashboard <ArrowRight size={18} />
              </Link>
              <Link to="/skills" className="btn btn-secondary btn-lg">
                <Compass size={18} /> Explore Catalog
              </Link>
            </>
          ) : (
            <>
              <Link to="/register" className="btn btn-primary btn-lg">
                Join SkillBridge Free <ArrowRight size={18} />
              </Link>
              <Link to="/skills" className="btn btn-secondary btn-lg">
                <Compass size={18} /> Browse Skills
              </Link>
            </>
          )}
        </div>
      </section>

      {/* Value Pillars */}
      <section style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 1.5rem 5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>The Core Philosophy</h2>
          <p style={{ color: 'var(--text-muted)' }}>LEARN + TEACH + EXCHANGE + CONNECT</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem' }}>
          {/* Card 1 */}
          <div className="card card-hover" style={{ borderTop: '4px solid var(--primary)' }}>
            <div className="stat-icon" style={{ background: 'var(--primary-light)', color: 'var(--primary)', marginBottom: '1.25rem' }}>
              <GraduationCap size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Teach Your Talents</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
              Share your expertise in programming, design, languages, mathematics, or music. Inspire fellow peers and strengthen your own mastery.
            </p>
          </div>

          {/* Card 2 */}
          <div className="card card-hover" style={{ borderTop: '4px solid var(--secondary)' }}>
            <div className="stat-icon" style={{ background: 'var(--secondary-light)', color: 'var(--secondary)', marginBottom: '1.25rem' }}>
              <BookOpen size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Learn From Others</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
              Get direct 1-on-1 guidance from students and mentors who have already walked the path. Ask questions freely and receive personalized feedback.
            </p>
          </div>

          {/* Card 3 */}
          <div className="card card-hover" style={{ borderTop: '4px solid var(--accent)' }}>
            <div className="stat-icon" style={{ background: 'var(--accent-light)', color: 'var(--accent)', marginBottom: '1.25rem' }}>
              <Repeat size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Skill Exchange Matching</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
              Our smart exchange algorithm connects you with peers where your offerings match their desires and vice-versa. Mutual growth with zero financial barrier.
            </p>
          </div>

          {/* Card 4 */}
          <div className="card card-hover" style={{ borderTop: '4px solid var(--success)' }}>
            <div className="stat-icon" style={{ background: 'var(--success-light)', color: 'var(--success)', marginBottom: '1.25rem' }}>
              <Video size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Interactive Sessions</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
              Schedule collaborative learning sessions with integrated calendar management and automated virtual meeting room links.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section style={{ background: 'var(--bg-surface)', padding: '5rem 1.5rem', borderTop: '1px solid var(--border-subtle)', borderBottom: '1px solid var(--border-subtle)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
            <h2 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>How SkillBridge Works</h2>
            <p style={{ color: 'var(--text-muted)' }}>Simple, transparent, and collaborative in 4 easy steps</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '2rem' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '48px', height: '48px', background: 'var(--primary)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem', fontWeight: 800, fontSize: '1.2rem' }}>
                1
              </div>
              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.4rem' }}>Post Your Skills</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                Add what you can teach and what topics you are eager to learn.
              </p>
            </div>

            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '48px', height: '48px', background: 'var(--secondary)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem', fontWeight: 800, fontSize: '1.2rem' }}>
                2
              </div>
              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.4rem' }}>Discover & Match</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                Explore the public skill catalog or let the algorithm pair mutual swaps.
              </p>
            </div>

            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '48px', height: '48px', background: 'var(--accent)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem', fontWeight: 800, fontSize: '1.2rem' }}>
                3
              </div>
              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.4rem' }}>Request & Accept</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                Send learning requests, discuss goals, and accept partnerships.
              </p>
            </div>

            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '48px', height: '48px', background: 'var(--success)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem', fontWeight: 800, fontSize: '1.2rem' }}>
                4
              </div>
              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.4rem' }}>Schedule & Learn</h4>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
                Set a time, hop on the meeting link, and start building new abilities.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section style={{ maxWidth: '1000px', margin: '5rem auto', padding: '0 1.5rem', textAlign: 'center' }}>
        <div style={{
          background: 'linear-gradient(135deg, var(--primary), #3730a3)',
          borderRadius: 'var(--radius-lg)',
          padding: '4rem 2rem',
          color: 'white',
          boxShadow: 'var(--shadow-xl)'
        }}>
          <h2 style={{ fontSize: '2.4rem', color: 'white', marginBottom: '1rem' }}>
            Ready to Expand Your Knowledge?
          </h2>
          <p style={{ fontSize: '1.1rem', opacity: 0.9, maxWidth: '600px', margin: '0 auto 2rem' }}>
            Join students, researchers, and creators exchanging knowledge on SkillBridge today.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/register" className="btn btn-secondary btn-lg" style={{ background: 'white', color: 'var(--primary)', fontWeight: 700 }}>
              Get Started Now <ArrowRight size={18} />
            </Link>
            <Link to="/skills" className="btn btn-outline btn-lg" style={{ borderColor: 'white', color: 'white' }}>
              Explore Skills
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
