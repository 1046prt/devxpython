# Car Explorer Dashboard

Welcome to the **Luxury Car Explorer**, a beautifully interactive Streamlit dashboard that allows users to explore, visualize, and download detailed specifications of luxury cars across the globe.

---

## 📌 Features

* 🌗 **Dark/Light Theme Toggle**: Adapts to your system preferences.
* 📊 **Visual Analytics**:

  * Price vs Horsepower
  * Horsepower vs Torque
  * Speed vs Acceleration
  * Brand popularity chart
* 🧶 **Dynamic Filters**:

  * Brand
  * Fuel Type
  * Engine Type
* 📄 **Data Table**: View and filter car data instantly.
* 📅 **CSV Download**: Export filtered car information.
* 📊 **Summary Metrics**: Quick insights into average horsepower, speed, acceleration, etc.

---

## 🧠 Dataset Info

This app uses a custom luxury car dataset containing attributes like:

| Column                    | Description                                   |
| ------------------------- | --------------------------------------------- |
| Company Names             | Brand of the car (e.g., Ferrari, Rolls Royce) |
| Cars Names                | Model name                                    |
| Engines                   | Engine type (e.g., V8, V12, Hybrid)           |
| CC/Battery Capacity       | Engine displacement or battery size           |
| HorsePower                | Power output in hp                            |
| Total Speed               | Max speed (km/h)                              |
| Performance(0 - 100 )KM/H | Acceleration time in seconds                  |
| Cars Prices               | Market price of the car                       |
| Fuel Types                | Petrol, Hybrid, etc.                          |
| Seats                     | Number of seats                               |
| Torque                    | Torque value in Nm                            |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/luxury-car-explorer.git
cd luxury-car-explorer
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

> **Note:** Make sure Python 3.8+ is installed.

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

---

## 📁 Project Structure

```bash
luxury-car-explorer/
├── app.py                  # Streamlit main application
├── components/
│   └── data/
│       └── car_dataset.csv # Dataset file
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Roadmap

* [ ] Add tooltip info for hover-over charts
* [ ] Predict car prices with regression models
* [ ] Export to PDF
* [ ] Filter by acceleration range and seating

---

## ♂️ Author

 **Prakash Raj**
Data Scientist | Web Developer
🔗 [LinkedIn](https://linkedin.com/in/1046prt) | 🌐 [Portfolio](prakashraj.info)

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).
