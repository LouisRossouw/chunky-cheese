
document.addEventListener('DOMContentLoaded', restoreOptions);
document.getElementById('add-btn').addEventListener('click', addUrl);
document.getElementById('go-btn').addEventListener('click', quickNavigate);
document.querySelectorAll('input[name="position"]').forEach(radio => {
    radio.addEventListener('change', savePosition);
});

function savePosition() {
    const position = document.querySelector('input[name="position"]:checked').value;
    chrome.storage.local.set({ position }, () => {
        showStatus('Position saved!');
    });
}

function addUrl() {
    const nameInput = document.getElementById('new-name');
    const urlInput = document.getElementById('new-url');
    const name = nameInput.value.trim();
    let url = urlInput.value.trim();

    if (!name || !url) {
        showStatus('Please provide both name and URL', true);
        return;
    }

    if (!url.startsWith('http')) {
        url = 'https://' + url;
    }

    chrome.storage.local.get({ urls: [] }, (result) => {
        const urls = result.urls;
        urls.push({ name, url });
        chrome.storage.local.set({ urls }, () => {
            nameInput.value = '';
            urlInput.value = '';
            renderUrlList(urls);
            showStatus('Shortcut added!');
        });
    });
}

function quickNavigate() {
    const urlInput = document.getElementById('quick-url');
    let url = urlInput.value.trim();

    if (!url) return;
    if (!url.startsWith('http')) {
        url = 'https://' + url;
    }

    // Save it as a shortcut too if it doesn't exist
    chrome.storage.local.get({ urls: [] }, (result) => {
        let urls = result.urls;
        if (!urls.find(u => u.url === url)) {
            const name = new URL(url).hostname;
            urls.push({ name, url });
            chrome.storage.local.set({ urls }, () => {
                window.location.href = url;
            });
        } else {
            window.location.href = url;
        }
    });
}

function deleteUrl(index) {
    chrome.storage.local.get({ urls: [] }, (result) => {
        const urls = result.urls;
        urls.splice(index, 1);
        chrome.storage.local.set({ urls }, () => {
            renderUrlList(urls);
            showStatus('Shortcut removed');
        });
    });
}

function restoreOptions() {
    chrome.storage.local.get({ position: 'bottom-left', urls: [] }, (result) => {
        document.querySelector(`input[value="${result.position}"]`).checked = true;
        renderUrlList(result.urls);
    });
}

function renderUrlList(urls) {
    const list = document.getElementById('url-list');
    list.innerHTML = '';

    if (urls.length === 0) {
        list.innerHTML = '<p style="text-align: center; opacity: 0.5;">No shortcuts yet.</p>';
        return;
    }

    urls.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'url-item';
        div.innerHTML = `
            <div class="url-info">
                <span class="url-name">${item.name}</span>
                <span class="url-link">${item.url}</span>
            </div>
            <button class="delete-btn" data-index="${index}">Delete</button>
        `;
        div.querySelector('.delete-btn').addEventListener('click', () => deleteUrl(index));
        list.appendChild(div);
    });
}

function showStatus(msg, isError = false) {
    const status = document.getElementById('status');
    status.textContent = msg;
    status.style.color = isError ? '#ef4444' : '#3b82f6';
    setTimeout(() => {
        status.textContent = '';
    }, 2000);
}
