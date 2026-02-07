# Bloom Frontend Implementation Guide

## Overview
This guide walks you through implementing the frontend for Bloom, your cycle-tracking and reflection app. The frontend uses Django templates, vanilla JavaScript, and a thoughtfully designed CSS system.

---

## 1. Directory Structure Setup

Create this structure in your Django project:

```
Bloom/
├── static/
│   ├── css/
│   │   ├── base.css              # Design system & core styles
│   │   ├── components.css        # Reusable components
│   │   └── pages/
│   │       ├── auth.css          # Login/signup pages
│   │       ├── dashboard.css     # Today/dashboard page
│   │       ├── calendar.css      # Calendar view
│   │       ├── insights.css      # Insights page
│   │       └── garden.css        # Garden visualization
│   ├── js/
│   │   ├── main.js               # Core app logic
│   │   └── components/
│   │       ├── calendar.js       # Calendar component
│   │       ├── check-in.js       # Daily check-in form
│   │       ├── period-logger.js  # Period logging
│   │       └── insights.js       # Data visualizations
│   └── images/
│       ├── favicon.png
│       └── icons/
│           └── (SVG icons)
├── templates/
│   ├── base.html                 # Master template
│   ├── components/               # Reusable template parts
│   │   ├── header.html
│   │   ├── navigation.html
│   │   └── modals/
│   │       ├── period-log.html
│   │       └── edit-entry.html
│   └── pages/
│       ├── auth/
│       │   ├── login.html        # us1_create_login
│       │   ├── signup.html       # us1_create_login
│       │   └── password_reset.html  # us2_password_reset
│       ├── dashboard/
│       │   ├── today.html        # us3_start_tracking
│       │   └── onboarding.html   # us3_start_tracking
│       ├── calendar/
│       │   ├── calendar.html     # us8_calendar_view
│       │   └── day-detail.html   # us6_editing_possible_mistakes
│       ├── tracking/
│       │   ├── log-period.html   # us4_cycle_tracking
│       │   └── edit-entry.html   # us6_editing_possible_mistakes
│       ├── insights/
│       │   └── insights.html     # us5_calc_period_length
│       └── garden/
│           └── garden.html       # Future: visualization
```

---

## 2. Setting Up Static Files in Django

### Update settings.py:

```python
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (if users upload images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### In your main urls.py:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # your url patterns
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 3. Creating Templates for Each User Story

### US1: Create Login (us1_create_login)

**templates/pages/auth/login.html** - Already created above

**templates/pages/auth/signup.html:**

```django
{% extends "base.html" %}
{% load static %}

