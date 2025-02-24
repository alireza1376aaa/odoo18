{
    'name': 'Auto HR Attendance',
    'version': '1.0',
    'summary': 'Automatically check-in and check-out employees based on login activity',
    'category': 'Human Resources',
    'author': 'Your Name',
    'depends': ['hr_attendance', 'base'],
    'data': [
        'data/auto_attendance_cron.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
