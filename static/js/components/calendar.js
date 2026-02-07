// ========================================
// BLOOM - Calendar Component
// Interactive cycle calendar with period tracking
// ========================================

class BloomCalendar {
  constructor(elementId, options = {}) {
    this.container = document.getElementById(elementId);
    if (!this.container) {
      console.error(`Calendar container #${elementId} not found`);
      return;
    }
    
    this.currentDate = new Date();
    this.selectedDate = null;
    this.periods = options.periods || []; // Array of {start_date, end_date}
    this.predictions = options.predictions || []; // Predicted period dates
    this.checkIns = options.checkIns || {}; // Map of date -> check-in data
    
    this.onDateClick = options.onDateClick || (() => {});
    this.onPeriodToggle = options.onPeriodToggle || (() => {});
    
    this.render();
    this.attachEventListeners();
  }
  
  render() {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0);
    
    const firstDayWeek = firstDay.getDay();
    const lastDate = lastDay.getDate();
    const prevLastDate = prevLastDay.getDate();
    
    let html = `
      <div class="calendar">
        <div class="calendar-header">
          <button class="calendar-nav" data-action="prev-month">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <h2 class="calendar-title">${this.getMonthName(month)} ${year}</h2>
          <button class="calendar-nav" data-action="next-month">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        
        <div class="calendar-weekdays">
          <div class="calendar-weekday">Sun</div>
          <div class="calendar-weekday">Mon</div>
          <div class="calendar-weekday">Tue</div>
          <div class="calendar-weekday">Wed</div>
          <div class="calendar-weekday">Thu</div>
          <div class="calendar-weekday">Fri</div>
          <div class="calendar-weekday">Sat</div>
        </div>
        
        <div class="calendar-days">
    `;
    
    // Previous month days
    for (let i = firstDayWeek; i > 0; i--) {
      const date = prevLastDate - i + 1;
      html += `<div class="calendar-day calendar-day-other">${date}</div>`;
    }
    
    // Current month days
    for (let day = 1; day <= lastDate; day++) {
      const date = new Date(year, month, day);
      const dateStr = this.formatDate(date);
      const classes = this.getDayClasses(date);
      const indicator = this.getDayIndicator(dateStr);
      
      html += `
        <div class="calendar-day ${classes}" data-date="${dateStr}">
          <span class="day-number">${day}</span>
          ${indicator}
        </div>
      `;
    }
    
    // Next month days
    const totalDays = firstDayWeek + lastDate;
    const remainingDays = totalDays % 7 === 0 ? 0 : 7 - (totalDays % 7);
    for (let i = 1; i <= remainingDays; i++) {
      html += `<div class="calendar-day calendar-day-other">${i}</div>`;
    }
    
    html += `
        </div>
      </div>
      
      <div class="calendar-legend">
        <div class="legend-item">
          <span class="legend-dot period"></span>
          <span>Period</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot predicted"></span>
          <span>Predicted</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot check-in"></span>
          <span>Check-in</span>
        </div>
      </div>
    `;
    
    this.container.innerHTML = html;
  }
  
  getDayClasses(date) {
    const classes = [];
    const dateStr = this.formatDate(date);
    const today = this.formatDate(new Date());
    
    if (dateStr === today) {
      classes.push('calendar-day-today');
    }
    
    if (this.selectedDate && dateStr === this.selectedDate) {
      classes.push('calendar-day-selected');
    }
    
    if (this.isPeriodDay(dateStr)) {
      classes.push('calendar-day-period');
    } else if (this.isPredictedPeriod(dateStr)) {
      classes.push('calendar-day-predicted');
    }
    
    if (this.checkIns[dateStr]) {
      classes.push('calendar-day-checkin');
    }
    
    return classes.join(' ');
  }
  
  getDayIndicator(dateStr) {
    let indicators = '';
    
    if (this.checkIns[dateStr]) {
      const checkIn = this.checkIns[dateStr];
      if (checkIn.mood) {
        indicators += `<span class="day-mood" title="${checkIn.mood}">${this.getMoodEmoji(checkIn.mood)}</span>`;
      }
    }
    
    return indicators ? `<div class="day-indicators">${indicators}</div>` : '';
  }
  
  isPeriodDay(dateStr) {
    return this.periods.some(period => {
      const start = new Date(period.start_date);
      const end = period.end_date ? new Date(period.end_date) : start;
      const date = new Date(dateStr);
      return date >= start && date <= end;
    });
  }
  
  isPredictedPeriod(dateStr) {
    return this.predictions.some(pred => {
      const predDate = new Date(pred.date);
      const date = new Date(dateStr);
      const diff = Math.abs(predDate - date) / (1000 * 60 * 60 * 24);
      return diff <= pred.range; // Within prediction range
    });
  }
  
  getMoodEmoji(mood) {
    const moodEmojis = {
      calm: '😌',
      happy: '😊',
      energized: '✨',
      tender: '🌸',
      irritable: '😤',
      sad: '😔',
      anxious: '😰',
      reflective: '🤔'
    };
    return moodEmojis[mood] || '💭';
  }
  
  attachEventListeners() {
    this.container.addEventListener('click', (e) => {
      // Navigation
      const navBtn = e.target.closest('[data-action]');
      if (navBtn) {
        const action = navBtn.dataset.action;
        if (action === 'prev-month') {
          this.currentDate.setMonth(this.currentDate.getMonth() - 1);
          this.render();
          this.attachEventListeners();
        } else if (action === 'next-month') {
          this.currentDate.setMonth(this.currentDate.getMonth() + 1);
          this.render();
          this.attachEventListeners();
        }
        return;
      }
      
      // Day click
      const day = e.target.closest('.calendar-day:not(.calendar-day-other)');
      if (day && day.dataset.date) {
        this.selectedDate = day.dataset.date;
        this.render();
        this.attachEventListeners();
        this.onDateClick(this.selectedDate);
      }
    });
  }
  
  formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  getMonthName(month) {
    const names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'];
    return names[month];
  }
  
  // Update data and re-render
  updatePeriods(periods) {
    this.periods = periods;
    this.render();
    this.attachEventListeners();
  }
  
  updateCheckIns(checkIns) {
    this.checkIns = checkIns;
    this.render();
    this.attachEventListeners();
  }
}

// Export
window.BloomCalendar = BloomCalendar;
