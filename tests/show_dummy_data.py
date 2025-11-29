#!/usr/bin/env python3
"""
Show what the dummy data will produce
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.depression_calculator import DepressionCalculator

calc = DepressionCalculator('teams_config.json')
result = calc.calculate_total_depression()
emoji, level = calc.get_depression_level(result['total_score'])

print('\n' + '='*60)
print('📊 DUMMY DATA TEST RESULTS')
print('='*60)
print(f'\nDepression Score: {result["total_score"]:.1f}')
print(f'Level: {emoji} {level}\n')
print('Breakdown by Team:')
print('-'*60)

for name, data in sorted(result['breakdown'].items(), key=lambda x: x[1]['score'], reverse=True):
    print(f'  {name:30s}: {data["score"]:6.1f} pts')
    if 'record' in data:
        print(f'    Record: {data["record"]}')

print('\n' + '='*60)
print('✅ Dummy data loaded successfully!')
print('\nTo test the dashboard:')
print('1. Start backend: cd backend && python3 app.py')
print('2. Start frontend: cd frontend && npm install && npm run dev')
print('3. Open http://localhost:3000')
print('='*60 + '\n')

