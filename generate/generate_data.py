import pandas as pd
from faker import Faker
import numpy as np
from datetime import date, timedelta
import os
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -- step 1: generate employees --------------------
def generate_employees():
    employees = [
        {
            "employee_id": "E001",
            "name": "Maria Zamora",
            "team": 1,
            "role": "team_leader",
            "hourly_rate": 22.00,
            "start_date": "2021-01-15",
            "active": True,
        },
        {
            "employee_id": "E002",
            "name": "Rosa Gutierrez",
            "team": 1,
            "role": "cleaner",
            "hourly_rate": 16.00,
            "start_date": "2021-03-01",
            "active": True,
        },
        {
            "employee_id": "E003",
            "name": "Carmen Lopez",
            "team": 1,
            "role": "cleaner",
            "hourly_rate": 16.00,
            "start_date": "2021-03-01",
            "active": True,
        },
        {
            "employee_id": "E004",
            "name": "Lucia Mendez",
            "team": 1,
            "role": "cleaner",
            "hourly_rate": 15.00,
            "start_date": "2022-06-01",
            "active": True,
        },
        {
            "employee_id": "E005",
            "name": "Sandra Reyes",
            "team": 2,
            "role": "team_leader",
            "hourly_rate": 20.00,
            "start_date": "2021-01-15",
            "active": True,
        },
        {
            "employee_id": "E006",
            "name": "Patricia Flores",
            "team": 2,
            "role": "cleaner",
            "hourly_rate": 16.00,
            "start_date": "2021-04-01",
            "active": True,
        },
        {
            "employee_id": "E007",
            "name": "Angela Torres",
            "team": 2,
            "role": "cleaner",
            "hourly_rate": 15.00,
            "start_date": "2022-09-01",
            "active": False,
        },
    ]
    df_employees = pd.DataFrame(employees)
    df_employees.to_csv(f"{OUTPUT_DIR}/employees.csv", index=False)
    print(f"✅ Employees: {len(df_employees)} records saved")
    return df_employees


# ── STEP 2: SERVICES ──────────────────────────────────
def generate_services():
    services = [
        {
            "service_id": "S001",
            "service_name": "Regular Clean",
            "base_price": 150.00,
            "duration_hours": 1.5,
            "description": "Standard cleaning — kitchen, bathrooms, floors, dusting",
        },
        {
            "service_id": "S002",
            "service_name": "Deep Clean",
            "base_price": 280.00,
            "duration_hours": 3.0,
            "description": "Full deep clean including appliances, baseboards, windows",
        },
        {
            "service_id": "S003",
            "service_name": "Move-Out Clean",
            "base_price": 350.00,
            "duration_hours": 4.0,
            "description": "Complete top-to-bottom clean for vacant properties",
        },
        {
            "service_id": "S004",
            "service_name": "Post-Construction Clean",
            "base_price": 400.00,
            "duration_hours": 5.0,
            "description": "Removal of dust, debris and residue after renovation",
        },
    ]
    df_services = pd.DataFrame(services)
    df_services.to_csv(f"{OUTPUT_DIR}/services.csv", index=False)
    print(f"✅ Services: {len(df_services)} records saved")
    return df_services


# --------step 3: generate clients-----------------------


def generate_clients():

    # ── Long Island city/county/zip mapping ──────────
    suffolk_cities = {
        "St. James": "11780",
        "Smithtown": "11787",
        "Hauppauge": "11788",
        "Nesconset": "11767",
        "Kings Park": "11754",
        "Commack": "11725",
        "East Northport": "11731",
        "Ronkonkoma": "11779",
        "Holbrook": "11741",
        "Patchogue": "11772",
    }

    nassau_cities = {
        "Garden City": "11530",
        "Mineola": "11501",
        "Westbury": "11590",
        "New Hyde Park": "11040",
        "Floral Park": "11001",
    }

    # ── House type logic ─────────────────────────────
    house_types = {
        "Ranch": {"beds": (2, 4), "sqft": (1000, 2000)},
        "Colonial": {"beds": (3, 6), "sqft": (1800, 4000)},
        "Cape Cod": {"beds": (2, 4), "sqft": (1200, 2500)},
        "Mansion": {"beds": (5, 10), "sqft": (5000, 15000)},
        "Condo": {"beds": (1, 3), "sqft": (600, 1500)},
        "Townhouse": {"beds": (2, 4), "sqft": (1200, 2800)},
    }

    # ── Allergies list ───────────────────────────────
    allergy_options = [
        "None",
        "None",
        "None",  # weighted — most have none
        "Bleach",
        "Ammonia",
        "Scented products",
        "Latex gloves",
    ]

    clients = []

    for i in range(1, 121):  # 120 clients
        # Pick city and county
        if random.random() < 0.85:  # 85% Suffolk, 15% Nassau
            city = random.choice(list(suffolk_cities.keys()))
            zip_code = suffolk_cities[city]
            county = "Suffolk"
        else:
            city = random.choice(list(nassau_cities.keys()))
            zip_code = nassau_cities[city]
            county = "Nassau"

        # Pick house type and derive bedrooms + sqft
        house_type = random.choice(list(house_types.keys()))
        bed_min, bed_max = house_types[house_type]["beds"]
        sqft_min, sqft_max = house_types[house_type]["sqft"]

        num_bedrooms = random.randint(bed_min, bed_max)
        square_feet = random.randint(sqft_min, sqft_max)

        # Build start date between 2021 and 2024
        start = date(2021, 1, 1)
        end = date(2024, 12, 31)
        start_date = start + timedelta(days=random.randint(0, (end - start).days))

        clients.append(
            {
                "client_id": f"C{i:03d}",
                "client_name": fake.name(),
                "address": f"{random.randint(1, 999)} {fake.street_name()}",
                "city": city,
                "county": county,
                "zip_code": zip_code,
                "house_type": house_type,
                "num_bedrooms": num_bedrooms,
                "square_feet": square_feet,
                "pets": random.random() < 0.40,  # 40% have pets
                "allergies": random.choice(allergy_options),
                "driveway_access": random.random() < 0.90,  # 90% have driveway
                "active": random.random() < 0.88,  # 88% active
                "start_date": start_date,
            }
        )

    df_clients = pd.DataFrame(clients)
    df_clients.to_csv(f"{OUTPUT_DIR}/clients.csv", index=False)
    print(f"✅ Clients: {len(df_clients)} records saved")
    return df_clients


