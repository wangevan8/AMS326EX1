import numpy as np
from scipy.interpolate import lagrange

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
avg_temps = [33, 34, 40, 51, 60, 69, 75, 74, 67, 56, 47, 38]

# Calculate days from Jan 1 for the middle of each month, assuming each month has 31 days
days = [16 + 31*i for i in range(12)]

# Code modified from: numpy.org API reference
# Fit a polynomial using numpy
coeff = np.polyfit(days, avg_temps, 3)
p3 = np.poly1d(coeff)

# Display the coefficient values
a3, a2, a1, a0 = coeff # Highest degree to lowest degree
# Display results
print(f"Polynomial coefficients: P3(t) = {a0:.10f} + {a1:.10f}t + {a2:.10f}t² + {a3:.10f}t³")

# June 4 is day 31*5 + 4 = 159 
june_4 = 31*5 + 4
t_june_4 = p3(june_4)
print(f"Temperature on June 4: {t_june_4:.2f} °F")

# Dec 25 is day 31*11 + 25 = 366
dec_25 = 31*11 + 25
t_dec_25 = p3(dec_25)
print(f"Temperature on Dec 25: {t_dec_25:.2f} °F")

# Search function to find the target days
# Total days = 372 because assume each month has 31 days
def find_days(polynomial, target_temp, start_day=1, end_day=372, step=0.1):
    
    target_tempdays = []
    
    # Code modified from: numpy.org API reference
    # Create a grid of days
    search_days = np.arange(start_day, end_day + step, step)
    
    # Calculate temperatures for each day
    temps = polynomial(search_days)
    
    # Find where temperature crosses the target value
    for i in range(len(temps) - 1):
        # Check if target temperature is crossed between consecutive points
        if (temps[i] <= target_temp and temps[i+1] >= target_temp) or \
           (temps[i] >= target_temp and temps[i+1] <= target_temp):
            
            # Linear interpolation
            day1, day2 = search_days[i], search_days[i+1]
            temp1, temp2 = temps[i], temps[i+1]
            
            # Avoid div by zero
            if temp1 != temp2:
                # Linear interpolation formula
                exact_day = day1 + (target_temp - temp1) * (day2 - day1) / (temp2 - temp1)
                target_tempdays.append(exact_day)
    
    return target_tempdays

# Find days when temperature is 64.89°F
result_days = find_days(p3, 64.89)

# Convert days to month/day format
def convert_date(day):
    for i in range(12):
        if day <= 31 * (i + 1):
            month_idx = i
            day_in_month = int(day - 31 * i)
            return months[month_idx], day_in_month
    return None, None

# Print results
print("\nDays when temperature reaches 64.89°F:")
for day in sorted(result_days):
    month, result_day = convert_date(day)
    print(f"{month} {result_day}: {p3(day):.2f}°F")
