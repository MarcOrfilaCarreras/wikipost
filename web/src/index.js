import './index.css';

import React from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import IndexPage from './pages/index';
import LoginAuthPage from './pages/auth/login';
import LogoutAuthPage from './pages/auth/logout';
import RegisterAuthPage from './pages/auth/register';
import OverviewDashboardAppPage from './pages/app/dashboard/overview';
import ArticlesWikipediaAppPage from './pages/app/wikipedia/articles';
import DraftsInstagramAppPage from './pages/app/instagram/drafts';
import ScheduledInstagramAppPage from './pages/app/instagram/scheduled';
import PublishedInstagramAppPage from './pages/app/instagram/published';
import ProfileSettingsAppPage from './pages/app/settings/profile';

import * as serviceWorkerRegistration from "./serviceWorkerRegistration";

const redirectToAppIfInPWA = () => {
  if (
    window.matchMedia("(display-mode: standalone)").matches ||
    window.navigator.standalone === true
  ) {
    if (window.location.pathname === "/") {
      window.location.href = "/app/dashboard/overview";
    }
  }
};

redirectToAppIfInPWA();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path='' element={<IndexPage />} />
        <Route path='/' element={<IndexPage />} />
        <Route path='/auth/login' element={<LoginAuthPage />} />
        <Route path='/auth/logout' element={<LogoutAuthPage />} />
        <Route path='/auth/register' element={<RegisterAuthPage />} />
        <Route path='/app/dashboard/overview' element={<OverviewDashboardAppPage />} />
        <Route path='/app/wikipedia/articles' element={<ArticlesWikipediaAppPage />} />
        <Route path='/app/instagram/drafts' element={<DraftsInstagramAppPage />} />
        <Route path='/app/instagram/scheduled' element={<ScheduledInstagramAppPage />} />
        <Route path='/app/instagram/published' element={<PublishedInstagramAppPage />} />
        <Route path='/app/settings/profile' element={<ProfileSettingsAppPage />} />
        <Route path="/auth/*" element={<Navigate to="/auth/login" replace />} />
        <Route path="/app/*" element={<Navigate to="/app/dashboard/overview" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

serviceWorkerRegistration.register();
