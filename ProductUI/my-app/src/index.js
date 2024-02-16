import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ViewCart from './viewCart';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
if (window.location.pathname === '/') {
  root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
  }else if (window.location.pathname === '/viewCart') {
    root.render(
      <React.StrictMode>
        <ViewCart />
      </React.StrictMode>
    );
}
reportWebVitals();
