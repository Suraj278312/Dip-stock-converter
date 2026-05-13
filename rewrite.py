import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS variables
css_vars = """
    :root {
      /* Light Mode by Default */
      --bg-color: #f1f5f9;
      --card-bg: rgba(255, 255, 255, 0.85);
      --card-border: rgba(148, 163, 184, 0.2);
      --text-main: #0f172a;
      --text-muted: #64748b;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --accent: #10b981;
      --accent-hover: #059669;
      --danger: #ef4444;
      --input-bg: rgba(255, 255, 255, 0.9);
      --bg-gradient: radial-gradient(circle at top right, #e2e8f0, #f1f5f9);
    }

    [data-theme="dark"] {
      --bg-color: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.1);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --accent: #10b981;
      --accent-hover: #059669;
      --danger: #ef4444;
      --input-bg: rgba(15, 23, 42, 0.6);
      --bg-gradient: radial-gradient(circle at top right, #1e1b4b, #0f172a);
    }
"""
content = re.sub(r':root\s*\{.*?\}(?=\s*\* \{)', css_vars, content, flags=re.DOTALL)

# 2. Update body CSS
body_css = """
    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      display: flex;
      justify-content: center;
      min-height: 100vh;
      background-image: var(--bg-gradient);
      background-attachment: fixed;
      transition: background 0.3s, color 0.3s;
    }
"""
content = re.sub(r'body\s*\{.*?\}', body_css, content, flags=re.DOTALL, count=1)

# 3. Update app-container and add dashboard-layout
layout_css = """
    .app-container {
      width: 100%;
      max-width: 1000px;
      padding: 30px 20px;
      margin: 0 auto;
    }

    .dashboard-layout {
      display: grid;
      grid-template-columns: 1fr;
      gap: 25px;
    }

    @media (min-width: 800px) {
      .dashboard-layout {
        grid-template-columns: 1.2fr 1fr;
      }
    }
    
    .header {
      text-align: center;
      padding: 10px 0 20px 0;
      position: relative;
    }
"""
# Replace app-container and header css
content = re.sub(r'\.app-container\s*\{.*?\}(?=\s*\.header)', layout_css, content, flags=re.DOTALL)
# Now remove the old header CSS that comes after
content = re.sub(r'/\* Header \*/\s*\.header\s*\{.*?\}\s*\.header\s+h1', '/* Header */\n    .header h1', content, flags=re.DOTALL)

# 4. Modify the HTML Structure
# Search for <!-- Main Calculator --> and wrap it
# Replace header
header_html = """
    <div class="header">
      <h1>Dip Stock Converter</h1>
      <p>Professional Fluid Calculation</p>
      <button id="theme-toggle" style="position: absolute; right: 0; top: 10px; background: transparent; border: none; font-size: 24px; cursor: pointer; color: var(--text-main);">
        🌓
      </button>
    </div>
    
    <div class="dashboard-layout">
      <!-- Left Column -->
      <div class="col-left">
"""
content = re.sub(r'<div class="header">.*?</div>', header_html, content, flags=re.DOTALL)

# Insert Right Column before Dip Search
right_col_html = """
      </div>
      <!-- Right Column -->
      <div class="col-right" style="display: flex; flex-direction: column; gap: 25px;">
        <!-- Dip Search -->
"""
content = content.replace('<!-- Dip Search -->', right_col_html)

# Close the Right Column and Dashboard Layout after Actions
close_html = """
      </div>
    </div>
"""
content = re.sub(r'(<!-- Actions -->.*?</div>\s*</div>)', r'\1' + close_html, content, flags=re.DOTALL)

# Also fix the actions grid-column
content = content.replace('style="grid-column: 1 / -1; justify-content: center; max-width: 600px; margin: 0 auto; width: 100%;"', 'style="justify-content: center; width: 100%;"')

# 5. Add Theme JS Logic
theme_js = """
    // --- UI Logic ---
    document.addEventListener('DOMContentLoaded', () => {
      
      // Theme Toggle
      const themeToggle = document.getElementById('theme-toggle');
      const currentTheme = localStorage.getItem('theme') || 'dark';
      document.body.setAttribute('data-theme', currentTheme);
      
      themeToggle.addEventListener('click', () => {
        const newTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
      });
"""
content = content.replace("// --- UI Logic ---\n    document.addEventListener('DOMContentLoaded', () => {", theme_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
