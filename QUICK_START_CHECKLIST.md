# Bloom Frontend Quick Start Checklist

## 📋 Pre-Implementation

- [ ] Review design system in `bloom-frontend-base.css`
- [ ] Understand file structure in `BLOOM_FRONTEND_GUIDE.md`
- [ ] Ensure Django static files are configured

## 🎨 Step 1: Setup Static Files Structure

```bash
cd Bloom
mkdir -p static/css/pages
mkdir -p static/js/components
mkdir -p static/images/icons
mkdir -p templates/pages/auth
mkdir -p templates/pages/dashboard
mkdir -p templates/pages/calendar
mkdir -p templates/pages/tracking
mkdir -p templates/pages/insights
```

## 📁 Step 2: Copy Core Files

### CSS Files
- [ ] Copy `bloom-frontend-base.css` → `static/css/base.css`
- [ ] Copy `components.css` → `static/css/components.css`
- [ ] Copy `auth.css` → `static/css/pages/auth.css`
- [ ] Copy `dashboard.css` → `static/css/pages/dashboard.css`

### JavaScript Files
- [ ] Copy `main.js` → `static/js/main.js`
- [ ] Copy `calendar.js` → `static/js/components/calendar.js`

### Template Files
- [ ] Copy `base.html` → `templates/base.html`
- [ ] Copy `login.html` → `templates/pages/auth/login.html`
- [ ] Copy `dashboard.html` → `templates/pages/dashboard/today.html`

## 🔧 Step 3: Configure Django Settings

Add to `settings.py`:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## 🌐 Step 4: Create URL Patterns

Example `urls.py`:
```python
from django.urls import path
from apps.us1_create_login import views as auth_views
from apps.us3_start_tracking import views as tracking_views

urlpatterns = [
    # Auth
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Dashboard
    path('', tracking_views.dashboard, name='dashboard'),
    path('today/', tracking_views.today, name='today'),
    
    # Calendar
    path('calendar/', tracking_views.calendar_view, name='calendar'),
]
```

## 🎯 Step 5: Create Views for Each User Story

### US1: Create Login
- [ ] Create login view in `apps/us1_create_login/views.py`
- [ ] Create signup view
- [ ] Test authentication flow

### US2: Password Reset
- [ ] Create password reset view
- [ ] Configure email backend (or use console for dev)
- [ ] Test reset flow

### US3: Start Tracking
- [ ] Create dashboard view
- [ ] Create onboarding flow
- [ ] Add daily check-in form handling

### US4: Cycle Tracking
- [ ] Create period logging view
- [ ] Handle form submission
- [ ] Save to database

### US5: Calculate Period Length
- [ ] Create insights view
- [ ] Calculate average cycle length
- [ ] Calculate predictions

### US6: Editing Mistakes
- [ ] Create edit entry view
- [ ] Add delete functionality
- [ ] Handle updates

### US8: Calendar View
- [ ] Create calendar view
- [ ] Pass period data as JSON
- [ ] Initialize JavaScript calendar

## 🧪 Step 6: Test Each Feature

- [ ] US1: Can users log in and sign up?
- [ ] US2: Can users reset password?
- [ ] US3: Can users complete onboarding?
- [ ] US4: Can users log periods?
- [ ] US5: Are insights calculating correctly?
- [ ] US6: Can users edit/delete entries?
- [ ] US8: Does calendar display properly?

## 🎨 Step 7: Customize & Polish

- [ ] Add custom colors to CSS variables
- [ ] Add favicon and app icons
- [ ] Test on mobile devices
- [ ] Add loading states
- [ ] Test form validation
- [ ] Add helpful error messages

## ♿ Step 8: Accessibility

- [ ] Add ARIA labels to interactive elements
- [ ] Test keyboard navigation
- [ ] Check color contrast ratios
- [ ] Add alt text to images
- [ ] Test with screen reader

## 🚀 Step 9: Deploy

- [ ] Run `python manage.py collectstatic`
- [ ] Test in production mode
- [ ] Configure CDN for static files (optional)
- [ ] Set DEBUG = False

## 📱 Bonus: Progressive Web App

- [ ] Add manifest.json
- [ ] Add service worker
- [ ] Enable offline mode
- [ ] Add "Add to Home Screen" prompt

---

## 🆘 Common Issues & Solutions

### Static files not loading?
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### CSS not updating?
- Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Clear browser cache
- Check browser console for 404 errors

### Forms not submitting?
- Check {% csrf_token %} is present
- Verify form action URL is correct
- Check browser console for JavaScript errors

### Calendar not rendering?
- Ensure jQuery/dependencies are loaded
- Check console for JavaScript errors
- Verify data is being passed correctly from view

---

## 📚 Resources

- Django Static Files: https://docs.djangoproject.com/en/stable/howto/static-files/
- Django Forms: https://docs.djangoproject.com/en/stable/topics/forms/
- Django Templates: https://docs.djangoproject.com/en/stable/topics/templates/
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/
- JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## 💡 Tips for Success

1. **Start simple**: Get login working first, then build up
2. **Test frequently**: Don't wait until everything is built
3. **Use browser DevTools**: Inspect elements, check console
4. **Mobile-first**: Test on phone as you go
5. **Stay organized**: Keep files in the right directories
6. **Version control**: Commit often with clear messages
7. **User feedback**: Show to real users early and often

---

Good luck building Bloom! 🌸
