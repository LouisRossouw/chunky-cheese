
(function() {
  let navContainer, navButton, navMenu;
  let settings = {
    position: 'bottom-left',
    urls: []
  };
  let currentView = 'shortcuts'; // 'shortcuts' or 'settings'

  function init() {
    console.log('Nav-Nav: Initializing content script...');
    if (document.getElementById('Nav-Nav-container')) return;

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', loadSettingsAndInit);
    } else {
      loadSettingsAndInit();
    }
  }

  function loadSettingsAndInit() {
    chrome.storage.local.get(['position', 'urls'], async (result) => {
      console.log('Nav-Nav: Loaded local storage', result);
      
      // Default settings
      if (result.position) settings.position = result.position;
      
      // Try to load from config.json first
      try {
        const response = await fetch(chrome.runtime.getURL('config.json'));
        if (response.ok) {
          const config = await response.json();
          console.log('Nav-Nav: Loaded config.json', config);
          if (config.position && !result.position) settings.position = config.position;
          
          // Merge URLs: priority to config.json for "static" deployment, 
          // but allow local storage to override if needed. 
          // For now, let's just combine them or use config as base.
          settings.urls = [...(config.urls || []), ...(result.urls || [])];
          
          // Remove duplicates by URL
          const uniqueUrls = [];
          const map = new Map();
          for (const item of settings.urls) {
            if (!map.has(item.url)) {
              map.set(item.url, true);
              uniqueUrls.push(item);
            }
          }
          settings.urls = uniqueUrls;
        } else {
          if (result.urls) settings.urls = result.urls;
        }
      } catch (e) {
        console.log('Nav-Nav: No config.json found or error loading it.', e);
        if (result.urls) settings.urls = result.urls;
      }
      
      createUI();
    });
  }

  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local') {
      if (changes.position) {
        settings.position = changes.position.newValue;
        updatePosition();
        if (currentView === 'settings') renderSettings();
      }
      if (changes.urls) {
        settings.urls = changes.urls.newValue;
        if (currentView === 'shortcuts') renderShortcuts();
        else renderSettings();
      }
    }
  });

  function createUI() {
    navContainer = document.createElement('div');
    navContainer.id = 'Nav-Nav-container';
    
    navButton = document.createElement('button');
    navButton.id = 'Nav-Nav-button';
    navButton.innerHTML = `
      <svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/></svg>
    `;
    
    navMenu = document.createElement('div');
    navMenu.id = 'Nav-Nav-menu';
    
    navButton.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = navMenu.classList.contains('visible');
      if (!isVisible) {
        navMenu.classList.add('visible');
        currentView = 'shortcuts';
        renderShortcuts();
      } else {
        navMenu.classList.remove('visible');
      }
    });

    document.addEventListener('click', (e) => {
      if (!navMenu.classList.contains('visible')) return;
      
      // If the target is still in the DOM and is NOT inside our container, close it.
      // If the target is NOT in the DOM (e.g. removed by innerHTML re-render), keep it open.
      const isInside = navContainer.contains(e.target) || e.target.closest?.('#site-nav-container');
      const isDetached = !document.documentElement.contains(e.target);
      
      if (!isInside && !isDetached) {
        navMenu.classList.remove('visible');
      }
    });

    navContainer.appendChild(navButton);
    navContainer.appendChild(navMenu);
    
    const attachToBody = () => {
      if (document.body) document.body.appendChild(navContainer);
      else document.documentElement.appendChild(navContainer);
    };
    attachToBody();

    updatePosition();
  }

  function updatePosition() {
    navButton.className = '';
    const posClass = `sn-${settings.position}`;
    navButton.classList.add(posClass);
    
    const isTop = settings.position.startsWith('top');
    const isLeft = settings.position.endsWith('left');
    
    navMenu.style.top = isTop ? '80px' : 'auto';
    navMenu.style.bottom = isTop ? 'auto' : '80px';
    navMenu.style.left = isLeft ? '20px' : 'auto';
    navMenu.style.right = isLeft ? 'auto' : '20px';
  }

  function renderShortcuts() {
    currentView = 'shortcuts';
    navMenu.innerHTML = `
      <div class="sn-menu-header">
        <div style="display: flex; align-items: center; gap: 8px;">
          <img src="${chrome.runtime.getURL('icons/icon128.png')}" style="width: 20px; height: 20px; border-radius: 4px;">
          <span>Nav-Nav</span>
        </div>
        <button class="sn-icon-btn" id="sn-to-settings" title="Settings">
          <svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
        </button>
      </div>
      <div class="sn-menu-content" id="sn-list"></div>
    `;

    document.getElementById('sn-to-settings').onclick = renderSettings;

    const list = document.getElementById('sn-list');
    if (settings.urls.length === 0) {
      list.innerHTML = '<div class="sn-empty-msg">No shortcuts saved. Click gear to add.</div>';
      return;
    }

    settings.urls.forEach(item => {
      const link = document.createElement('a');
      link.className = 'sn-menu-item';
      link.href = item.url;
      link.innerHTML = `
        <div class="icon">${item.name.charAt(0).toUpperCase()}</div>
        <span>${item.name}</span>
      `;
      link.onclick = (e) => { e.preventDefault(); window.location.href = item.url; };
      list.appendChild(link);
    });
  }

  function renderSettings() {
    currentView = 'settings';
    navMenu.innerHTML = `
      <div class="sn-menu-header">
        <button class="sn-icon-btn" id="sn-back" title="Back">
          <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
        </button>
        <div style="display: flex; align-items: center; gap: 8px;">
          <img src="${chrome.runtime.getURL('icons/icon128.png')}" style="width: 20px; height: 20px; border-radius: 4px;">
          <span>Settings</span>
        </div>
        <div style="width: 36px;"></div>
      </div>
      <div class="sn-menu-content">
        <div class="sn-settings-view">
          <div>
            <div class="sn-section-title">Position</div>
            <div class="sn-pos-grid">
              <div class="sn-pos-btn ${settings.position === 'top-left' ? 'active' : ''}" data-pos="top-left">Top Left</div>
              <div class="sn-pos-btn ${settings.position === 'top-right' ? 'active' : ''}" data-pos="top-right">Top Right</div>
              <div class="sn-pos-btn ${settings.position === 'bottom-left' ? 'active' : ''}" data-pos="bottom-left">Bottom Left</div>
              <div class="sn-pos-btn ${settings.position === 'bottom-right' ? 'active' : ''}" data-pos="bottom-right">Bottom Right</div>
            </div>
          </div>
          
          <div>
            <div class="sn-section-title">Add Shortcut</div>
            <div class="sn-form">
              <input type="text" id="sn-new-name" class="sn-input" placeholder="Name">
              <input type="text" id="sn-new-url" class="sn-input" placeholder="URL">
              <button id="sn-add-btn" class="sn-btn-primary">Add</button>
            </div>
          </div>

          <div>
            <div class="sn-section-title">Manage</div>
            <div class="sn-delete-list" id="sn-delete-list"></div>
          </div>
        </div>
      </div>
    `;

    document.getElementById('sn-back').onclick = renderShortcuts;
    
    document.querySelectorAll('.sn-pos-btn').forEach(btn => {
      btn.onclick = () => {
        const position = btn.dataset.pos;
        chrome.storage.local.set({ position });
      };
    });

    document.getElementById('sn-add-btn').onclick = () => {
      const name = document.getElementById('sn-new-name').value.trim();
      let url = document.getElementById('sn-new-url').value.trim();
      if (!name || !url) return;
      if (!url.startsWith('http')) url = 'https://' + url;
      
      const urls = [...settings.urls, { name, url }];
      chrome.storage.local.set({ urls });
    };

    const deleteList = document.getElementById('sn-delete-list');
    settings.urls.forEach((item, index) => {
      const div = document.createElement('div');
      div.className = 'sn-delete-item';
      div.innerHTML = `
        <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 180px; color: #ffffff !important;">${item.name}</span>
        <button class="sn-btn-delete" data-index="${index}">Delete</button>
      `;
      div.querySelector('.sn-btn-delete').onclick = () => {
        const urls = [...settings.urls];
        urls.splice(index, 1);
        chrome.storage.local.set({ urls });
      };
      deleteList.appendChild(div);
    });
  }

  init();
})();
