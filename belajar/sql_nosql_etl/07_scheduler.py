"""
Automation: Scheduler / Cronjob untuk ETL Pipeline.

3 cara menjalankan:
1. Python Scheduler (schedule library) - looping dalam proses
2. Cronjob Linux
3. Docker + scheduler

Contoh 1: Python Scheduler (cocok untuk development)
    python 07_scheduler.py

Contoh 2: Cronjob Linux (production)
    # crontab -e
    # Jalankan setiap jam:
    0 * * * * cd /path/ke/project && python 06_etl_pipeline.py

Contoh 3: systemd service (daemon)
    [Unit]
    Description=ETL Scheduler for Reporting DB
    [Service]
    ExecStart=/usr/bin/python /path/ke/project/07_scheduler.py
    Restart=always
    [Install]
    WantedBy=multi-user.target
"""

import time
import subprocess
import os
import sys
from datetime import datetime

# Konfigurasi
INTERVAL_MINUTES = 15
ETL_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '06_etl_pipeline.py')
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'scheduler.log')


def run_etl():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] Running ETL pipeline...')
    try:
        result = subprocess.run(
            [sys.executable, ETL_SCRIPT],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        with open(LOG_FILE, 'a') as f:
            f.write(f'[{timestamp}] SUCCESS\n{output}\n\n')
        print(f'[{timestamp}] SUCCESS')
        print(output)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip()
        with open(LOG_FILE, 'a') as f:
            f.write(f'[{timestamp}] ERROR\n{error_msg}\n\n')
        print(f'[{timestamp}] ERROR: {error_msg}')


def run_once():
    """Gunakan ini untuk Cronjob / systemd (1 kali jalan, lalu exit)."""
    run_etl()


def run_loop():
    """Gunakan ini untuk scheduler daemon (loop terus-menerus)."""
    print(f'ETL Scheduler started. Interval: {INTERVAL_MINUTES} menit')
    print(f'Log: {LOG_FILE}')
    print('Press Ctrl+C to stop.')

    run_etl()

    while True:
        for remaining in range(INTERVAL_MINUTES * 60, 0, -1):
            mins = remaining // 60
            secs = remaining % 60
            print(f'\rNext ETL in: {mins:02d}:{secs:02d}', end='')
            time.sleep(1)
        print()
        run_etl()


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'loop'

    if mode == 'once':
        run_once()
    elif mode == 'loop':
        run_loop()
    else:
        print(f'Usage: python {os.path.basename(__file__)} [once|loop]')
        print('  once  - Jalankan ETL sekali (untuk cronjob)')
        print('  loop  - Jalankan scheduler looping (default)')
