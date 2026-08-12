# ♻️ SmartWaste Priority System

A web-based waste management system that predicts waste collection priority based on waste quantity and collection delay.

## 🚀 Features

- ♻️ Waste collection priority prediction
- 📊 Admin dashboard
- 📈 Data visualization using charts
- 🔍 Search predictions
- 🗑️ Delete prediction records
- 📥 Export prediction data
- 💾 SQLite database integration
- 🎨 Responsive and user-friendly interface

## 🛠️ Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js

## 📌 Priority Logic

The system calculates a priority score using:

Priority Score = Waste Quantity + (Collection Delay × 10)

### Priority Levels

| Score | Priority |
|------:|----------|
| 80+ | 🔴 High |
| 50–79 | 🟡 Medium |
| Below 50 | 🟢 Low |

## 📂 Project Structure

```text
SmartWaste-Priority-System/
│
├── app.py
├── main.py
├── smartwaste.db
│
├── static/
│   ├── style.css
│   └── ...
│
└── templates/
    ├── index.html
    ├── dashboard.html
    └── ...
## 🎯 Project Objective

The main objective of this project is to help waste management teams identify high-priority waste collection areas and improve collection efficiency using a simple rule-based prediction system.

## 🔮 Future Enhancements

- Machine learning-based prediction
- Real-time waste monitoring
- GPS-based collection tracking
- Automated notifications
- Advanced analytics
- User authentication and role management

## 👨‍💻 Author

**NATAM PAVANSAI**

B.Tech – Computer Science Engineering

## 📸 Screenshots

Project screenshots are available in the repository files.

