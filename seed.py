import asyncio
from src.db import db

async def seed():
    # Connect to the database
    await db.connect()

    print("Cleaning database...")
    # Delete in order to avoid foreign key constraints
    await db.invoices.delete_many()
    await db.students.delete_many()
    await db.schools.delete_many()

    print("Seeding schools...")
    # 1. School with perfectly balanced finances
    mattilda = await db.schools.create(data={'name': 'Mattilda Academy'})
    
    # 2. School with many unpaid invoices (Debt scenario)
    liceo = await db.schools.create(data={'name': 'Liceo Canadiense'})
    
    # 3. New school without activity
    empty_school = await db.schools.create(data={'name': 'Escuela de Matildas'})

    print("Seeding students and invoices...")
    
    # Alice: Paid her only invoice
    alice = await db.students.create(data={'name': 'Alice', 'schoolId': mattilda.id})
    await db.invoices.create(data={
        'name': 'Colegiatura Enero',
        'amount': 5000,
        'paid': True,
        'studentId': alice.id
    })
    
    # Bob: Has one paid and one unpaid
    bob = await db.students.create(data={'name': 'Bob Smith', 'schoolId': mattilda.id})
    await db.invoices.create(data={
        'name': 'Colegiatura Enero',
        'amount': 5000,
        'paid': True,
        'studentId': bob.id
    })
    await db.invoices.create(data={
        'name': 'Extracurricular Sports',
        'amount': 1500,
        'paid': False,
        'studentId': bob.id
    })

    # Charlie: Large unpaid debt
    charlie = await db.students.create(data={'name': 'Charlie Brown', 'schoolId': liceo.id})
    await db.invoices.create(data={
        'name': 'Colegiatura Anual',
        'amount': 25000,
        'paid': False,
        'studentId': charlie.id
    })
    await db.invoices.create(data={
        'name': 'Pago Biblioteca',
        'amount': 200,
        'paid': False,
        'studentId': charlie.id
    })
    
    # Diana: Partial payer
    diana = await db.students.create(data={'name': 'Diana Prince', 'schoolId': liceo.id})
    await db.invoices.create(data={'name': 'Tech Fee', 'amount': 1000, 'paid': True, 'studentId': diana.id})
    await db.invoices.create(data={'name': 'Lab Fee', 'amount': 1200, 'paid': False, 'studentId': diana.id})

    # One student, no invoices yet
    await db.students.create(data={'name': 'Eve Adams', 'schoolId': empty_school.id})

    print("Seeding completed successfully!")
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(seed())
