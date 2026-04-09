import asyncio
from vanna_setup import get_agent
from vanna.core.user import RequestContext

async def seed_memory():
    # 1. Initialize the agent
    agent = get_agent()
    
    # 2. Create a dummy context for the 'admin' user
    # Vanna 2.0 needs this to know who is seeding the memory
    context = RequestContext(user_id="admin", tenant_id="default")
    
    # 3. The 15 required Q&A pairs
    examples = [
        # Patient Queries
        ("How many patients do we have?", "SELECT COUNT(*) AS total_patients FROM patients"),
        ("Which city has the most patients?", "SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1"),
        ("List patients from Mumbai", "SELECT * FROM patients WHERE city = 'Mumbai'"),
        ("Show me all female patients", "SELECT * FROM patients WHERE gender = 'F'"),

        # Doctor Queries
        ("List all doctors and their specializations", "SELECT name, specialization FROM doctors"),
        ("Which doctor has the most appointments?", "SELECT d.name, COUNT(a.id) as total_appointments FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.name ORDER BY total_appointments DESC LIMIT 1"),

        # Appointment Queries
        ("How many cancelled appointments do we have?", "SELECT COUNT(*) FROM appointments WHERE status = 'Cancelled'"),
        ("Show me appointments for last month", "SELECT * FROM appointments WHERE appointment_date >= date('now', '-1 month')"),
        ("List appointments for today", "SELECT * FROM appointments WHERE date(appointment_date) = date('now')"),

        # Financial Queries
        ("What is the total revenue?", "SELECT SUM(total_amount) AS total_revenue FROM invoices"),
        ("Show revenue by doctor", """
            SELECT d.name, SUM(i.total_amount) AS total_revenue 
            FROM invoices i 
            JOIN appointments a ON a.patient_id = i.patient_id 
            JOIN doctors d ON d.id = a.doctor_id 
            GROUP BY d.name ORDER BY total_revenue DESC
        """),
        ("Show unpaid invoices", "SELECT * FROM invoices WHERE status = 'Pending' OR status = 'Overdue'"),
        ("What is the average treatment cost?", "SELECT AVG(cost) FROM treatments"),

        # Time-based Queries
        ("Show monthly appointment trends for the past 6 months", "SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) FROM appointments GROUP BY month ORDER BY month DESC LIMIT 6"),
        ("Show patient registration trend by month", "SELECT strftime('%Y-%m', registered_date) as month, COUNT(*) FROM patients GROUP BY month ORDER BY month")
    ]

    print(" Starting to seed agent memory...")
    
    for question, sql in examples:
        
        await agent.agent_memory.save_tool_usage(
            context=context,        
            question=question,     
            tool_name="run_sql",   
            args={"sql": sql},     
            success=True           
        )
    
    print(f"Agent memory seeded with {len(examples)} examples.")

if __name__ == "__main__":
    asyncio.run(seed_memory())
