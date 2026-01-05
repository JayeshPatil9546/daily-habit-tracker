# Daily Habit Tracker

## Overview

A full-stack habit tracking application designed to help users monitor daily activities and build positive habits. Track activities like:
- Wake up at 6:00 AM
- Morning run (30 min)
- Workout (gym/home)
- No junk food today
- Drink 3L water
- Read 20 pages
- Meditate 10 min
- Sleep by 11:00 PM

Users can check off completed habits daily, view streaks, and analyze growth with analytics and data visualization.

## Features

### 1. Daily Habit Checklist
- Add custom habits
- Check off completed habits with one click
- Mark habits as Done or Skipped
- Add optional notes for each habit

### 2. Streak Tracking
- Current streak counter for each habit
- Longest streak achievements
- Fire emoji motivation
- Streak notifications

### 3. Calendar View
- Monthly calendar with color-coded days
- Green = All habits completed
- Yellow = Some habits completed
- Red = Many habits missed
- Click dates to see daily details

### 4. Analytics & Insights
- Weekly/Monthly completion rates
- Bar charts showing habit completion %
- Pie charts for weekly overview
- Trend analysis over time
- Auto-generated growth insights
- Pattern detection (e.g., weekend habits)

### 5. Data Management
- Local storage (browser) or cloud sync
- Export data as CSV/Excel
- Backup and restore
- Dark mode support

## Tech Stack

### Frontend
- **React.js** - UI components
- **Chart.js** / **Recharts** - Data visualization
- **CSS3** / **TailwindCSS** - Styling
- **Axios** - API calls
- **React Router** - Navigation

### Backend
- **Node.js** - Server
- **Express.js** - API framework
- **MongoDB** - Database
- **JWT** - Authentication
- **Bcrypt** - Password hashing

### Tools
- **Git** - Version control
- **npm** - Package management
- **VS Code** - Development

## Project Structure

```
daily-habit-tracker/
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── HabitList.jsx
│   │   │   ├── HabitCard.jsx
│   │   │   ├── CheckboxItem.jsx
│   │   │   ├── Calendar.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── Today.jsx
│   │   │   ├── Weekly.jsx
│   │   │   ├── Monthly.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Settings.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── App.css
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── backend/                    # Node/Express backend
│   ├── routes/
│   │   ├── habits.js
│   │   ├── users.js
│   │   └── analytics.js
│   ├── controllers/
│   │   ├── habitController.js
│   │   ├── userController.js
│   │   └── analyticsController.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Habit.js
│   │   └── DailyLog.js
│   ├── middleware/
│   │   └── authMiddleware.js
│   ├── config/
│   │   └── db.js
│   ├── server.js
│   ├── package.json
│   └── .env.example
├── docs/                       # Documentation
│   ├── API.md
│   ├── SETUP.md
│   └── FEATURES.md
├── .gitignore
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js (v14+)
- npm or yarn
- MongoDB (local or Atlas)
- Git

### Backend Setup

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your MongoDB URI and JWT secret
npm start
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
# App opens at http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout

### Habits
- `GET /api/habits` - Get all habits
- `POST /api/habits` - Create new habit
- `PUT /api/habits/:id` - Update habit
- `DELETE /api/habits/:id` - Delete habit

### Daily Logs
- `POST /api/logs` - Log habit completion
- `GET /api/logs/:date` - Get logs for date
- `GET /api/logs/habit/:habitId` - Get logs for habit

### Analytics
- `GET /api/analytics/weekly` - Weekly stats
- `GET /api/analytics/monthly` - Monthly stats
- `GET /api/analytics/insights` - Growth insights
- `GET /api/analytics/trends` - Trend data

## Usage

1. **Register/Login** - Create account
2. **Add Habits** - Click "+" to add habits
3. **Daily Tracking** - Check off completed habits each day
4. **View Calendar** - See overall consistency
5. **Check Analytics** - Track growth and patterns
6. **Export Data** - Backup your habit data

## Sample Habits

```javascript
const sampleHabits = [
  { name: "Wake up at 6:00 AM", icon: "☀️", category: "morning" },
  { name: "Morning run (30 min)", icon: "🏃", category: "fitness" },
  { name: "Workout (gym/home)", icon: "💪", category: "fitness" },
  { name: "No junk food today", icon: "🥗", category: "nutrition" },
  { name: "Drink 3L water", icon: "💧", category: "health" },
  { name: "Read 20 pages", icon: "📖", category: "learning" },
  { name: "Meditate 10 min", icon: "🧘", category: "wellness" },
  { name: "Sleep by 11:00 PM", icon: "😴", category: "health" }
];
```

## Data Models

### User Model
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String (hashed),
  createdAt: Date,
  updatedAt: Date
}
```

### Habit Model
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  name: String,
  icon: String,
  category: String,
  color: String,
  createdAt: Date
}
```

### DailyLog Model
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  habitId: ObjectId,
  date: Date,
  completed: Boolean,
  notes: String,
  createdAt: Date
}
```

## Analytics Features

### Weekly Report
- 7-day completion rate
- Best performing habit
- Least completed habit
- Completion trend

### Monthly Report
- 30-day completion rate
- Streak statistics
- Growth comparison to last month
- Top 3 habits

### Insights
- "You woke up early on 6 out of 7 days"
- "Your workout consistency improved by 15%"
- "You usually skip habits on weekends"

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Author

**JayeshPatil9546**
- GitHub: [@JayeshPatil9546](https://github.com/JayeshPatil9546)
- Location: Pune, India

## Support

For issues, suggestions, or feature requests:
- Open an Issue on GitHub
- Email: your-email@example.com

## Roadmap

- [x] Basic habit tracking
- [x] Daily checklist
- [x] Calendar view
- [ ] Mobile app (React Native)
- [ ] Social sharing
- [ ] Habit recommendations
- [ ] AI-powered insights
- [ ] Multi-language support
- [ ] Premium features

## Changelog

### v1.0.0 (Initial Release)
- Daily habit tracking
- Streak counter
- Calendar visualization
- Basic analytics
- User authentication

---

**Start building better habits today!** 🚀
