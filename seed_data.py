"""
SmartLab Hub — Sample Data Seeder
Run with: python seed_data.py
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartLab_Hub.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from catalog.models import Category, Equipment
from inventory.models import EquipmentUnit
from bookings.models import Booking
from datetime import date, timedelta
import random

User = get_user_model()


def seed():
    print("🌱 Seeding SmartLab Hub with sample data...")

    # ── CATEGORIES ──
    categories_data = [
        ('Microscopy', 'Optical and electron microscopes'),
        ('Centrifugation', 'Centrifuges and separators'),
        ('Spectroscopy', 'Spectrometers and analyzers'),
        ('Weighing', 'Analytical and precision balances'),
        ('Temperature Control', 'Incubators, ovens, and fridges'),
        ('Electrophoresis', 'Gel electrophoresis equipment'),
    ]
    categories = {}
    for name, desc in categories_data:
        cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
        categories[name] = cat
    print(f"  ✓ {len(categories)} categories created")

    # ── VENDOR USERS ──
    vendors = []
    vendor_data = [
        ('vendor1', 'Amara', 'Osei', 'amara@biolabsupply.ke', 'BioLab Supply Kenya'),
        ('vendor2', 'Chinwe', 'Adeyemi', 'chinwe@sciequip.ke', 'SciEquip Africa'),
    ]
    for username, fn, ln, email, org in vendor_data:
        v, created = User.objects.get_or_create(username=username, defaults={
            'email': email, 'first_name': fn, 'last_name': ln,
            'role': 'VENDOR', 'organization': org, 'is_active': True,
            'pickup_location': 'Nairobi CBD, Science House', 'dropoff_location': 'Nairobi CBD, Science House'
        })
        if created:
            v.set_password('vendor123')
            v.save()
        vendors.append(v)
    print(f"  ✓ {len(vendors)} vendor accounts (password: vendor123)")

    # ── STUDENT USERS ──
    students = []
    student_data = [
        ('student1', 'Kofi', 'Mensah', 'kofi@uon.ac.ke', 'University of Nairobi'),
        ('student2', 'Fatima', 'Hassan', 'fatima@ku.ac.ke', 'Kenyatta University'),
        ('researcher1', 'Dr. Emmanuel', 'Nkosi', 'emmanuel@icipe.org', 'ICIPE'),
    ]
    for username, fn, ln, email, org in student_data:
        u, created = User.objects.get_or_create(username=username, defaults={
            'email': email, 'first_name': fn, 'last_name': ln,
            'role': 'STUDENT' if 'student' in username else 'RESEARCHER',
            'organization': org, 'is_active': True,
        })
        if created:
            u.set_password('student123')
            u.save()
        students.append(u)
    print(f"  ✓ {len(students)} student/researcher accounts (password: student123)")

    # ── EQUIPMENT ──
    equipment_data = [
        {
            'name': 'Compound Light Microscope',
            'brand': 'Olympus', 'model_number': 'CX23',
            'category': 'Microscopy',
            'description': 'Advanced compound microscope with 40x-1000x magnification. Ideal for cell biology, microbiology, and histology studies.',
            'rental_price_per_day': 1500, 'purchase_price': 185000,
            'serials': ['OLY-CX23-001', 'OLY-CX23-002'],
        },
        {
            'name': 'Fluorescence Microscope',
            'brand': 'Zeiss', 'model_number': 'Primo Star',
            'category': 'Microscopy',
            'description': 'High-performance fluorescence microscope with LED illumination. Suitable for immunofluorescence and live cell imaging.',
            'rental_price_per_day': 4500, 'purchase_price': 850000,
            'serials': ['ZSS-PS-001'],
        },
        {
            'name': 'Microcentrifuge',
            'brand': 'Eppendorf', 'model_number': '5424 R',
            'category': 'Centrifugation',
            'description': 'Refrigerated microcentrifuge reaching up to 21,382 × g. Perfect for molecular biology and biochemistry applications.',
            'rental_price_per_day': 2000, 'purchase_price': 320000,
            'serials': ['EPP-5424-001', 'EPP-5424-002', 'EPP-5424-003'],
        },
        {
            'name': 'UV-Vis Spectrophotometer',
            'brand': 'Shimadzu', 'model_number': 'UV-1900',
            'category': 'Spectroscopy',
            'description': 'Double-beam UV-Vis spectrophotometer with wavelength range 190-1100 nm. For quantitative and qualitative analysis.',
            'rental_price_per_day': 3500, 'purchase_price': 650000,
            'serials': ['SHM-UV1900-001'],
        },
        {
            'name': 'Analytical Balance',
            'brand': 'Mettler Toledo', 'model_number': 'ME204',
            'category': 'Weighing',
            'description': 'High-precision analytical balance with 220g capacity and 0.1mg readability. GxP compliant.',
            'rental_price_per_day': 800, 'purchase_price': 95000,
            'serials': ['MT-ME204-001', 'MT-ME204-002'],
        },
        {
            'name': 'CO2 Incubator',
            'brand': 'Thermo Fisher', 'model_number': 'Heracell VIOS 160i',
            'category': 'Temperature Control',
            'description': 'Direct heat CO2 incubator with HEPA filtration. Essential for mammalian cell culture work.',
            'rental_price_per_day': 5500, 'purchase_price': 1200000,
            'serials': ['TF-VIOS-001'],
        },
        {
            'name': 'Gel Electrophoresis System',
            'brand': 'Bio-Rad', 'model_number': 'PowerPac Basic',
            'category': 'Electrophoresis',
            'description': 'Horizontal gel electrophoresis system for DNA/RNA analysis. Includes power supply and gel casting tray.',
            'rental_price_per_day': 1200, 'purchase_price': 85000,
            'serials': ['BR-PPB-001', 'BR-PPB-002'],
        },
    ]

    units_created = 0
    for i, eq_data in enumerate(equipment_data):
        vendor = vendors[i % len(vendors)]
        serials = eq_data.pop('serials')
        cat_name = eq_data.pop('category')

        eq, created = Equipment.objects.get_or_create(
            name=eq_data['name'],
            vendor=vendor,
            defaults={
                **eq_data,
                'category': categories[cat_name],
            }
        )

        for serial in serials:
            unit, u_created = EquipmentUnit.objects.get_or_create(
                serial_number=serial,
                defaults={
                    'equipment': eq,
                    'status': random.choice(['AVAILABLE', 'AVAILABLE', 'AVAILABLE', 'RENTED', 'MAINTENANCE']),
                    'internal_id': f'LAB-{serial[-3:]}',
                }
            )
            if u_created:
                units_created += 1

    print(f"  ✓ {len(equipment_data)} equipment listings with {units_created} units")

    # ── SAMPLE BOOKINGS ──
    avail_units = EquipmentUnit.objects.filter(status='AVAILABLE')
    if avail_units.exists() and students:
        for i, student in enumerate(students[:2]):
            unit = avail_units[i % avail_units.count()]
            start = date.today() - timedelta(days=random.randint(1, 30))
            end = start + timedelta(days=random.randint(1, 7))
            Booking.objects.get_or_create(
                user=student,
                unit=unit,
                start_date=start,
                defaults={
                    'end_date': end,
                    'booking_type': 'RENTAL',
                    'status': random.choice(['COMPLETED', 'ACTIVE', 'PENDING']),
                    'pick_up_location': 'Nairobi CBD Science House',
                    'drop_off_location': 'Nairobi CBD Science House',
                }
            )
        print(f"  ✓ Sample bookings created")

    print("\n✅ Seed complete!")
    print("\n──────────────────────────────────")
    print("  Login Credentials:")
    print("  Admin:      admin / admin123")
    print("  Vendor 1:   vendor1 / vendor123")
    print("  Vendor 2:   vendor2 / vendor123")
    print("  Student:    student1 / student123")
    print("  Researcher: researcher1 / student123")
    print("──────────────────────────────────")


if __name__ == '__main__':
    seed()