# ---- step 4: special instructions -----------------------------------
def generate_special_instructions(df_clients):

    categories = {
        "Access": [
            "Garage code is 1234",
            "Key under the front mat",
            "Ring doorbell twice",
            "Side gate is always unlocked",
            "Park in the driveway only",
        ],
        "Pets": [
            "Dog is friendly but keep him in the backyard",
            "Cat hides under the bed — do not let out",
            "Two dogs — keep bathroom door closed",
            "Bird cage in living room — do not open",
            "Fish tank in bedroom — do not unplug",
        ],
        "Elderly": [
            "Client is elderly — keep remotes on coffee table",
            "Do not move furniture — client has mobility issues",
            "Leave walker next to the bed",
            "Client may be home — knock before entering rooms",
            "Keep nightlight plugged in at all times",
        ],
        "Cleaning": [
            "Use unscented products only",
            "Do not use bleach anywhere in the house",
            "Hardwood floors — no wet mop, dry only",
            "Granite countertops — use only provided cleaner",
            "No vacuum on area rugs — hand clean only",
        ],
        "Preference": [
            "Client likes blinds open after cleaning",
            "Always leave a fresh towel on the bathroom counter",
            "Stack mail neatly on kitchen counter",
            "Turn on air freshener after cleaning",
            "Client prefers team to finish before noon",
        ],
    }

    instructions = []
    inst_id = 1

    for _, client in df_clients.iterrows():
        # Each client gets 1-3 random instructions
        num_instructions = random.randint(1, 3)
        used_categories = random.sample(list(categories.keys()), num_instructions)

        for category in used_categories:
            instruction = random.choice(categories[category])
            instructions.append(
                {
                    "instruction_id": f"I{inst_id:03d}",
                    "client_id": client["client_id"],
                    "category": category,
                    "instruction": instruction,
                }
            )
            inst_id += 1

    df_instructions = pd.DataFrame(instructions)
    df_instructions.to_csv(f"{OUTPUT_DIR}/special_instructions.csv", index=False)
    print(f"✅ Special Instructions: {len(df_instructions)} records saved")
    return df_instructions


# -------step 5: generate bookings -------------------------------------


def generate_bookings(df_clients, df_services, df_employees):

    bookings = []
    booking_num = 1

    for _, client in df_clients.iterrows():
        # How often does this client book?
        frequency = random.choice(["weekly", "biweekly"])
        interval = 7 if frequency == "weekly" else 14

        # When did they start booking?
        # Must be after their start_date
        client_start = pd.to_datetime(client["start_date"])
        pipeline_end = date(2024, 12, 31)

        current_date = client_start.date()

        while current_date <= pipeline_end:
            # Pick a service — 70% regular, 20% deep, 10% other
            service = df_services.sample(weights=[70, 20, 5, 5], n=1).iloc[0]

            # Calculate actual charge based on square footage
            sqft_multiplier = client["square_feet"] / 1500
            actual_charge = round(
                service["base_price"] * sqft_multiplier * random.uniform(0.9, 1.2), 2
            )

            # Assign team — active clients alternate teams
            team_id = random.choice([1, 2])

            # Actual hours — varies from estimated
            actual_hours = round(
                service["duration_hours"] * random.uniform(0.8, 1.3), 1
            )

            # Payment
            payment_status = random.choices(
                ["Paid", "Pending", "Overdue"], weights=[85, 10, 5]
            )[0]

            payment_method = random.choice(["Cash", "Check", "Zelle", "Venmo"])

            bookings.append(
                {
                    "booking_id": f"B{booking_num:04d}",
                    "client_id": client["client_id"],
                    "service_id": service["service_id"],
                    "team_id": team_id,
                    "booking_date": current_date,
                    "actual_hours": actual_hours,
                    "actual_charge": actual_charge,
                    "payment_status": payment_status,
                    "payment_method": payment_method,
                }
            )

            booking_num += 1
            current_date += timedelta(days=interval)

    df_bookings = pd.DataFrame(bookings)
    df_bookings.to_csv(f"{OUTPUT_DIR}/bookings.csv", index=False)
    print(f"✅ Bookings: {len(df_bookings)} records saved")
    return df_bookings


def main():
    df_employees = generate_employees()
    df_services = generate_services()
    df_clients = generate_clients()
    generate_special_instructions(df_clients)
    generate_bookings(df_clients, df_services, df_employees)


if __name__ == "__main__":
    main()
