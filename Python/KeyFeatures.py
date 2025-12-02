# Written by Courtney Jackson
# Used AI assistance to help write in python, 
# I wrote the logic of how I wanted it to function, 
# and had AI help me with syntax and structure.
from datetime import datetime
from typing import List, Dict

from connection import get_connection

# Wrote a simple script to get conference recommendations based 
# on what the user is intrested in. It takes their intresets and 
# sees if any of their intrests appear in the conference name or 
# description.
def get_personal_conference_recommendations(user_id: int) -> List[Dict]:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT Interest_1, Interest_2, Interest_3 FROM `user` WHERE ID = %s",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"No user found with ID: {user_id}")
            return []
        
        # Extracts users interests
        interests = [row.get("Interest_1"), row.get("Interest_2"), row.get("Interest_3")]
        interests = [i.strip() for i in interests if i and i.strip()]
        
        if not interests:
            print("User has no interests")
            return []

        # Fetch conferences and match with user interests
        cur.execute(
            "SELECT CID, Title, Descrip FROM Conferences"
        )
        conferences = cur.fetchall()
        
        matched_conferences = []
        for conf in conferences:
            title = conf.get("Title", "").lower()
            description = conf.get("Descrip", "").lower()
            matched_interests = []
            for interest in interests:
                interest_lower = interest.lower()
                if interest_lower in title or interest_lower in description:
                    matched_interests.append(interest)
            
            # If any interests matched, add this conference to our results
            if matched_interests:
                conf['Matched_Interests'] = matched_interests
                matched_conferences.append(conf)
        
        # Print the matching conferences
        if not matched_conferences:
            print("There are no conferences with your interests available right now")
            return []
        
        print(f"\nFound {len(matched_conferences)} matching conferences:")
        for conf in matched_conferences:
            print(f"\nConference ID: {conf.get('CID')}")
            print(f"Title: {conf.get('Title')}")
            print(f"Description: {conf.get('Descrip', '')[:100]}...")
            print(f"Matched Interests: {', '.join(conf.get('Matched_Interests', []))}")
        
        return matched_conferences
    
    # Error block
    except Exception as e:
        print(f"Error fetching user interests: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Sends an email to the user notifying them of upcoming paper deadlines
# for conferences that match their interests
# Email sending to be added in PHASE III
def notify_user_of_paper_deadlines(user_id: int, days_ahead: int = 30) -> List[Dict]:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        
        # Get user interests first
        cur.execute(
            "SELECT Interest_1, Interest_2, Interest_3 FROM `user` WHERE ID = %s",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            print(f"No user found with ID: {user_id}")
            return []
        
        interests = [row.get("Interest_1"), row.get("Interest_2"), row.get("Interest_3")]
        interests = [i.strip() for i in interests if i and i.strip()]
        
        if not interests:
            print("User has no interests - cannot check for relevant deadlines")
            return []
        
        # Calculate the deadline cutoff date
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        # Get conferences with upcoming paper deadlines that match user interests
        cur.execute("""
            SELECT CID, Title, Descrip, PaperDeadline 
            FROM Conferences 
            WHERE PaperDeadline IS NOT NULL 
            AND PaperDeadline >= CURDATE() 
            AND PaperDeadline <= %s
            ORDER BY PaperDeadline ASC
        """, (cutoff_date.date(),))
        
        upcoming_conferences = cur.fetchall()
        
        if not upcoming_conferences:
            print(f"No conferences with paper deadlines in the next {days_ahead} days")
            return []
        
        # Filter conferences that match user interests
        matching_deadline_conferences = []
        
        for conf in upcoming_conferences:
            title = conf.get("Title", "").lower()
            description = conf.get("Descrip", "").lower()
            matched_interests = []
            
            for interest in interests:
                interest_lower = interest.lower()
                if interest_lower in title or interest_lower in description:
                    matched_interests.append(interest)
            
            if matched_interests:
                conf['Matched_Interests'] = matched_interests
                matching_deadline_conferences.append(conf)
        
        # Display upcoming deadlines
        if not matching_deadline_conferences:
            print(f"No conferences matching your interests have paper deadlines in the next {days_ahead} days")
            return []
        
        print(f"\n🚨 UPCOMING PAPER DEADLINES for User {user_id}:")
        print(f"Found {len(matching_deadline_conferences)} conferences with deadlines in the next {days_ahead} days:\n")
        
        for conf in matching_deadline_conferences:
            deadline = conf.get('PaperDeadline')
            days_remaining = (deadline - datetime.now().date()).days if deadline else 0
            
            print(f"📅 Conference: {conf.get('Title')}")
            print(f"   Paper Deadline: {deadline} ({days_remaining} days remaining)")
            print(f"   Matched Interests: {', '.join(conf.get('Matched_Interests', []))}")
            print(f"   Description: {conf.get('Descrip', '')[:100]}...")
            print("-" * 60)
        
        return matching_deadline_conferences
        
    except Exception as e:
        print(f"Error checking paper deadlines: {e}")
        return []
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    test_user_id = 1
    
    print("=== CONFERENCE RECOMMENDATIONS ===")
    recs = get_personal_conference_recommendations(test_user_id)
    
    print("\n" + "="*50)
    print("=== UPCOMING PAPER DEADLINES ===")
    deadlines = notify_user_of_paper_deadlines(test_user_id, days_ahead=30)