import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Compass,
  Repeat,
  Calendar,
  Inbox,
  User as UserIcon,
  LogOut,
  PlusCircle,
  Sparkles,
  LayoutDashboard
} from 'lucide-react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="navbar">
      <div className="nav-container">
        {/* Brand Logo */}
        <Link to="/" className="brand-logo">
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>
          <span>SkillBridge</span>
        </Link>

        {/* Center Nav Links */}
        <nav>
          <ul className="nav-links">
            <li>
              <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} end>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to="/skills" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                <Compass size={16} /> Explore Skills
              </NavLink>
            </li>

            {isAuthenticated && (
              <>
                <li>
                  <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <LayoutDashboard size={16} /> Dashboard
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/matches" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Repeat size={16} /> Matches
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/requests" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Inbox size={16} /> Requests
                  </NavLink>
                </li>
                <li>
                  <NavLink to="/sessions" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Calendar size={16} /> Sessions
                  </NavLink>
                </li>
              </>
            )}
          </ul>
        </nav>

        {/* Right Nav Actions */}
        <div className="nav-actions">
          {isAuthenticated ? (
            <>
              <Link to="/skills/new" className="btn btn-primary btn-sm">
                <PlusCircle size={16} /> Add Skill
              </Link>
              <Link to="/profile" className="nav-link" title="My Profile">
                <div className="user-avatar" style={{ width: '32px', height: '32px', fontSize: '0.85rem' }}>
                  {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                </div>
              </Link>
              <button onClick={handleLogout} className="btn btn-secondary btn-sm" title="Log Out">
                <LogOut size={16} />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary btn-sm">
                Log In
              </Link>
              <Link to="/register" className="btn btn-primary btn-sm">
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