{% block title %}Create Your Account{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <div class="auth-header">
            <h1>Begin Your Journey</h1>
            <p class="auth-subtitle">Create your Bloom account</p>
        </div>
        
        <form method="post" class="auth-form">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_email" class="form-label">Email</label>
                {{ form.email }}
            </div>
            
            <div class="form-group">
                <label for="id_username" class="form-label">Username</label>
                {{ form.username }}
            </div>
            
            <div class="form-group">
                <label for="id_password1" class="form-label">Password</label>
                {{ form.password1 }}
            </div>
            
            <div class="form-group">
                <label for="id_password2" class="form-label">Confirm Password</label>
                {{ form.password2 }}
            </div>
            
            <div class="form-group">
                <label class="checkbox-label">
                    <input type="checkbox" name="agree_terms" required>
                    <span>I agree to the <a href="/privacy">Privacy Policy</a></span>
                </label>
            </div>
            
            <button type="submit" class="btn btn-primary btn-full">
                Create Account
            </button>
        </form>
        
        <div class="auth-footer">
            <p>Already have an account?</p>
            <a href="{% url 'login' %}" class="btn btn-soft btn-full">
                Log in
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

### US2: Password Reset (us2_password_reset)

**templates/pages/auth/password_reset.html:**

```django
{% extends "base.html" %}

{% block title %}Reset Password{% endblock %}

{% block content %}
<div class="auth-container">
    <div class="auth-card">
        <h1>Reset Your Password</h1>
        <p class="text-muted">Enter your email and we'll send you a reset link</p>
        
        <form method="post" class="auth-form">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_email" class="form-label">Email</label>
                {{ form.email }}
            </div>
            
            <button type="submit" class="btn btn-primary btn-full">
                Send Reset Link
            </button>
        </form>
        
        <div class="auth-footer">
            <a href="{% url 'login' %}" class="link-secondary">Back to login</a>
        </div>
    </div>
</div>
{% endblock %}
```

### US3: Start Tracking (us3_start_tracking)

**templates/pages/dashboard/onboarding.html:**

```django
{% extends "base.html" %}

{% block title %}Welcome to Bloom{% endblock %}

{% block content %}
<div class="container container-narrow">
    <div class="onboarding-flow">
        <div class="onboarding-step">
            <div class="onboarding-icon">🌸</div>
            <h1>Welcome to Bloom!</h1>
            <p>Let's get started by tracking your first period.</p>
            
            <form method="post" class="onboarding-form">
                {% csrf_token %}
                
                <div class="form-group">
                    <label class="form-label">When did your last period start?</label>
                    <input type="date" name="last_period_start" class="form-input" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Average cycle length (optional)</label>
                    <select name="avg_cycle_length" class="form-select">
                        <option value="">I'm not sure</option>
                        {% for days in cycle_lengths %}
                        <option value="{{ days }}">{{ days }} days</option>
                        {% endfor %}
                    </select>
                    <span class="form-help">Most cycles are 21-35 days. Don't worry if you're not sure—we'll learn together!</span>
                </div>
                
                <button type="submit" class="btn btn-primary btn-full">
                    Continue
                </button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### US4: Cycle Tracking (us4_cycle_tracking)

**templates/pages/tracking/log-period.html:**

```django
{% extends "base.html" %}

{% block title %}Log Period{% endblock %}

{% block content %}
<div class="container container-narrow">
    <div class="page-header">
        <h1>Log Your Period</h1>
        <p class="text-muted">Track when your period starts and ends</p>
    </div>
    
    <form method="post" class="tracking-form card">
        {% csrf_token %}
        
        <div class="form-group">
            <label class="form-label">
                <span class="label-icon">📅</span>
                Start Date
            </label>
            <input type="date" name="start_date" class="form-input" required 
                   value="{{ today|date:'Y-m-d' }}">
        </div>
        
        <div class="form-group">
            <label class="form-label">
                <span class="label-icon">📅</span>
                End Date
                <span class="label-optional">(leave blank if ongoing)</span>
            </label>
            <input type="date" name="end_date" class="form-input">
        </div>
        
        <div class="form-group">
            <label class="form-label">
                <span class="label-icon">💧</span>
                Flow Intensity
            </label>
            <div class="flow-selector">
                <label class="flow-option">
                    <input type="radio" name="flow" value="light">
                    <span class="flow-visual">💧</span>
                    <span>Light</span>
                </label>
                <label class="flow-option">
                    <input type="radio" name="flow" value="medium" checked>
                    <span class="flow-visual">💧💧</span>
                    <span>Medium</span>
                </label>
                <label class="flow-option">
                    <input type="radio" name="flow" value="heavy">
                    <span class="flow-visual">💧💧💧</span>
                    <span>Heavy</span>
                </label>
            </div>
        </div>
        
        <div class="form-group">
            <label class="form-label">
                <span class="label-icon">📝</span>
                Notes
            </label>
            <textarea name="notes" class="form-textarea" 
                      placeholder="Any observations about this cycle?"></textarea>
        </div>
        
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">
                Save Period
            </button>
            <a href="{% url 'dashboard' %}" class="btn btn-ghost">
                Cancel
            </a>
        </div>
    </form>
</div>
{% endblock %}
```

### US5: Calculate Period Length (us5_calc_period_length)

**templates/pages/insights/insights.html:**

```django
{% extends "base.html" %}

{% block title %}Your Insights{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Your Cycle Insights</h1>
        <p class="text-muted">Patterns and predictions based on your tracking</p>
    </div>
    
    <div class="insights-grid">
        <!-- Average Cycle Length -->
        <div class="insight-card">
            <div class="insight-icon">📊</div>
            <h3>Average Cycle Length</h3>
            <div class="insight-value">{{ avg_cycle_length }} days</div>
            <p class="insight-description">
                Based on {{ period_count }} tracked cycles
            </p>
        </div>
        
        <!-- Average Period Length -->
        <div class="insight-card">
            <div class="insight-icon">🩸</div>
            <h3>Average Period Length</h3>
            <div class="insight-value">{{ avg_period_length }} days</div>
            <p class="insight-description">
                Your periods typically last {{ avg_period_length }} days
            </p>
        </div>
        
        <!-- Next Period Prediction -->
        <div class="insight-card insight-card-highlight">
            <div class="insight-icon">🔮</div>
            <h3>Next Period Prediction</h3>
            <div class="insight-value">{{ next_period_date|date:"F j" }}</div>
            <p class="insight-description">
                Expected in {{ days_until_next }} days
            </p>
        </div>
        
        <!-- Cycle Regularity -->
        <div class="insight-card">
            <div class="insight-icon">📈</div>
            <h3>Cycle Regularity</h3>
            <div class="insight-value">{{ regularity }}%</div>
            <p class="insight-description">
                {% if regularity >= 80 %}
                Your cycles are quite regular!
                {% elif regularity >= 60 %}
                Your cycles show moderate consistency
                {% else %}
                Your cycles vary—that's okay!
                {% endif %}
            </p>
        </div>
    </div>
    
    <!-- Cycle Length Chart -->
    <div class="chart-section card">
        <h3>Cycle Length Over Time</h3>
        <canvas id="cycleLengthChart"></canvas>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{% static 'js/components/insights.js' %}"></script>
<script>
    const cycleData = {{ cycle_data|safe }};
    initCycleLengthChart(cycleData);
</script>
{% endblock %}
```

### US6: Editing Possible Mistakes (us6_editing_possible_mistakes)

**templates/pages/calendar/day-detail.html:**

```django
{% extends "base.html" %}

{% block title %}Edit {{ date|date:"F j, Y" }}{% endblock %}

{% block content %}
<div class="container container-narrow">
    <div class="day-detail-header">
        <a href="{% url 'calendar' %}" class="back-link">← Back to calendar</a>
        <h1>{{ date|date:"l, F j, Y" }}</h1>
    </div>
    
    {% if period_entry %}
    <div class="entry-card card">
        <div class="entry-header">
            <h3>Period Entry</h3>
            <button class="btn btn-ghost btn-sm" onclick="toggleEdit('period')">
                Edit
            </button>
        </div>
        
        <div id="period-view" class="entry-view">
            <p><strong>Start:</strong> {{ period_entry.start_date|date:"F j, Y" }}</p>
            {% if period_entry.end_date %}
            <p><strong>End:</strong> {{ period_entry.end_date|date:"F j, Y" }}</p>
            {% endif %}
            <p><strong>Flow:</strong> {{ period_entry.get_flow_display }}</p>
        </div>
        
        <form id="period-edit" method="post" class="entry-edit" style="display: none;">
            {% csrf_token %}
            <input type="hidden" name="entry_type" value="period">
            
            <div class="form-group">
                <label class="form-label">Start Date</label>
                <input type="date" name="start_date" class="form-input" 
                       value="{{ period_entry.start_date|date:'Y-m-d' }}">
            </div>
            
            <div class="form-group">
                <label class="form-label">End Date</label>
                <input type="date" name="end_date" class="form-input" 
                       value="{{ period_entry.end_date|date:'Y-m-d' }}">
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-sm">Save</button>
                <button type="button" class="btn btn-ghost btn-sm" onclick="toggleEdit('period')">Cancel</button>
                <button type="button" class="btn-delete" onclick="deleteEntry('period', {{ period_entry.id }})">Delete</button>
            </div>
        </form>
    </div>
    {% endif %}
    
    {% if check_in %}
    <div class="entry-card card">
        <div class="entry-header">
            <h3>Daily Check-in</h3>
            <button class="btn btn-ghost btn-sm" onclick="toggleEdit('checkin')">
                Edit
            </button>
        </div>
        
        <div id="checkin-view" class="entry-view">
            <p><strong>Mood:</strong> {{ check_in.get_mood_display }}</p>
            <p><strong>Energy:</strong> {{ check_in.energy }}/3</p>
            {% if check_in.symptoms %}
            <p><strong>Symptoms:</strong> {{ check_in.get_symptoms_display }}</p>
            {% endif %}
            {% if check_in.notes %}
            <p><strong>Notes:</strong> {{ check_in.notes }}</p>
            {% endif %}
        </div>
        
        <form id="checkin-edit" method="post" class="entry-edit" style="display: none;">
            {# Edit form similar to check-in #}
        </form>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block extra_js %}
<script>
function toggleEdit(type) {
    const view = document.getElementById(`${type}-view`);
    const edit = document.getElementById(`${type}-edit`);
    
    if (view.style.display === 'none') {
        view.style.display = 'block';
        edit.style.display = 'none';
    } else {
        view.style.display = 'none';
        edit.style.display = 'block';
    }
}

function deleteEntry(type, id) {
    if (confirm('Are you sure you want to delete this entry?')) {
        fetch(`/api/delete/${type}/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': BloomApp.getCookie('csrftoken')
            }
        }).then(() => {
            window.location.href = '{% url "calendar" %}';
        });
    }
}
</script>
{% endblock %}
```

### US8: Calendar View (us8_calendar_view)

**templates/pages/calendar/calendar.html:**

```django
{% extends "base.html" %}
{% load static %}

{% block title %}Calendar{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/calendar.css' %}">
{% endblock %}

{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Your Cycle Calendar</h1>
        <a href="{% url 'log_period' %}" class="btn btn-primary">
            Log Period
        </a>
    </div>
    
    <div id="bloom-calendar"></div>
    
    <!-- Day detail sidebar (shows when day is clicked) -->
    <div id="day-sidebar" class="day-sidebar" style="display: none;">
        <div class="sidebar-header">
            <h3 id="sidebar-date"></h3>
            <button class="btn-close" onclick="closeSidebar()">×</button>
        </div>
        <div id="sidebar-content"></div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/components/calendar.js' %}"></script>
<script>
    const calendar = new BloomCalendar('bloom-calendar', {
        periods: {{ periods_json|safe }},
        predictions: {{ predictions_json|safe }},
        checkIns: {{ checkins_json|safe }},
        onDateClick: (date) => {
            showDayDetail(date);
        }
    });
    
    function showDayDetail(date) {
        // Fetch day details via AJAX
        fetch(`/api/day-detail/${date}/`)
            .then(r => r.json())
            .then(data => {
                document.getElementById('sidebar-date').textContent = data.formatted_date;
                document.getElementById('sidebar-content').innerHTML = data.html;
                document.getElementById('day-sidebar').style.display = 'block';
            });
    }
    
    function closeSidebar() {
        document.getElementById('day-sidebar').style.display = 'none';
    }
</script>
{% endblock %}
```

---

## 4. Styling Components

**static/css/components.css:**

```css
/* ========================================
   NAVIGATION
   ======================================== */

.nav-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-lg);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-family: var(--font-heading);
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--bloom-primary-dark);
  text-decoration: none;
}

.logo-icon {
  font-size: var(--text-2xl);
}

.nav-links {
  display: flex;
  list-style: none;
  gap: var(--space-md);
  margin: 0;
  padding: 0;
}

.nav-link {
  padding: var(--space-sm) var(--space-md);
  color: var(--bloom-text-secondary);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.nav-link:hover {
  background-color: var(--bloom-surface-soft);
  color: var(--bloom-text-primary);
}

.nav-link.active {
  background-color: var(--bloom-primary-light);
  color: var(--bloom-primary-dark);
  font-weight: 500;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.nav-icon {
  color: var(--bloom-text-secondary);
  transition: color var(--transition-fast);
}

.nav-icon:hover {
  color: var(--bloom-primary-dark);
}

/* ========================================
   ALERTS
   ======================================== */

.alert {
  position: relative;
  padding: var(--space-md) var(--space-lg);
  margin-bottom: var(--space-md);
  border-radius: var(--radius-md);
  background-color: var(--bloom-surface);
  border: 1px solid var(--bloom-border);
  transition: opacity var(--transition-base);
}

.alert-success {
  background-color: var(--success);
  color: white;
  border-color: var(--success);
}

.alert-error {
  background-color: var(--error);
  color: white;
  border-color: var(--error);
}

.alert-info {
  background-color: var(--info);
  color: white;
  border-color: var(--info);
}

.alert-close {
  position: absolute;
  top: var(--space-sm);
  right: var(--space-sm);
  background: none;
  border: none;
  font-size: var(--text-2xl);
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
}

.alert-close:hover {
  opacity: 1;
}

/* ========================================
   CALENDAR STYLES
   ======================================== */

.calendar {
  background-color: var(--bloom-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-lg);
}

.calendar-title {
  margin: 0;
  font-size: var(--text-2xl);
}

.calendar-nav {
  background: none;
  border: none;
  padding: var(--space-sm);
  cursor: pointer;
  color: var(--bloom-text-secondary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.calendar-nav:hover {
  background-color: var(--bloom-surface-soft);
  color: var(--bloom-primary-dark);
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.calendar-weekday {
  text-align: center;
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--bloom-text-secondary);
  padding: var(--space-sm);
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: var(--space-sm);
}

.calendar-day {
  position: relative;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 2px solid transparent;
}

.calendar-day:hover {
  background-color: var(--bloom-surface-soft);
}

.calendar-day-other {
  color: var(--bloom-text-muted);
  cursor: default;
}

.calendar-day-today {
  border-color: var(--bloom-primary);
  font-weight: 600;
}

.calendar-day-selected {
  background-color: var(--bloom-primary-light);
}

.calendar-day-period {
  background-color: var(--phase-menstrual);
  color: white;
}

.calendar-day-predicted {
  background-color: var(--bloom-primary-light);
  border: 2px dashed var(--bloom-primary);
}

.calendar-day-checkin::after {
  content: '';
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 6px;
  height: 6px;
  background-color: var(--bloom-secondary);
  border-radius: 50%;
}

.day-number {
  font-size: var(--text-sm);
}

.day-indicators {
  position: absolute;
  top: 2px;
  left: 2px;
  font-size: 10px;
}

.calendar-legend {
  display: flex;
  gap: var(--space-lg);
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--bloom-border-light);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--text-sm);
  color: var(--bloom-text-secondary);
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-dot.period {
  background-color: var(--phase-menstrual);
}

.legend-dot.predicted {
  background-color: var(--bloom-primary-light);
  border: 2px dashed var(--bloom-primary);
}

.legend-dot.check-in {
  background-color: var(--bloom-secondary);
}

/* ========================================
   MOOD & SYMPTOM SELECTORS
   ======================================== */

.mood-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: var(--space-sm);
}

.mood-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-md);
  background-color: var(--bloom-surface-soft);
  border: 2px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.mood-option:hover {
  background-color: var(--bloom-primary-light);
}

.mood-option.active {
  background-color: var(--bloom-primary-light);
  border-color: var(--bloom-primary);
}

.mood-emoji {
  font-size: var(--text-2xl);
}

.mood-label {
  font-size: var(--text-xs);
  color: var(--bloom-text-secondary);
}

.symptoms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-sm);
}

.symptom-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background-color: var(--bloom-surface-soft);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.symptom-checkbox:has(input:checked) {
  background-color: var(--bloom-primary-light);
  border: 1px solid var(--bloom-primary);
}

.symptom-checkbox input {
  margin: 0;
}

/* ========================================
   RESPONSIVE
   ======================================== */

@media (max-width: 768px) {
  .nav-main {
    flex-direction: column;
    align-items: stretch;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
  
  .mood-selector {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .calendar-weekday {
    font-size: var(--text-xs);
  }
  
  .day-number {
    font-size: var(--text-xs);
  }
}
```

---

## 5. Next Steps

1. **Copy files to your project:**
   - Copy CSS files to `static/css/`
   - Copy JS files to `static/js/`
   - Copy template files to `templates/`

2. **Run Django commands:**
   ```bash
   python manage.py collectstatic
   python manage.py runserver
   ```

3. **Test each user story:**
   - Create test views in your Django apps
   - Wire up URL patterns
   - Test forms and validation

4. **Customize:**
   - Adjust colors in CSS variables
   - Add your own illustrations/icons
   - Refine copy to match Bloom's voice

5. **Accessibility:**
   - Add ARIA labels
   - Test keyboard navigation
   - Ensure color contrast

---

This setup gives you a solid, compassionate frontend that matches Bloom's philosophy. The design is clean, the components are reusable, and the user experience prioritizes emotional safety and reflection.
